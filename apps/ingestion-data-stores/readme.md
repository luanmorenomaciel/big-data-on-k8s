# Ingestion Data Stores Application
> * application that generates data

### application structure
```shell
# 1) [objects] are the entities that generates data
# 2) [datastore] main entry for ingesting data into the data stores
```

### generate data using [cli]
```sh
# main
# /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/apps/ingestion-data-stores
python3.9 cli.py

# apache kafka ~ strimzi
python3.9 cli.py 'strimzi-users-json'
python3.9 cli.py 'strimzi-users-without-log-compaction-json'
python3.9 cli.py 'strimzi-users-with-log-compaction-json'
python3.9 cli.py 'strimzi-agent-json'
python3.9 cli.py 'strimzi-credit-card-json'
python3.9 cli.py 'strimzi-musics-json'
python3.9 cli.py 'strimzi-movies-titles-json'
python3.9 cli.py 'strimzi-movies-keywords-json'
python3.9 cli.py 'strimzi-movies-ratings-json'
python3.9 cli.py 'strimzi-rides-json'
python3.9 cli.py 'strimzi-users-avro'
python3.9 cli.py 'strimzi-users-without-log-compaction-avro'
python3.9 cli.py 'strimzi-users-with-log-compaction-avro'
python3.9 cli.py 'strimzi-agent-avro'
python3.9 cli.py 'strimzi-credit-card-avro'
python3.9 cli.py 'strimzi-musics-avro'
python3.9 cli.py 'strimzi-rides-avro'

# relational databases
python3.9 cli.py 'mssql'
python3.9 cli.py 'postgres'
python3.9 cli.py 'ysql'
python3.9 cli.py 'mysql'

# nosql databases
python3.9 cli.py 'mongodb'
python3.9 cli.py 'ycql'

# object stores
python3.9 cli.py 'minio'
python3.9 cli.py 'minio-movies'
```

### verify apache kafka events
```sh
# set variables to read events
BROKER_IP=[IP]:9094
SCHEMA_REGISTRY=http://[IP]:8081

# apache kafka
kafkacat -C -b $BROKER_IP -t src-app-users-json -J -o end
kafkacat -C -b $BROKER_IP -t src-app-agent-json -J -o end
kafkacat -C -b $BROKER_IP -t src-app-credit-card-json -J -o end
kafkacat -C -b $BROKER_IP -t src-app-musics-json -J -o end
kafkacat -C -b $BROKER_IP -t src-app-movies-titles-data-json -J -o end
kafkacat -C -b $BROKER_IP -t src-app-movies-keywords-data-json -J -o end
kafkacat -C -b $BROKER_IP -t src-app-movies-ratings-data-json -J -o end
kafkacat -C -b $BROKER_IP -t src-app-rides-json -J -o end

kafkacat -C -b $BROKER_IP -t src-app-users-avro -s avro -r $SCHEMA_REGISTRY -o end -f 'key=%k, event=%s, partition=%p, offset=%o, timestamp=%T, key_length=%K, value_length=%S \n'
kafkacat -C -b $BROKER_IP -t src-app-agent-avro -s avro -r $SCHEMA_REGISTRY -o end -f 'key=%k, event=%s, partition=%p, offset=%o, timestamp=%T, key_length=%K, value_length=%S \n'
kafkacat -C -b $BROKER_IP -t src-app-credit-card-avro -s avro -r $SCHEMA_REGISTRY -o end -f 'key=%k, event=%s, partition=%p, offset=%o, timestamp=%T, key_length=%K, value_length=%S \n'
kafkacat -C -b $BROKER_IP -t src-app-musics-avro -s avro -r $SCHEMA_REGISTRY -o end -f 'key=%k, event=%s, partition=%p, offset=%o, timestamp=%T, key_length=%K, value_length=%S \n'
kafkacat -C -b $BROKER_IP -t src-app-rides-avro -s avro -r $SCHEMA_REGISTRY -o end -f 'key=%k, event=%s, partition=%p, offset=%o, timestamp=%T, key_length=%K, value_length=%S \n'
```

### dockerize app
```sh
# dockerize and push app to hub
docker build -f Dockerfile --tag ingestion-data-stores .
docker tag ingestion-data-stores owshq/ingestion-data-stores:0.1
docker push owshq/ingestion-data-stores:0.1

# access docker image
docker run -i -t ingestion-data-stores /bin/bash
docker run ingestion-data-stores python3.9 cli.py
```

### deploy app into k8s
```sh
# get cluster context
kubectx aks-owshq-dev

# cron jobs deployment
# /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/apps/ingestion-data-stores/cronjob
k apply -f crj_minio.yaml -n app
k apply -f crj_mssql.yaml -n app
k apply -f crj_mysql.yaml -n app
k apply -f crj_postgres.yaml -n app
k apply -f crj_ysql.yaml -n app
k apply -f crj_ycql.yaml -n app
k apply -f crj_mongodb.yaml -n app
k apply -f crj-strimzi-events.yaml -n app

# deploy app ~ deployment and svc
k apply -f deployment.yaml -n app
k apply -f service.yaml -n app

# deployment info
k describe deployment ingestion-data-stores-python-app

# list & describe pods
k get pods -l name=ingestion-data-stores-python-app
k describe pod -l name=ingestion-data-stores-python-app

# verify logs
k logs -l name=ingestion-data-stores-python-app -f

# remove deployment
k delete deployment ingestion-data-stores-python-app
k delete svc svc-lb-ingestion-data-stores-python-app
```
