```shell
# using homebrew
brew install minikube

# kubernetes cluster information
* provider = Minikube
* version = 1.20.0
* type = macOS Big Sur
* cpus = 6
* memory = 12 GiB
* node count = 1

# setting minikube to use - docker for desktop
# configure cpu and memory
minikube config set driver docker
minikube config set cpus 2
minikube config set memory 6000

# apply changes
minikube delete
minikube start

# verify context
kubectx
kubectx minikube

# access kubernetes cluster
minikube tunnel
minikube dashboard

# verify nodes and pods
k get nodes
k get pods --all-namespaces

# check docker engine
docker ps

# housekeeping
minikube delete
```