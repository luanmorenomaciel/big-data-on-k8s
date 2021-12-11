#### Queries streams using KSQLDB

Query streams can be tricky, so don't forget to follow the documentation before start query all and everything
* ksqldb docs = https://docs.ksqldb.io/en/latest/how-to-guides/query-structured-data/

```sh

# connect into KSQLDB CLI
KSQLDB=ksqldb-server-65dd475564-j7mlw
k exec $KSQLDB -n processing -i -t -- bash ksql

# set latest or earliest offset read
SET 'auto.offset.reset' = 'earliest';
SET 'auto.offset.reset' = 'latest';

```

```sql
-- select * streams [only development - bad practice]
select * from ksql_stream_app_musics_avro emit changes limit 100;
select * from ksql_stream_app_users_avro emit changes limit 100;
select * from ksql_stream_mysql_cdc_device_avro emit changes limit 100;
select * from ksql_stream_sqlserver_cdc_company_avro emit changes limit 100;
select * from ksql_stream_sqlserver_cdc_credit_card_avro  emit changes limit 100;
select * from ksql_stream_sqlserver_jdbc_subscription_avro  emit changes limit 100;
select * from ksql_stream_app_users_json emit changes limit 100;
select * from ksql_stream_app_users_avro emit changes limit 100;

-- music avro
SELECT
ROWKEY->user_id AS "user_id_rowkey",
USER_ID,
GENRE,
ARTIST_NAME,
TRACK_NAME,
TRACK_ID,
POPULARITY,
DURATION_MS
FROM ksql_stream_app_musics_avro emit changes;

-- users avro
SELECT
ROWKEY->user_id AS "user_id_rowkey",
USER_ID,
UUID,
FIRST_NAME,
LAST_NAME,
DATE_BIRTH,
CITY,
COUNTRY,
COMPANY_NAME,
JOB,
PHONE_NUMBER,
LAST_ACCESS_TIME,
TIME_ZONE,
DT_CURRENT_TIMESTAMP
FROM ksql_stream_app_users_avro emit changes;

-- device avro
SELECT
ROWKEY->"INCR",
"AFTER"->"INCR" as "INCR_AFTER",
"BEFORE"->"INCR" as "INCR_BEFORE",
"AFTER"->"ID" as "ID_AFTER",
"BEFORE"->"ID" as "ID_BEFORE",
"AFTER"->"UID" as "UID_AFTER",
"BEFORE"->"UID" as "UID_BEFORE",
"AFTER"->"BUILD_NUMBER" as "BUILD_NUMBER_AFTER",
"BEFORE"->"BUILD_NUMBER" as "BUILD_NUMBER_BEFORE",
"AFTER"->"MANUFACTURER" as "MANUFACTURER_AFTER",
"BEFORE"->"MANUFACTURER" as "MANUFACTURER_BEFORE",
"AFTER"->"MODEL" as "MODEL_AFTER",
"BEFORE"->"MODEL" as "MODEL_BEFORE",
"AFTER"->"PLATFORM" as "PLATFORM_AFTER",
"BEFORE"->"PLATFORM" as "PLATFORM_BEFORE",
"AFTER"->"SERIAL_NUMBER" as "SERIAL_NUMBER_AFTER",
"BEFORE"->"SERIAL_NUMBER" as "SERIAL_NUMBER_BEFORE",
"AFTER"->"VERSION" as "VERSION_AFTER",
"BEFORE"->"VERSION" as "VERSION_BEFORE",
"AFTER"->"USER_ID" as "USER_ID_AFTER",
"BEFORE"->"USER_ID" as "USER_ID_BEFORE_AFTER",
"AFTER"->"DT_CURRENT_TIMESTAMP" as "DT_CURRENT_TIMESTAMP_AFTER",
"BEFORE"->"DT_CURRENT_TIMESTAMP" as "DT_CURRENT_TIMESTAMP_BEFORE",
"SOURCE"->"VERSION" as "VERSION",
"SOURCE"->"CONNECTOR" as "CONNECTOR",
"SOURCE"->"NAME" as "NAME",
"SOURCE"->"TS_MS" as "TS_MS_SOURCE",
"SOURCE"->"SNAPSHOT" as "SNAPSHOT",
"SOURCE"->"DB" as "DB",
"SOURCE"->"SEQUENCE" as "SEQUENCE",
"SOURCE"->"TABLE" as "TABLE",
"SOURCE"->"SERVER_ID" as "SERVER_ID",
"SOURCE"->"GTID" as "GTID",
"SOURCE"->"FILE" as "FILE",
"SOURCE"->"POS" as "POS",
"SOURCE"->"ROW" as "ROW",
"SOURCE"->"THREAD" as "THREAD",
"SOURCE"->"QUERY" as "QUERY",
"OP" as "OP",
"TS_MS" as "TS_MS",
"TRANSACTION"->"ID" as "TRANSACTION_ID",
"TRANSACTION"->"TOTAL_ORDER" as "TOTAL_ORDER",
"TRANSACTION"->"DATA_COLLECTION_ORDER" as "DATA_COLLECTION_ORDER"
FROM ksql_stream_mysql_cdc_device_avro emit changes limit 10;



-- select with after events [newest] insert cases
SELECT
ROWKEY->"INCR" as "INCR_ROWKEY",
"AFTER"->"INCR" as "INCR_VALUE",
"AFTER"->"ID" as "ID",
"AFTER"->"UID" as "UID",
"AFTER"->"BUILD_NUMBER" as "BUILD_NUMBER",
"AFTER"->"MANUFACTURER" as "MANUFACTURER_",
"AFTER"->"MODEL" as "MODEL",
"AFTER"->"PLATFORM" as "PLATFORM",
"AFTER"->"SERIAL_NUMBER" as "SERIAL_NUMBER",
"AFTER"->"VERSION" as "VERSION",
"AFTER"->"USER_ID" as "USER_ID",
"AFTER"->"DT_CURRENT_TIMESTAMP" as "DT_CURRENT_TIMESTAMP",
"SOURCE"->"CONNECTOR" as "CONNECTOR",
"SOURCE"->"NAME" as "NAME",
"SOURCE"->"TS_MS" as "TS_MS_SOURCE"
FROM ksql_stream_mysql_cdc_device_avro emit changes limit 10;


-- select with before events [oldest] update and delete cases
SELECT
ROWKEY->"INCR" as "INCR_ROWKEY",
"BEFORE"->"INCR" as "INCR_VALUE",
"BEFORE"->"ID" as "ID",
"BEFORE"->"UID" as "UID",
"BEFORE"->"BUILD_NUMBER" as "BUILD_NUMBER",
"BEFORE"->"MANUFACTURER" as "MANUFACTURER_",
"BEFORE"->"MODEL" as "MODEL",
"BEFORE"->"PLATFORM" as "PLATFORM",
"BEFORE"->"SERIAL_NUMBER" as "SERIAL_NUMBER",
"BEFORE"->"VERSION" as "VERSION",
"BEFORE"->"USER_ID" as "USER_ID",
"BEFORE"->"DT_CURRENT_TIMESTAMP" as "DT_CURRENT_TIMESTAMP",
"SOURCE"->"CONNECTOR" as "CONNECTOR",
"SOURCE"->"NAME" as "NAME",
"SOURCE"->"TS_MS" as "TS_MS_SOURCE"
FROM ksql_stream_mysql_cdc_device_avro
WHERE "BEFORE"->"INCR" is not null
emit changes limit 10;


--company avro [unwrap example]
SELECT
ROWKEY->"INCR" AS "INCR_ROWKEY",                         
INCR,                          
ID,                          
UID,                            
BUSINESS_NAME,
SUFFIX,                 
INDUSTRY,                       
CATCH_PHRASE,                   
BUZZWORD,                       
BS_COMPANY_STATEMENT,           
EMPLOYEE_IDENTIFICATION_NUMBER,
DUNS_NUMBER,                    
LOGO,                           
TYPE,                          
PHONE_NUMBER,                   
FULL_ADDRESS,                   
LATITUDE,                       
LONGITUDE,                      
USER_ID,                        
DT_CURRENT_TIMESTAMP,
DT_CREATION,          
__OP AS "DML_OPE"                   
FROM ksql_stream_sqlserver_cdc_company_avro emit changes limit 100;


--credit card avro [transformation and processing]

SELECT  
ROWKEY->"INCR" AS "INCR_ROWKEY",
INCR,
ID,
UID,
MASK(CREDIT_CARD_NUMBER),
CREDIT_CARD_EXPIRY_DATE,
CREDIT_CARD_TYPE,
USER_ID,
DT_CURRENT_TIMESTAMP,
DT_CREATION
FROM ksql_stream_sqlserver_cdc_credit_card_avro  emit changes limit 10;


SELECT  
CREDIT_CARD_TYPE,
COUNT(CREDIT_CARD_TYPE) AS "QTY_CREDIT_CARD_TYPE"
FROM ksql_stream_sqlserver_cdc_credit_card_avro WINDOW SESSION (60 SECONDS)
GROUP BY CREDIT_CARD_TYPE
EMIT CHANGES;

-- subscription avro
SELECT
ROWKEY AS "INCR_ROWKEY",
INCR,
ID,
UID,
PLAN,
STATUS,
PAYMENT_METHOD,
SUBSCRIPTION_TERM,
PAYMENT_TERM,
USER_ID,
DT_CURRENT_TIMESTAMP,
DT_CREATION,
MESSAGETOPIC,
MESSAGESOURCE
FROM ksql_stream_sqlserver_jdbc_subscription_avro  emit changes limit 100;



--join STREAMS
SELECT
sub.ROWKEY AS "INCR_ROWKEY",
sub.INCR,
sub.ID,
sub.UID,
sub.PLAN,
sub.STATUS,
sub.PAYMENT_METHOD,
sub.SUBSCRIPTION_TERM,
sub.PAYMENT_TERM,
sub.USER_ID,
sub.DT_CURRENT_TIMESTAMP,
MASK(card.CREDIT_CARD_NUMBER),
card.CREDIT_CARD_EXPIRY_DATE,
card.CREDIT_CARD_TYPE
FROM ksql_stream_sqlserver_jdbc_subscription_avro AS SUB
INNER JOIN ksql_stream_sqlserver_cdc_credit_card_avro AS card WITHIN 1 DAY
ON sub."ROWKEY" = card."ROWKEY"->"INCR"
EMIT CHANGES LIMIT 100;


SELECT
"user_id",
"uuid",
"first_name",
"last_name",
"date_birth",
"city",
"country",
"job",
"phone_number",
"last_access_time",
"time_zone",   
"dt_current_timestampa"
FROM ksql_stream_app_users_json
EMIT CHANGES LIMIT 100;


```
