```sh
# install terraform
brew install terraform

# verify version
# v1.0.11
terraform
terraform version

# azure default subscription
az login
az account show
az account set --subscription "495322cb-95ae-4e66-b31d-1ea25d0b4ada"

# create service principal
az ad sp create-for-rbac --name iac_terraform_identity

{
  "appId": "",
  "displayName": "",
  "name": "",
  "password": "",
  "tenant": ""
}
```

```sh
# access iac terraform script
/Users/luanmorenomaciel/BitBucket/big-data-on-k8s/iac/aks/aks_owshq_prod

# k8s.tf = build cluster and resources
# variables.tf = reusable script
# output.tf = output info

# init terraform script process
# prepare working directory
terraform init

# build plan to build
# changes required
terraform plan

# apply creation iac code
# create resources
terraform apply -auto-approve

# access cluster
# kubernetes aks engine
az account set --subscription 495322cb-95ae-4e66-b31d-1ea25d0b4ada
az aks get-credentials --resource-group k8s-aks-owshq-prod --name aks-owshq-prod

# change [variables.tf]
terraform plan
terraform apply

# remove resources [rg]
# destroy resources
terraform destroy -auto-approve
```
