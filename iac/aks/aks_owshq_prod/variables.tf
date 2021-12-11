# [client id] from azure subscription
variable "client_id" {
    default = "fb1b5c6f-ec87-45c6-a41f-02173f0b29b7"
}

# [client secret] from azure subscription
variable "client_secret" {
    default = "TCvn~hGX7hr0a9p6PtaH9Nd7zM~MRhigI6"
}

# default node pool count
variable "agent_count" {
    default = 1
}
# user node pools
variable "node_pol_npds3v2" {
    default = 2
}
variable "node_pool_npd8sv3" {
    default = 3
}

# local public key location
variable "ssh_public_key" {
    default = "~/.ssh/id_rsa.pub"
}

# prefix to build dns name
variable "dns_prefix" {
    default = "dns"
}

# name of the cluster
variable cluster_name {
    default = "aks-owshq-prod"
}

# name of the resource group
variable resource_group_name {
    default = "k8s-aks-owshq-prod"
}

# default location
variable location {
    default = "East US 2"
}
