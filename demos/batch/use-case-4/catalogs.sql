-- list all available catalogs
SHOW CATALOGS;

-- explore catalogs
-- uses the concept of tables
SHOW SCHEMAS FROM kafka;
SHOW TABLES FROM kafka.default;

SHOW SCHEMAS FROM minio;

SHOW SCHEMAS FROM pinot;
SHOW TABLES FROM pinot.default;

SHOW SCHEMAS FROM postgres;
SHOW TABLES FROM postgres.public;

SHOW SCHEMAS FROM sqlserver;
SHOW TABLES FROM sqlserver.dbo;

-- describe data
-- unified view
DESCRIBE kafka.default."src-app-users-json";
DESCRIBE kafka.default."src-app-agent-json";
DESCRIBE kafka.default."src-app-credit-card-json";
DESCRIBE kafka.default."src-app-musics-json";
DESCRIBE kafka.default."src-app-rides-json";

DESCRIBE postgres.public."user";
DESCRIBE postgres.public."device";
DESCRIBE postgres.public."subscription";

DESCRIBE sqlserver.dbo."bank";
DESCRIBE sqlserver.dbo."company";
DESCRIBE sqlserver.dbo."credit_card";
DESCRIBE sqlserver.dbo."subscription";

DESCRIBE pinot.default.realtime_output_ksqldb_stream_pr_company_employee_analysis;
DESCRIBE pinot.default.realtime_output_ksqldb_stream_pr_credit_card_subscription_analysis_avro;
DESCRIBE pinot.default.realtime_src_app_users_avro;

-- count rows
SELECT COUNT(*) FROM kafka.default."src-app-agent-json";
SELECT COUNT(*) FROM postgres.public."user"
SELECT COUNT(*) FROM sqlserver.dbo."subscription";
SELECT COUNT(*) FROM pinot.default."realtime_output_ksqldb_stream_pr_credit_card_subscription_analysis_avro";

-- read data
SELECT * FROM kafka.default."src-app-agent-json" LIMIT 10;
SELECT * FROM postgres.public."user" LIMIT 10;
SELECT * FROM sqlserver.dbo."subscription" LIMIT 10;
SELECT * FROM pinot.default."realtime_output_ksqldb_stream_pr_credit_card_subscription_analysis_avro" LIMIT 10;

-- cast message to retrieve column
-- using fn - json_extract_scalar
SELECT cast(json_extract_scalar(_message, '$.user_id') AS int) AS user_id
FROM kafka.default."src-app-agent-json" LIMIT 10;

-- retrieve music data
-- group data and order by
SELECT cast(json_extract_scalar(_message, '$.genre') AS varchar) AS user_id, COUNT(*) AS Q
FROM kafka.default."src-app-musics-json"
GROUP BY cast(json_extract_scalar(_message, '$.genre') AS varchar)
ORDER BY Q DESC
LIMIT 3;

/*
{
    "user_id": 582,
    "uuid": "8447e3ad-2ec4-43fb-a71c-e2693110c67d",
    "first_name": "Robert",
    "last_name": "Fowler",
    "date_birth": "1999-09-15",
    "city": "Lake Jason",
    "country": "Marshall Islands",
    "company_name": "Garner-Jones",
    "job": "Surveyor, hydrographic",
    "phone_number": "(384)978-0671x4523",
    "last_access_time": "1996-06-04T03:33:07",
    "time_zone": "Africa/Algiers",
    "dt_current_timestamp": "2021-07-28 10:54:26.389474"
}
*/

-- join between kafka and postgres schemas
SELECT cast(json_extract_scalar(users._message, '$.city') AS varchar) AS city,
       cast(json_extract_scalar(users._message, '$.country') AS varchar) AS country,
       device.model,
       device.dt_current_timestamp
FROM kafka.default."src-app-users-json" AS users
INNER JOIN postgres.public.device AS device
ON cast(json_extract_scalar(users._message, '$.user_id') AS int) = device.user_id
LIMIT 10;

-- group data using country column
SELECT cast(json_extract_scalar(users._message, '$.country') AS varchar) AS country,
       device.model,
       COUNT(*) AS amount
FROM kafka.default."src-app-users-json" AS users
INNER JOIN postgres.public.device AS device
ON cast(json_extract_scalar(users._message, '$.user_id') AS int) = device.user_id
GROUP BY cast(json_extract_scalar(users._message, '$.country') AS varchar), device.model
ORDER BY amount DESC
LIMIT 10;

-- retrieve [payment_term] info
SELECT cast(json_extract_scalar(users._message, '$.country') AS varchar) AS country,
       device.model,
       dt_an.payment_term,
       COUNT(*) AS amount
FROM kafka.default."src-app-users-json" AS users
INNER JOIN postgres.public.device AS device
ON cast(json_extract_scalar(users._message, '$.user_id') AS int) = device.user_id
INNER JOIN pinot.default."realtime_output_ksqldb_stream_pr_credit_card_subscription_analysis_avro" AS dt_an
ON CAST(dt_an.sub_user_id AS INT) = device.user_id
GROUP BY cast(json_extract_scalar(users._message, '$.country') AS varchar), device.model, dt_an.payment_term
ORDER BY amount DESC
LIMIT 10;