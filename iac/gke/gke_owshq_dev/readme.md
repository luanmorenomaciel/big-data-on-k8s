# Terraform & GKE [Google Kubernetes Engine]
https://learn.hashicorp.com/tutorials/terraform/gke

### configure terraform
```sh
# install terraform 
brew install terraform

# verify version
# v1.0.10
terraform
terraform version

# google sdk install, init and authorize
brew install --cask google-cloud-sdk
gcloud init
gcloud auth application-default login
```

### build gke cluster using google provider
```sh
# access iac terraform script
/Users/luanmorenomaciel/BitBucket/big-data-on-k8s/iac/gke/gke_owshq_dev

# get project id
gcloud config get-value project

# vpc.tf = provision vpc and subnet resources
# gke.tf = provision gke cluster (separate from managed node pool)
# terraform.tfvars = template for variables
# versions.tf = terraform version requirement

# init terraform script process
# prepare working directory
terraform init

# note: compute engine & kubernetes engine api are required for terraform apply to work on this configuration
# build plan to build 
# changes required
terraform plan

# apply creation iac code
# create resources
terraform apply -auto-approve

# fetch kubernetes cluster info
gcloud container clusters get-credentials silver-charmer-243611-gke --region us-central1

# remove resources [rg]
# destroy resources
terraform destroy -auto-approve
```