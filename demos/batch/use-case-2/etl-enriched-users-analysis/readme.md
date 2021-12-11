```sh
# install & upgrade minio cli client
brew install minio/stable/mc
brew upgrade minio/stable/mc

# minio web console
console = http://20.62.76.8:9090/
endpoint = 20.62.75.137
access_key = H4aQRS39OITgclWk
secret_key = wRozzyetjvRrVQS9qpIzFVnimQFm9CqW

# minio configuration
mc config host add minio http://20.62.75.137/ H4aQRS39OITgclWk wRozzyetjvRrVQS9qpIzFVnimQFm9CqW

# list info
mc ls minio
mc tree minio
```

```sh
# libraries to copy to jars folder
# local environment [copy]
# [jars loc] = /usr/local/lib/python3.9/site-packages/pyspark/jars 

# /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/demos/batch/use-case-2/etl-enriched-users-analysis
# app name = etl-enriched-users-analysis
# location of dockerfile [build image]
Dockerfile

# build image
# tag image
# push image to registry
docker build . -t etl-enriched-users-analysis:3.1.1
docker tag etl-enriched-users-analysis:3.1.1 owshq/etl-enriched-users-analysis:3.1.1
docker push owshq/etl-enriched-users-analysis:3.1.1

# select cluster to deploy 
kubectx aks-owshq-dev
k top nodes

# verify spark operator
kubens processing  
helm ls -n processing
kgp -n processing

# create & verify cluster role binding perms
k apply -f /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/demos/batch/use-case-2/etl-enriched-users-analysis/crb-spark-operator-processing.yaml -n processing
k describe clusterrolebinding crb-spark-operator-processing

# deploy spark application [kubectl] for testing purposes
# [deploy application]
kubens processing
k apply -f /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/demos/batch/use-case-2/etl-enriched-users-analysis/etl-enriched-users-analysis.yaml -n processing

# get yaml detailed info
# verify submit
k get sparkapplications
k get sparkapplications etl-enriched-users-analysis -o=yaml
k describe sparkapplication etl-enriched-users-analysis

# [schedule app]
k apply -f /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/demos/batch/use-case-2/etl-enriched-users-analysis/sch-etl-enriched-users-analysis.yaml -n processing
k get scheduledsparkapplication
k describe scheduledsparkapplication etl-enriched-users-analysis

# verify logs in real-time
# port forward to spark ui
POD=etl-enriched-users-analysis-driver
k port-forward $POD 4040:4040

# housekeeping
k delete SparkApplication etl-enriched-users-analysis -n processing
k delete Scheduledsparkapplication etl-enriched-users-analysis -n processing
k delete clusterrolebinding crb-spark-operator-processing
helm uninstall spark -n processing
```