```shell
# application
ingestion-data-stores

# cli
python3.9 cli.py 'ysql'
python3.9 cli.py 'ycql'

# get cluster context 
kubectx aks-owshq-dev

# cron jobs
k apply -f crj_ysql.yaml -n app
k apply -f crj_ycql.yaml -n app

# yugabytedb ui
20.75.14.5:7000

# postgres
20.96.160.13:5433

# cassandra
20.96.160.13:9042
```

```sql
-- https://docs.yugabyte.com/latest/explore/query-1-performance/explain-analyze/
-- https://docs.yugabyte.com/latest/api/ysql/datatypes/type_json/create-indexes-check-constraints/#indexes-on-jsonb-columns
-- https://docs.yugabyte.com/latest/api/ysql/the-sql-language/statements/ddl_create_index/#where-clause
-- https://docs.yugabyte.com/latest/explore/query-1-performance/pg-hint-plan/
-- https://blog.yugabyte.com/how-a-distributed-sql-database-boosts-secondary-index-queries-with-index-only-scan/

-- query data
SELECT *
FROM public.user;

SELECT *
FROM public.subscription;

SELECT *
FROM public.device;

-- count rows
SELECT COUNT(*)
FROM public.user;

SELECT COUNT(*)
FROM public.subscription;

SELECT COUNT(*)
FROM public.device;

-- drop and create table
DROP TABLE IF EXISTS public."users";
CREATE TABLE public."users"
(
    id bigint,
    uid varchar(500),
    first_name varchar(500),
    last_name varchar(500),
    username varchar(500),
    email varchar(500),
    gender varchar(500),
    date_of_birth varchar(500),
    address jsonb,
    subscription jsonb,
    user_id bigint,
    dt_current_timestamp timestamp
);

-- insert new data into table
INSERT INTO public.users
SELECT id,uid,first_name,last_name,username,email,gender,date_of_birth,CAST(address AS jsonb),CAST(subscription AS jsonb),user_id,dt_current_timestamp
FROM public.user;

-- count rows
SELECT COUNT(*)
FROM public."users";

-- query data
SELECT *
FROM public."users";

-- using json function
SELECT jsonb_pretty(subscription) AS subscription,
       jsonb_pretty(address) AS address
FROM public."users"
WHERE gender = 'Male';

-- query inside of json format = postgres’s [cost-based optimizer]
-- seq scan = read all rows from all tables (nodes) used to read the entire table
-- index scan = accesses only specific tablet and range used to read specific parts (lookup)

EXPLAIN (ANALYZE, VERBOSE) SELECT (subscription->>'plan') AS plan,
       COUNT(*) AS amount
FROM public."users"
WHERE subscription->>'plan' IN ('Basic','Bronze','Business','Diamond','Essential')
GROUP BY (subscription->>'plan')
LIMIT 5;

/*
Limit  (cost=116.25..116.31 rows=5 width=40) (actual time=546.023..546.027 rows=5 loops=1)
"  Output: ((subscription ->> 'plan'::text)), (count(*))"
  ->  HashAggregate  (cost=116.25..118.75 rows=200 width=40) (actual time=546.020..546.022 rows=5 loops=1)
"        Output: ((subscription ->> 'plan'::text)), count(*)"
        Group Key: (users.subscription ->> 'plan'::text)
        ->  Seq Scan on public.users  (cost=0.00..111.25 rows=1000 width=32) (actual time=9.796..540.347 rows=24097 loops=1)
              Output: (subscription ->> 'plan'::text)
"              Filter: ((users.subscription ->> 'plan'::text) = ANY ('{Basic,Bronze,Business,Diamond,Essential}'::text[]))"
              Rows Removed by Filter: 43603
Planning Time: 1.255 ms
Execution Time: 548.251 ms
*/

-- index on jsonb column
DROP INDEX idx_subscription_plan_jsonb;
CREATE INDEX idx_subscription_plan_jsonb
ON public."users" ((subscription->>'plan') ASC);

/*
Limit  (cost=0.00..2.74 rows=5 width=40) (actual time=71.196..394.171 rows=5 loops=1)
"  Output: ((subscription ->> 'plan'::text)), (count(*))"
  ->  GroupAggregate  (cost=0.00..5.49 rows=10 width=40) (actual time=71.193..394.162 rows=5 loops=1)
"        Output: ((subscription ->> 'plan'::text)), count(*)"
        Group Key: (users.subscription ->> 'plan'::text)
        ->  Index Scan using idx_subscription_plan_jsonb on public.users  (cost=0.00..5.31 rows=10 width=32) (actual time=18.318..390.830 rows=24097 loops=1)
              Output: (subscription ->> 'plan'::text)
"              Index Cond: ((users.subscription ->> 'plan'::text) = ANY ('{Basic,Bronze,Business,Diamond,Essential}'::text[]))"
Planning Time: 5.642 ms
Execution Time: 395.059 ms
*/

-- query subscription (plan)
SELECT (subscription->>'plan') AS plan,
       COUNT(*) AS amount
FROM public."users"
WHERE subscription->>'plan' IN ('Basic','Bronze','Business','Diamond','Essential')
GROUP BY (subscription->>'plan')
LIMIT 5;

-- set query hint plan
SET pg_hint_plan.enable_hint = ON;
SET pg_hint_plan.debug_print TO ON;
SET client_min_messages TO LOG;

--//--
EXPLAIN (ANALYZE, VERBOSE) SELECT (subscription->>'plan') AS plan,
       subscription.payment_method,
       COUNT(*) AS amount
FROM public."users" AS users
INNER JOIN public."subscription" AS subscription
ON users.id = subscription.user_id
WHERE subscription->>'plan' IN ('Diamond')
GROUP BY (subscription->>'plan'), subscription.payment_method
LIMIT 5;

/*
Limit  (cost=111.16..111.27 rows=5 width=72) (actual time=999.495..1002.457 rows=5 loops=1)
"  Output: ((users.subscription ->> 'plan'::text)), subscription.payment_method, (count(*))"
  ->  GroupAggregate  (cost=111.16..112.29 rows=50 width=72) (actual time=999.494..1002.449 rows=5 loops=1)
"        Output: ((users.subscription ->> 'plan'::text)), subscription.payment_method, count(*)"
"        Group Key: ((users.subscription ->> 'plan'::text)), subscription.payment_method"
        ->  Sort  (cost=111.16..111.29 rows=50 width=64) (actual time=998.753..999.901 rows=17563 loops=1)
"              Output: ((users.subscription ->> 'plan'::text)), subscription.payment_method"
              Sort Key: subscription.payment_method
              Sort Method: quicksort  Memory: 3890kB
              ->  Hash Join  (cost=5.38..109.75 rows=50 width=64) (actual time=68.923..983.344 rows=41837 loops=1)
"                    Output: (users.subscription ->> 'plan'::text), subscription.payment_method"
                    Hash Cond: (subscription.user_id = users.id)
                    ->  Seq Scan on public.subscription  (cost=0.00..100.00 rows=1000 width=40) (actual time=13.854..894.682 rows=86300 loops=1)
"                          Output: subscription.id, subscription.uid, subscription.plan, subscription.status, subscription.payment_method, subscription.subscription_term, subscription.payment_term, subscription.user_id, subscription.dt_current_timestamp"
                    ->  Hash  (cost=5.25..5.25 rows=10 width=40) (actual time=55.031..55.031 rows=4857 loops=1)
"                          Output: users.subscription, users.id"
                          Buckets: 8192 (originally 1024)  Batches: 1 (originally 1)  Memory Usage: 739kB
                          ->  Index Scan using idx_subscription_plan_jsonb on public.users  (cost=0.00..5.25 rows=10 width=40) (actual time=13.067..53.816 rows=4857 loops=1)
"                                Output: users.subscription, users.id"
                                Index Cond: ((users.subscription ->> 'plan'::text) = 'Diamond'::text)
Planning Time: 0.134 ms
Execution Time: 1003.459 ms
*/

SET pg_hint_plan.enable_hint = OFF;
--//--
```

```sql
SELECT *
FROM owshq.user;

SELECT COUNT(*)
FROM owshq.user;

SELECT gender
FROM owshq.user
GROUP BY gender;

EXPLAIN SELECT gender
FROM owshq.user
GROUP BY gender;
```