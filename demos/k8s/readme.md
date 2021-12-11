https://kubernetes.io/docs/reference/kubectl/cheatsheet/
https://kubernetes.io/docs/tutorials/kubernetes-basics/

```shell
# kubernetes cli
kubectl
kubectl version

# verify configured clusters 
# your context
kubectl config view
$HOME/.kube/config

# get cluster context
kubectx 
kubectx aks-owshq-dev
kubectl cluster-info

# worker nodes
k get nodes
k top nodes
kubectl get events

# set namespace
kubens
kubens app

# create a [pod]  
k apply -f /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/demos/k8s/pod.yaml
k get pods -o wide
k get pods busybox
k describe pod busybox
k exec busybox -it -- /bin/sh
k logs busybox

# create a [daemon set]
# current = 7 node cluster
k apply -f /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/demos/k8s/daemonset.yaml
k get daemonset
k describe daemonset fluent-bit
k get pods 

# create a [deployment/replica set]
k apply -f /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/demos/k8s/deployment.yaml
k get deployment
k get replicaset
k describe pod busybox-5bc85cc8d9-6l5ww

# create a [statefulset]
k apply -f /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/demos/k8s/statefulset.yaml
k get statefulset
k describe statefulset web
k get pods -w -l app=nginx
k logs web-0 
k get pvc -l app=nginx

# create a [job]
k create job job-busybox --image=busybox -- echo "busybox" 
k describe job job-busybox
k get job job-busybox --output=yaml

# create a [cronjob]
k create cronjob cronjob-busybox --image=busybox --schedule="*/1 * * * *" -- echo "busybox"  
k describe cronjob cronjob-busybox
k get cronjob cronjob-busybox --output=yaml

# [service] for stateful application
k apply -f /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/demos/k8s/service.yaml

# housekeeping
k delete pod busybox
k delete daemonset fluent-bit
k delete deployment busybox
k delete statefulset web
k delete job job-busybox
k delete cronjob cronjob-busybox
```