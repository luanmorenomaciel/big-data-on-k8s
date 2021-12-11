terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "~>2.0"
    }
  }
}

provider "azurerm" {
  subscription_id = "495322cb-95ae-4e66-b31d-1ea25d0b4ada"
  client_id = "fb1b5c6f-ec87-45c6-a41f-02173f0b29b7"
  client_secret = "TCvn~hGX7hr0a9p6PtaH9Nd7zM~MRhigI6"
  tenant_id = "876c68e8-02d9-4abc-912e-4b9d8fc61c1e"
  features {}
}

resource "azurerm_resource_group" "k8s" {
    name = var.resource_group_name
    location = var.location
}

resource "azurerm_kubernetes_cluster" "k8s" {
    name = var.cluster_name
    location = azurerm_resource_group.k8s.location
    resource_group_name = azurerm_resource_group.k8s.name
    dns_prefix = var.dns_prefix

    linux_profile {
        admin_username = "ubuntu"

        ssh_key {
            key_data = file(var.ssh_public_key)
        }
    }

    default_node_pool {
        name            = "agentpool"
        node_count      = var.agent_count
        vm_size         = "Standard_DS3_v2"
    }

    service_principal {
        client_id     = var.client_id
        client_secret = var.client_secret
    }

    network_profile {
        load_balancer_sku = "Standard"
        network_plugin = "kubenet"
    }

    tags = {
        Environment = "QA"
    }
}