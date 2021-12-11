#### Processing queries streams using KSQLDB

For processing streams we need can use query, let's work with functions and windowing understanding
* ksqldb docs = https://docs.ksqldb.io/en/latest/developer-guide/ksqldb-reference/scalar-functions/#mask
* ksqldb docs windowing = https://docs.ksqldb.io/en/latest/concepts/time-and-windows-in-ksqldb-queries/#tumbling-window
```sh

# connect into KSQLDB CLI
KSQLDB=ksqldb-server-65dd475564-j7mlw
k exec $KSQLDB -n processing -i -t -- bash ksql

# set latest or earliest offset read
SET 'auto.offset.reset' = 'earliest';
SET 'auto.offset.reset' = 'latest';

```

```sql

--******************--
-- Financial analysis
--******************--

-- create output stream
CREATE OR REPLACE STREAM output_ksqldb_stream_pr_credit_card_subscription_analysis_avro
WITH (KAFKA_TOPIC='output-ksqldb-stream-pr-credit-card-subscription-analysis-avro', PARTITIONS=16, VALUE_FORMAT='AVRO')
AS
SELECT
card."ROWKEY"->"INCR" as "business_key",
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
card.CREDIT_CARD_TYPE,
TIMESTAMPTOSTRING(card.ROWTIME, 'yyyy-MM-dd HH:mm:ss',  'America/Sao_Paulo') AS "processing_time"
FROM ksql_stream_sqlserver_jdbc_subscription_avro AS SUB
INNER JOIN ksql_stream_sqlserver_cdc_credit_card_avro AS card WITHIN 1 DAY
ON sub."ROWKEY" = card."ROWKEY"->"INCR"
PARTITION BY card."ROWKEY"->"INCR"
EMIT CHANGES;

-- create output table
CREATE OR REPLACE TABLE output_ksqldb_tb_pr_credit_card_count_avro
WITH (KAFKA_TOPIC='output-ksqldb-tb-pr-credit-card-count-avro', PARTITIONS=16, VALUE_FORMAT='AVRO')
AS
SELECT  
CREDIT_CARD_TYPE,
COUNT(CREDIT_CARD_TYPE) AS "QTY_CREDIT_CARD_TYPE"
FROM ksql_stream_sqlserver_cdc_credit_card_avro WINDOW TUMBLING (SIZE 1 HOUR)
GROUP BY CREDIT_CARD_TYPE
EMIT CHANGES;


--******************--
-- HR analysis
--******************--


CREATE OR REPLACE STREAM output_ksqldb_stream_pr_company_employee_analysis_avro
WITH (KAFKA_TOPIC='output-ksqldb-stream-pr-company-employee-analysis-avro', PARTITIONS=16, VALUE_FORMAT='AVRO')
AS
SELECT
user.USER_ID,
user.FIRST_NAME,
user.LAST_NAME,
user.DATE_BIRTH,
user.JOB,
user.DT_CURRENT_TIMESTAMP,
company.BUSINESS_NAME,        
company.INDUSTRY,                                         
company.EMPLOYEE_IDENTIFICATION_NUMBER,
TIMESTAMPTOSTRING(company.ROWTIME, 'yyyy-MM-dd HH:mm:ss',  'America/Sao_Paulo') AS "processing_time"
FROM ksql_stream_sqlserver_cdc_company_avro AS company
INNER JOIN ksql_stream_app_users_avro AS user WITHIN 2 DAY
ON CAST(company."USER_ID" AS INT) = user."USER_ID"
EMIT CHANGES;



```


Processing queries

```sql
-- queries new streams and table enriched
SELECT * FROM output_ksqldb_stream_pr_credit_card_subscription_analysis_avro EMIT CHANGES;
SELECT * FROM output_ksqldb_tb_pr_credit_card_count_avro  EMIT CHANGES;
SELECT * FROM output_ksqldb_stream_pr_company_employee_analysis_avro  EMIT CHANGES;
```

```sh
# Checking topics enriched
PRINT 'output-ksqldb-stream-pr-credit-card-subscription-analysis-avro' FROM BEGINNING;
PRINT 'output-ksqldb-tb-pr-credit-card-count-avro' FROM BEGINNING;
PRINT 'output-ksqldb-stream-pr-company-employee-analysis-avro' FROM BEGINNING;

```
