### Working with KafkaConnect Cluster on Kubernetes for Source and Sink Pipelines

##### Business needs:

* Move data from different databases for another technologies
* ingest of data inside our data lake [MinIO]

##### Use-cases:

HR profiles:
* Candidate information
* Companies information

E-commerce evaluation
* commerce website information


##### Datasources:

* SQL server
* MySQL
* MongoDB
* Postgres4


### apache kafka on kubernetes [strimzi]
```sh
# alias k=kubectl

# get strimzi information
k get strimzi

# list kafka connectors
k get kafkaconnectors

# list topic kafka cmds

kubectl exec edh-kafka-0 -c kafka -i -t -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```


### enable CDC SQL server

```sh
USE OwsHQ  
GO  
EXEC sys.sp_cdc_enable_db  
GO  


USE Owshq
GO  
EXEC sys.sp_cdc_enable_table  
@source_schema = N'dbo',  
@source_name   = N'credit_card',  
@role_name     = NULL
GO  

USE Owshq
GO  
EXEC sys.sp_cdc_enable_table  
@source_schema = N'dbo',  
@source_name   = N'subscription',  
@role_name     = NULL
GO  

USE Owshq
GO  
EXEC sys.sp_cdc_enable_table  
@source_schema = N'dbo',  
@source_name   = N'company',  
@role_name     = NULL
GO  


```
