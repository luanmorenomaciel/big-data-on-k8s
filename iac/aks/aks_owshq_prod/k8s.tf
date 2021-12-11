/*
https://github.com/hashicorp/terraform-provider-azurerm/tree/main/examples/kubernetes
https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs
https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/kubernetes_cluster
https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/kubernetes_cluster_node_pool
https://docs.microsoft.com/en-us/azure/aks/use-multiple-node-pools
https://docs.microsoft.com/en-us/azure/aks/use-system-pools
*/

# use of azure provider
# pushed from terraform registry
terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "~>2.0"
    }
  }
}

# specify azure subscription info
# use azure cli to retrieve it
provider "azurerm" {
  subscription_id = "495322cb-95ae-4e66-b31d-1ea25d0b4ada"
  client_id = "fb1b5c6f-ec87-45c6-a41f-02173f0b29b7"
  client_secret = "TCvn~hGX7hr0a9p6PtaH9Nd7zM~MRhigI6"
  tenant_id = "876c68e8-02d9-4abc-912e-4b9d8fc61c1e"
  features {}
}

# specify resource group
# logical unit of grouping
resource "azurerm_resource_group" "k8s" {
    name = var.resource_group_name
    location = var.location
}

# building kubernetes cluster
# production-ready environment
resource "azurerm_kubernetes_cluster" "k8s" {
    name = var.cluster_name
    location = azurerm_resource_group.k8s.location
    resource_group_name = azurerm_resource_group.k8s.name
    dns_prefix = var.dns_prefix

    # enable ssh key use
    linux_profile {
        admin_username = "ubuntu"

        # copy of the ssh key for access
        ssh_key {
            key_data = file(var.ssh_public_key)
        }
    }

    # system node pool
    # kubernetes.azure.com/mode: system
    # scheduling system pods
    # use taint = critical addons only = true: no schedule
    # use of scale set vms = unit to scale machines
    # https://docs.microsoft.com/en-us/azure/aks/use-system-pools
    # https://docs.microsoft.com/en-us/azure/virtual-machine-scale-sets/overview
    default_node_pool {
        name               = "agentpool"
        node_count         = var.agent_count
        vm_size            = "Standard_DS2_v2"
        type               = "VirtualMachineScaleSets"
        only_critical_addons_enabled = true
        # node_taints        = ["CriticalAddonsOnly=true:NoSchedule"]
        # repel user pods to schedule
    }

    # account to provision resources
    # rbac permission control
    service_principal {
        client_id     = var.client_id
        client_secret = var.client_secret
    }

    # addon features by aks product
    addon_profile {

      aci_connector_linux {
        enabled = false
      }

      azure_policy {
        enabled = false
      }

      http_application_routing {
        enabled = false
      }

      kube_dashboard {
        enabled = false
      }

      oms_agent {
        enabled = false
      }
    }

    # network profile info
    network_profile {
      load_balancer_sku = "Standard"
      network_plugin    = "kubenet"
    }

    # tags to add
    tags = {
        Environment = "Production"
    }
}

# build additional node pool
resource "azurerm_kubernetes_cluster_node_pool" "node-pool-user-1" {
  kubernetes_cluster_id = azurerm_kubernetes_cluster.k8s.id
  name                  = "npds3v2"
  vm_size               = "Standard_DS3_v2"
  enable_auto_scaling   = true
  min_count             = 2
  max_count             = 5
  node_count            = var.node_pol_npds3v2
  availability_zones    = [1,2,3]
}

# build additional node pool
resource "azurerm_kubernetes_cluster_node_pool" "node-pool-user-2" {
  kubernetes_cluster_id = azurerm_kubernetes_cluster.k8s.id
  name                  = "npd8sv3"
  vm_size               = "Standard_D8S_v3"
  enable_auto_scaling   = true
  min_count             = 3
  max_count             = 5
  node_count            = var.node_pool_npd8sv3
  availability_zones    = [1,2,3]
}

# add spot instances in a different node poll
# cost savings for some non-critical pipelines
# https://docs.microsoft.com/en-us/azure/aks/spot-node-pool