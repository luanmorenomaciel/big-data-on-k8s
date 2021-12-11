```sh
# connect into k8s cluster
kubectx aks-owshq-dev

# create namespaces
k create namespace orchestrator
k create namespace database
k create namespace ingestion
k create namespace processing
k create namespace datastore
k create namespace deepstorage
k create namespace tracing
k create namespace logging
k create namespace monitoring
k create namespace viz
k create namespace cicd
k create namespace app
k create namespace cost
k create namespace misc
k create namespace dataops
k create namespace gateway

# add & update helm list repos
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

# install crd's [custom resources]
# argo-cd
# https://artifacthub.io/packages/helm/argo/argo-cd
# https://github.com/argoproj/argo-helm
helm install argocd argo/argo-cd --namespace cicd --version 3.26.8

# install argo-cd [gitops]
# create a load balancer
k patch svc argocd-server -n cicd -p '{"spec": {"type": "LoadBalancer"}}'

# retrieve load balancer ip
# load balancer = 20.69.223.133
kubens cicd && kubectl get services -l app.kubernetes.io/name=argocd-server,app.kubernetes.io/instance=argocd -o jsonpath="{.items[0].status.loadBalancer.ingress[0].ip}"

# get password to log into argocd portal
# argocd login 20.69.223.133 --username admin --password PafATjllzVYkv6tC --insecure
ARGOCD_LB="20.69.223.133"
kubens cicd && k get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d | xargs -t -I {} argocd login $ARGOCD_LB --username admin --password {} --insecure

# create cluster role binding for admin user [sa]
k create clusterrolebinding cluster-admin-binding --clusterrole=cluster-admin --user=system:serviceaccount:cicd:argocd-application-controller -n cicd

# register cluster
CLUSTER="aks-owshq-dev"
argocd cluster add $CLUSTER --in-cluster

# add repo into argo-cd repositories
REPOSITORY="https://bitbucket.org/owshq/big-data-on-k8s.git"
argocd repo add $REPOSITORY --username [NAME] --password [PWD] --port-forward
```

```sh
# default location
/Users/luanmorenomaciel/BitBucket/big-data-on-k8s

# helm
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
helm repo add strimzi https://strimzi.io/charts/
helm repo update

# strimzi
helm install kafka strimzi/strimzi-kafka-operator --namespace ingestion --version 0.26.0

# spark
helm install spark spark-operator/spark-operator --namespace processing --set image.tag=v1beta2-1.3.0-3.1.1

# config maps
k apply -f repository/yamls/ingestion/metrics/kafka-metrics-config.yaml
k apply -f repository/yamls/ingestion/metrics/zookeeper-metrics-config.yaml
k apply -f repository/yamls/ingestion/metrics/connect-metrics-config.yaml
k apply -f repository/yamls/ingestion/metrics/cruise-control-metrics-config.yaml

# ingestion
k apply -f repository/app-manifests/ingestion/kafka-broker.yaml
k apply -f repository/app-manifests/ingestion/schema-registry.yaml
k apply -f repository/app-manifests/ingestion/kafka-connect.yaml
k apply -f repository/app-manifests/ingestion/cruise-control.yaml
k apply -f repository/app-manifests/ingestion/kafka-connectors.yaml

# databases
k apply -f repository/app-manifests/database/mssql.yaml
k apply -f repository/app-manifests/database/mysql.yaml
k apply -f repository/app-manifests/database/postgres.yaml
k apply -f repository/app-manifests/database/mongodb.yaml
k apply -f repository/app-manifests/database/yugabytedb.yaml

# deep storage
k apply -f repository/app-manifests/deepstorage/minio-operator.yaml

# datastore
k apply -f repository/app-manifests/datastore/pinot.yaml

# processing
k apply -f repository/app-manifests/processing/ksqldb.yaml
k apply -f repository/app-manifests/processing/trino.yaml

# orchestrator
k apply -f repository/app-manifests/orchestrator/airflow.yaml

# data ops
k apply -f repository/app-manifests/lenses/lenses.yaml

# monitoring
k apply -f repository/app-manifests/monitoring/prometheus-alertmanager-grafana-botkube.yaml

# logging
k apply -f repository/app-manifests/logging/elasticsearch.yaml
k apply -f repository/app-manifests/logging/filebeat.yaml
k apply -f repository/app-manifests/logging/kibana.yaml

# cost
k apply -f repository/app-manifests/cost/kubecost.yaml

# load balancer
k apply -f repository/app-manifests/misc/load-balancers-svc.yaml

# deployed apps
k get applications -n cicd

# housekeeping
helm delete argocd -n cicd
helm delete kafka -n ingestion
helm delete spark -n processing
```
