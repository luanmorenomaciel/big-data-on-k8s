-- list catalogs
show catalogs;

-- create schema
-- minio = trino folder
CREATE SCHEMA minio.files;

-- drop table if exists
DROP TABLE minio.files.ds_gold_reviews_full_parquet;
DROP TABLE minio.files.ds_gold_reviews_full_orc;

-- creating table from [parquet] files
CREATE TABLE minio.files.ds_gold_reviews_full_parquet
(
  review_id VARCHAR,
  business_id VARCHAR,
  user_id VARCHAR,
  review_stars BIGINT,
  review_useful BIGINT,
  store_name VARCHAR,
  store_city VARCHAR,
  store_state VARCHAR,
  store_category VARCHAR,
  store_review_count BIGINT,
  store_stars DOUBLE,
  user_name VARCHAR,
  user_average_stars DOUBLE,
  user_importance VARCHAR
)
WITH
(
  external_location = 's3a://files/parquet/gold_reviews',
  format = 'parquet'
);

-- creating table from [orc] files
CREATE TABLE minio.files.ds_gold_reviews_full_orc
(
  review_id VARCHAR,
  business_id VARCHAR,
  user_id VARCHAR,
  review_stars BIGINT,
  review_useful BIGINT,
  store_name VARCHAR,
  store_city VARCHAR,
  store_state VARCHAR,
  store_category VARCHAR,
  store_review_count BIGINT,
  store_stars DOUBLE,
  user_name VARCHAR,
  user_average_stars DOUBLE,
  user_importance VARCHAR
)
WITH
(
  external_location = 's3a://files/orc/gold_reviews',
  format = 'orc'
);

-- describe data
DESCRIBE minio.files.ds_gold_reviews_full_parquet;
DESCRIBE minio.files.ds_gold_reviews_full_orc;

-- query table
-- 434.170.658
SELECT COUNT(*) AS Q FROM minio.files.ds_gold_reviews_full_parquet;
SELECT COUNT(*) AS Q FROM minio.files.ds_gold_reviews_full_orc;

-- parquet
-- [2021-12-05 11:00:50] 10 rows retrieved starting from 1 in 1 m 16 s 924 ms (execution: 1 s 749 ms, fetching: 1 m 15 s 175 ms)
SELECT store_name,
    store_city,
    COUNT(*) AS Q
FROM minio.files.ds_gold_reviews_full_parquet
WHERE user_importance = 'rockstar'
GROUP BY store_name, store_city
ORDER BY Q DESC
LIMIT 10;

-- orc
-- [2021-12-05 11:01:36] 10 rows retrieved starting from 1 in 26 s 785 ms (execution: 1 s 681 ms, fetching: 25 s 104 ms)
SELECT store_name,
    store_city,
    COUNT(*) AS Q
FROM minio.files.ds_gold_reviews_full_orc
WHERE user_importance = 'rockstar'
GROUP BY store_name, store_city
ORDER BY Q DESC
LIMIT 10;

-- ui
-- http://localhost:9000/ui/
