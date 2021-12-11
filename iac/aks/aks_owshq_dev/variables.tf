variable "client_id" {
    default = "fb1b5c6f-ec87-45c6-a41f-02173f0b29b7"
}

variable "client_secret" {
    default = "TCvn~hGX7hr0a9p6PtaH9Nd7zM~MRhigI6"
}

variable "agent_count" {
    default = 8
}

variable "ssh_public_key" {
    default = "~/.ssh/id_rsa.pub"
}

variable "dns_prefix" {
    default = "dns"
}

variable cluster_name {
    default = "aks-owshq-dev"
}

variable resource_group_name {
    default = "k8s-aks-owshq-dev"
}

variable location {
    default = "East US 2"
}
