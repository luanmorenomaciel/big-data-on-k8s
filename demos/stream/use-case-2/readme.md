### ETL in Real-Time using KSQLDB

##### Business needs:

* Query events coming from kafka
* Processing events using events - Aggregation, filtering, functions
* Join streams

##### Use-cases:


Financial

* credit card information
* subscription information
* device information


HR profiles:
* Candidate information
* Companies information


##### Datasources:

* Apache Kafka


### processing events using SQL [ksqldb]
```sh
# alias k=kubectl

# change namespace context
kubens processing

# list pods
k get pods

# connect into KSQLDB CLI
KSQLDB=ksqldb-server-65dd475564-j7mlw
k exec $KSQLDB -n processing -i -t -- bash ksql

# set latest offset read
SET 'auto.offset.reset' = 'earliest';
SET 'auto.offset.reset' = 'latest';

# show info
SHOW TOPICS;
SHOW STREAMS;
SHOW TABLES;
SHOW QUERIES;

# understand topics that will be needed

# user events
PRINT 'src-app-users-avro' FROM BEGINNING;

# credit card events
PRINT 'owshq.sqlserver.dbo.credit_card' FROM BEGINNING;

# subscriptions events
PRINT 'src-sqlserver-subscription-avro' FROM BEGINNING;

# company
PRINT 'owshq.sqlserver.dbo.company' FROM BEGINNING;


# devices events
PRINT 'owshq.mysql.owshq.device' FROM BEGINNING;


```
