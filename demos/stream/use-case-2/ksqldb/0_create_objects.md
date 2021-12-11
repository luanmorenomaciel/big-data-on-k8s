#### create objects in ksqldb

For interact with kafka topics using ksqldb is needed create objects stream or tables to make queries.
* ksqldb docs = https://ksqldb.io/

```sh

# connect into KSQLDB CLI
KSQLDB=ksqldb-server-65dd475564-j7mlw
k exec $KSQLDB -n processing -i -t -- bash ksql

# set latest or earliest offset read
SET 'auto.offset.reset' = 'earliest';
SET 'auto.offset.reset' = 'latest';


# avro streams applications
CREATE OR REPLACE STREAM ksql_stream_app_musics_avro WITH (KAFKA_TOPIC='src-app-musics-avro', VALUE_FORMAT='AVRO', KEY_FORMAT = 'AVRO');
CREATE OR REPLACE STREAM ksql_stream_app_users_avro WITH (KAFKA_TOPIC='src-app-users-avro', VALUE_FORMAT='AVRO', KEY_FORMAT = 'AVRO');

# avro stream connect databases
CREATE OR REPLACE STREAM ksql_stream_mysql_cdc_device_avro WITH (KAFKA_TOPIC='owshq.mysql.owshq.device', VALUE_FORMAT='AVRO', KEY_FORMAT = 'AVRO');
CREATE OR REPLACE STREAM ksql_stream_sqlserver_cdc_company_avro WITH (KAFKA_TOPIC='owshq.sqlserver.dbo.company', VALUE_FORMAT='AVRO', KEY_FORMAT = 'AVRO');
CREATE OR REPLACE STREAM ksql_stream_sqlserver_cdc_credit_card_avro WITH (KAFKA_TOPIC='owshq.sqlserver.dbo.credit_card', VALUE_FORMAT='AVRO', KEY_FORMAT = 'AVRO');
CREATE OR REPLACE STREAM ksql_stream_sqlserver_jdbc_subscription_avro WITH (KAFKA_TOPIC='src-sqlserver-subscription-avro', VALUE_FORMAT='AVRO', KEY_FORMAT = 'AVRO');




# user json stream
CREATE OR REPLACE STREAM ksql_stream_app_users_json
(
    "user_id" INT,
    "uuid" VARCHAR,
    "first_name" VARCHAR,
    "last_name" VARCHAR,
    "date_birth" VARCHAR,
    "city" VARCHAR,
    "country" VARCHAR,
    "job" VARCHAR,
    "phone_number" VARCHAR,
    "last_access_time" VARCHAR,
    "time_zone" VARCHAR,
    "dt_current_timestamp" VARCHAR
)
WITH (KAFKA_TOPIC='src-app-users-json', VALUE_FORMAT='JSON');



```
