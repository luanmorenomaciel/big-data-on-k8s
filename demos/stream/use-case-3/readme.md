### Using a OLAP System for Analytical Queries

##### Business needs:

* Query events coming from kafka with low latency, and columnar storage improvement.

##### Use-cases:


Financial

* credit card information
* subscription information
* device information


HR profiles:
* Candidate information
* Companies information


Car applications
* Uber information
* Lift information

##### Datasources:

* Apache Kafka


### Low latency query data warehouse [apache pinot]
```sh
# alias k=kubectl

# change namespace context
kubens datastore

# list pods
k get pods

# list services
k get svc

# external UI = http://20.85.35.96:9001/#/

# get topics to be ingested in Apache pinot
k get kafkatopics -n ingestion

# output-ksqldb-stream-pr-company-employee-analysis-avro
# output-ksqldb-stream-pr-credit-card-subscription-analysis-avro
# output-ksqldb-tb-pr-credit-card-count-avro
# src-app-musics-json



##### Deploy tasks

# copy files from repository to [container] to build spec

# tables and schemas
k cp demos/stream/use-case-3/src-app-users-json/realtime_src_app_users_avro.json datastore/pinot-controller-0:/opt/pinot
k cp demos/stream/use-case-3/src-app-users-json/sch_src_app_users_avro.json datastore/pinot-controller-0:/opt/pinot

k cp demos/stream/use-case-3/output-ksqldb-stream-pr-company-employee-analysis-avro/realtime_output_ksqldb_stream_pr_company_employee_analysis_avro.json datastore/pinot-controller-0:/opt/pinot
k cp demos/stream/use-case-3/output-ksqldb-stream-pr-company-employee-analysis-avro/sch_output_ksqldb_stream_pr_company_employee_analysis_avro.json datastore/pinot-controller-0:/opt/pinot

k cp demos/stream/use-case-3/output-ksqldb-stream-pr-credit-card-subscription-analysis-avro/realtime_output_ksqldb_stream_pr_credit_card_subscription_analysis_avro.json datastore/pinot-controller-0:/opt/pinot
k cp demos/stream/use-case-3/output-ksqldb-stream-pr-credit-card-subscription-analysis-avro/sch_output_ksqldb_stream_pr_credit_card_subscription_analysis_avro.json datastore/pinot-controller-0:/opt/pinot


k cp demos/stream/use-case-3/output-faust-enriched-rides/realtime_output_faust_enriched_rides_events_training.json datastore/pinot-controller-0:/opt/pinot
k cp demos/stream/use-case-3/output-faust-enriched-rides/sch_output_faust_enriched_rides_training.json datastore/pinot-controller-0:/opt/pinot

# access the admin tools logging into [controller] container
kubens datastore
k exec pinot-controller-0 -i -t -- bash
/opt/pinot

# execute inside the container
JAVA_OPTS=""



# create table kafka users
bin/pinot-admin.sh AddTable \
-schemaFile /opt/pinot/sch_src_app_users_avro.json \
-tableConfigFile /opt/pinot/realtime_src_app_users_avro.json \
-exec


# create table output company and employee analysis
bin/pinot-admin.sh AddTable \
-schemaFile /opt/pinot/sch_output_ksqldb_stream_pr_company_employee_analysis_avro.json \
-tableConfigFile /opt/pinot/realtime_output_ksqldb_stream_pr_company_employee_analysis_avro.json \
-exec

# create table output subscription and credit analysis
bin/pinot-admin.sh AddTable \
-schemaFile /opt/pinot/sch_output_ksqldb_stream_pr_credit_card_subscription_analysis_avro.json \
-tableConfigFile /opt/pinot/realtime_output_ksqldb_stream_pr_credit_card_subscription_analysis_avro.json \
-exec

# create table rides analytics
bin/pinot-admin.sh AddTable \
-schemaFile /opt/pinot/sch_output_faust_enriched_rides_training.json \
-tableConfigFile /opt/pinot/realtime_output_faust_enriched_rides_events_training.json \
-exec



# get tasks logs
cat pinotController.log

```




Queries


```sql



-- credit card query
select count(CREDIT_CARD_TYPE) qty_cards, CREDIT_CARD_TYPE  from realtime_output_ksqldb_stream_pr_credit_card_subscription_analysis_avro
group by CREDIT_CARD_TYPE
having qty_cards >=1020
order by 1 desc


--uber lift query

select car_type, count(car_type) from realtime_output_faust_enriched_rides_events
where city is not null
or gender is not null
or model_type is not null
or dynamic_fare is not null
group by car_type



select count(city) ,city
from realtime_output_faust_enriched_rides_events
where city like 'a%'
OR city like 'b%'
OR city like 'c%'
OR city like 'd%'
OR city like 'e%'
OR city like 'f%'
OR city like 'g%'
OR city like 'h%'
OR city like 'i%'
OR city like 'j%'
OR city like 'l%'
OR city like 'm%'
OR city like 'n%'
OR city like 'k%'
OR city like 'o%'
OR city like 'p%'
OR city like 'q%'
OR city like 'r%'
OR city like 's%'
OR city like 't%'
OR city like 'u%'
OR city like 'v%'
OR city like 'y%'
OR city like 'z%'
group by city
order by count(city) desc


```
