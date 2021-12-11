```shell
# verify kafka connectivity
export KAFKA_BOOTSTRAP_SERVER = "kafka://40.65.243.238:9094"

# generate data into topic
# use ingestion app ~ batch_rides.bash
export TOPIC_SRC_APP_RIDES_JSON = "src-app-rides-json"
python3.9 cli.py 'strimzi-rides-json'

# init python faust application
faust -A src.app worker -l info

# enriched topic
output-faust-enriched-rides

# verify output topic
# kafka
BROKER=40.65.243.238:9094
kcat -C -b $BROKER -t output-faust-enriched-rides -J -o end
```

```shell
# login
# docker hub
docker login
https://hub.docker.com/repositories

# /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/demos/stream/use-case-5/pr-rides-analysis
Dockerfile

# build image
# tag image
# push image to registry
docker build . -t faust-enriched-rides:1.0
docker tag faust-enriched-rides:1.0 owshq/faust-enriched-rides:1.0
docker push owshq/faust-enriched-rides:1.0
```

```shell
# select cluster and namespace
kubectx aks-owshq-dev
kubens processing

# location of deployment file
# deploy processing faust app
/Users/luanmorenomaciel/BitBucket/big-data-on-k8s/demos/stream/use-case-5/pr-rides-analysis/deployment
kubectl apply -f /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/demos/stream/use-case-5/pr-rides-analysis/deployment/deployment.yaml -n processing

# deployment info
kubectl describe deployment faust-enriched-rides

# list & describe pods
kubectl get pods -l name=faust-enriched-rides
kubectl describe pod faust-enriched-rides-59cb697786-65xgt

# verify logs
kubectl logs -f faust-enriched-rides-59cb697786-65xgt

# remove deployment
k delete deployment faust-enriched-rides

# access container
kubectl exec -c faust-enriched-rides -it faust-enriched-rides-59cb697786-65xgt -- /bin/bash
```