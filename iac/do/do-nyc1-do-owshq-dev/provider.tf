terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "1.22.2"
    }
  }
}

variable "do_token" {default = "luan-moreno"}
variable "pvt_key" {default = "348fd66dc6a04b53a9aa2884f2b2e7df5df2477ec8cacb2f4e726b11d7cae085"}

provider "digitalocean" {
  token = var.do_token
}

data "digitalocean_ssh_key" "terraform" {
  # ls ~/.ssh/*.pub
  name = "/Users/luanmorenomaciel/.ssh/id_rsa.pub"
}