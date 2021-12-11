### Orchestrating and Managing a Real-Time Pipelines with Lenses


##### Queries
```sql

-- app-users
select * from src-app-users-avro

-- app-agents
select * from src-app-agent-avro

-- sql-credit-card
select * from src-sqlserver-credit-card-avro

-- sql-subscription
select * from src-sqlserver-subscription-avro

-- join query
select a.email,CONCAT(u.first_name, ' ',u.last_name ) as full_name, u.job, u.city,a.platform from src-app-users-avro as u join src-app-agent-avro as a on u.user_id = a.user_id

-- query join from sql processor
select * from output_st_app_join_users_agents_events

SELECT
j.email,
j.full_name,
j.job,
j.city,
cc.credit_card_number,
cc.credit_card_type
from output_join_users_agents_events as j join src-app-credit-card-avro as cc on j.user_id = cc.user_id


```

##### Lenses connector

```sh
# sink connector yugabyteDB

connector.class=io.confluent.connect.jdbc.JdbcSinkConnector
table.name.format=mssql_subscription
topics=src-sqlserver-subscription-avro
tasks.max=2
batch.size=1500
connection.attempts=2
value.converter.schema.registry.url=http://schema-registry-cp-schema-registry:8081
delete.enabled=true
auto.evolve=true
name=sink-yugabytedb-ysql-sqlserver-subscription-avro-363e0214
auto.create=true
connection.url=jdbc:postgresql://yb-tservers.database.svc.cluster.local:5433/owshq?user=yugabyte&password=yugabyte
value.converter=io.confluent.connect.avro.AvroConverter
insert.mode=upsert
key.converter=io.confluent.connect.avro.AvroConverter
key.converter.schema.registry.url=http://schema-registry-cp-schema-registry:8081
pk.mode=record_key
pk.fields=incr


# source connector yugabyteDB
connector.class=io.confluent.connect.jdbc.JdbcSourceConnector
incrementing.column.name=incr
transforms.createKey.type=org.apache.kafka.connect.transforms.ValueToKey
connection.password=yugabyte
tasks.max=2
transforms.InsertTopic.type=org.apache.kafka.connect.transforms.InsertField$Value
transforms=createKey,extractInt,InsertTopic,InsertSourceDetails
transforms.InsertTopic.topic.field=messagetopic
mode=incrementing
topic.prefix=src-yugabyte-mssql-subscription-avro
transforms.createKey.fields=incr
value.converter=io.confluent.connect.avro.AvroConverter
key.converter=io.confluent.connect.avro.AvroConverter
transforms.InsertSourceDetails.static.field=messagesource
validate.non.null=false
query=SELECT * FROM public.mssql_subscription
connection.attempts=2
transforms.extractInt.type=org.apache.kafka.connect.transforms.ExtractField$Key
value.converter.schema.registry.url=http://schema-registry-cp-schema-registry:8081
transforms.InsertSourceDetails.type=org.apache.kafka.connect.transforms.InsertField$Value
transforms.extractInt.field=incr
connection.user=yugabyte
name=ingest-src-yugabyte-mssql-subscription-avro-85bde6fd
connection.url=jdbc:postgresql://yb-tservers.database.svc.cluster.local:5433/owshq
transforms.InsertSourceDetails.static.value=yugabytedb
key.converter.schema.registry.url=http://schema-registry-cp-schema-registry:8081


```


##### SQL processors

```sh

# object name = movie_rating_title_stream
# processing of movies and titles

SET defaults.topic.autocreate=true;
SET commit.interval.ms='1000';
SET enable.auto.commit=false;
SET auto.offset.reset='earliest';


INSERT INTO output_stream_lenses_processor_movies_titles_ratings
SELECT STREAM
  original_title,
  overview,
  release_date
FROM src-app-movies-ratings-json as ratings JOIN src-app-movies-titles-json as titles
   ON ratings.user_id = titles.user_id WITHIN 2180h
   where rating <=3



# object name = count_music_popularity
# aggregation count music popularity
SET defaults.topic.autocreate=true;
SET commit.interval.ms='1000';
SET enable.auto.commit=false;
SET auto.offset.reset='earliest';

INSERT INTO output_stream_lenses_music_popularity
SELECT STREAM
	   popularity
      ,count(popularity) as qty_popularity
FROM src-app-musics-avro
WINDOW BY TUMBLE 7d
GROUP BY popularity


# object name =
# join between computer events and commerce events


#######  computer SQL processor stream
SET defaults.topic.autocreate=true;
SET commit.interval.ms='1000';
SET enable.auto.commit=false;
SET auto.offset.reset='earliest';

INSERT INTO stream_lenses_commerce_events
  SELECT STREAM
  _key as business_key,
  after.incr,
  after.price,
  after.promo_code,
  after.price_string
  FROM owshq.mysql.owshq.commerce
  where after.incr is not null;


#######  computer SQL processor stream
SET defaults.topic.autocreate=true;
SET commit.interval.ms='1000';
SET enable.auto.commit=false;
SET auto.offset.reset='earliest';

INSERT INTO stream_lenses_computer_events
  SELECT STREAM
  _key as business_key,
  after.incr,
  after.platform,
  after.type,
  after.os,
  after.stack
  FROM owshq.mysql.owshq.computer
  where after.incr is not null;


####### computer & commerce join
SET defaults.topic.autocreate=true;
SET commit.interval.ms='1000';
SET enable.auto.commit=false;
SET auto.offset.reset='earliest';

INSERT INTO output_st_lenses_join_commerce_computer_events
SELECT STREAM
platform,
type,
os,
stack,
price,
promo_code,
price_string
FROM stream_lenses_commerce_events as commerce JOIN stream_lenses_computer_events as computer
   ON commerce._key.incr = computer._key.incr
WITHIN 7d


# obejct_name = join_subscriptions
# join between 2 subscription sources
SET defaults.topic.autocreate=true;
SET commit.interval.ms='1000';
SET enable.auto.commit=false;
SET auto.offset.reset='earliest';

INSERT INTO output_lenses_join_subscription
SELECT STREAM
plan,
status,
payment_method,
subscription_term,
payment_term,
user_id
FROM src-yugabyte-mssql-subscription-avro as yugasub JOIN src-sqlserver-subscription-avro as mssqlsub
   ON yugasub._key = mssqlsub._key
WITHIN 7d



# object name = cte_agent_users_processing
# create join app users and agent


SET defaults.topic.autocreate=true;
SET commit.interval.ms='1000';
SET enable.auto.commit=false;
SET auto.offset.reset='earliest';

WITH agentStream AS (
  SELECT STREAM *
  FROM src-app-agent-avro
);

WITH usersStream AS (
  SELECT STREAM *
  FROM src-app-users-avro
);


WITH usersInfoStream AS (
SELECT STREAM
  a.email,
  CONCAT(u.first_name, ' ',u.last_name ) as full_name,
  u.job,
  u.city
  FROM usersStream AS u JOIN agentStream AS a
        on u.user_id = a.user_id
  WITHIN 7d
);


INSERT INTO output_lenses_join_users_agents_events
SELECT STREAM *
FROM usersInfoStream;



```
