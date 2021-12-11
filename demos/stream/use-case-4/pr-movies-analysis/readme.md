```sh
# pyspark = v.3.1.1
# jars = /usr/local/lib/python3.9/site-packages/pyspark/jars
pyspark --version
```

```sh
# bash script ~ ingestion app
# src-app-users-json
# src-app-movies-titles-json

# retrieve topic info
k get kafkatopics
```

```sh
# change interpreter to local ~ 3.9
# verify settings
# 1 = batch = output-pyspark-counts-country-batch-json
# 2 = stream = output-pyspark-counts-genres-stream-json

# kafka
BROKER=40.65.243.238:9094

kcat -C -b $BROKER -t src-app-users-json -J -o end
kcat -C -b $BROKER -t src-app-movies-titles-json -J -o end

kcat -C -b $BROKER -t output-pyspark-counts-country-batch-json -J -o start
kcat -C -b $BROKER -t output-pyspark-counts-genres-stream-json -J -o start
```

```sh
# libraries to copy to jars folder
# local environment [copy]
# [jars loc] = /usr/local/lib/python3.9/site-packages/pyspark/jars 

# /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/demos/stream/use-case-4/pr-movies-analysis
# location of dockerfile [build image]
Dockerfile

# build image
# tag image
# push image to registry
docker build . -t etl-pr-movies-analysis:3.1.1
docker tag etl-pr-movies-analysis:3.1.1 owshq/etl-pr-movies-analysis:3.1.1
docker push owshq/etl-pr-movies-analysis:3.1.1

# select cluster to deploy 
kubectx aks-owshq-dev
k top nodes

# verify spark operator
kubens processing  
helm ls -n processing
kgp -n processing

# create & verify cluster role binding perms
k apply -f /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/demos/stream/use-case-4/pr-movies-analysis/crb-spark-operator-processing.yaml -n processing
k describe clusterrolebinding crb-spark-operator-processing

# deploy spark application [kubectl] for testing purposes
# [deploy application]
kubens processing
k apply -f /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/demos/stream/use-case-4/pr-movies-analysis/pr-movies-analysis-batch.yaml -n processing
k apply -f /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/demos/stream/use-case-4/pr-movies-analysis/pr-movies-analysis-stream.yaml -n processing

# get yaml detailed info
# verify submit
k get sparkapplications
k describe sparkapplication pr-movies-analysis-batch
k describe sparkapplication pr-movies-analysis-stream

# verify logs in real-time
# port forward to spark ui
POD=pr-movies-analysis-batch-driver
POD=pr-movies-analysis-batch-stream
k port-forward $POD 4040:4040

# housekeeping
k delete SparkApplication pr-movies-analysis-batch -n processing
k delete SparkApplication pr-movies-analysis-stream -n processing
k delete clusterrolebinding crb-spark-operator-processing
helm uninstall spark -n processing
```