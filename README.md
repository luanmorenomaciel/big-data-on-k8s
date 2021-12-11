```shell
#  microsoft azure
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
az account set --subscription []
az aks get-credentials --resource-group k8s-aks-owshq-dev --name aks-owshq-dev

# google gcp
# https://cloud.google.com/sdk/gcloud
gcloud container clusters get-credentials [] --region us-central1

# digital ocean
# https://docs.digitalocean.com/reference/doctl/how-to/install/
doctl kubernetes cluster kubeconfig save []

# linode
# https://www.linode.com/docs/guides/linode-cli/
cluster_id=[]
linode-cli lke clusters-list
linode-cli lke kubeconfig-view $cluster_id

# local kube config
kubectl config view
$HOME/.kube/config
```

```shell
# microsoft azure aks cost
# 7 = virtual machines (ds3v2)
# 4 vcpus & 14 gb of ram
# 1,170.19
# ~ R$ 10.000
```
