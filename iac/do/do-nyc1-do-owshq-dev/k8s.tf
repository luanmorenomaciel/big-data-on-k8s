data "digitalocean_kubernetes_versions" "cluster" {
  version_prefix = "1.20.11-do.0"
}

resource "digitalocean_kubernetes_cluster" "do-owshq-dev" {
  name         = "do-owshq-dev"
  region       = "nyc1"
  auto_upgrade = true
  version      = data.digitalocean_kubernetes_versions.cluster.latest_version

  node_pool {
    name       = "default"
    size       = "s-2vcpu-4gb"
    node_count = 3
  }
}