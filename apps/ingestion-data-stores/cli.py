# import libraries
import os
import sys
import argparse
import warnings
from dotenv import load_dotenv
from datastore.mssql.mssql import MSSQL
from datastore.postgres.postgres import Postgres
from datastore.mysql.mysql import MySQL
from schemas import sch_music_data, sch_agent, sch_users, sch_credit_card, sch_rides
from datastore.kafka.kafka_json import Kafka
from datastore.kafka.kafka_json_scram_sha_512 import KafkaScramSha512
from datastore.kafka.musics import MusicsAvro
from datastore.kafka.agent import AgentAvro
from datastore.kafka.users import UsersAvro
from datastore.kafka.log_compaction_users_avro import LogCompactionUsersAvro
from datastore.kafka.log_compaction_users_json import LogCompactionUsersJson
from datastore.kafka.credit_card import CreditCardAvro
from datastore.kafka.rides import RidesAvro
from objects.agent import Agent
from objects.credit_card import CreditCard
from objects.users import Users
from objects.musics import Musics
from objects.movies import Movies
from objects.rides import Rides
from datastore.mongodb.mongodb import MongoDB
from datastore.storage.stg_minio import MinioStorage
from datastore.yugabytedb.ysql import YSQL
from datastore.yugabytedb.ycql import YCQL

# warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# get env
load_dotenv()

# load variables
get_dt_rows = os.getenv("EVENTS")
kafka_broker = os.getenv("KAFKA_BOOTSTRAP_SERVER")
kafka_broker_ssl = os.getenv("KAFKA_BOOTSTRAP_SERVER_SSL")
confluent_cloud_kafka_broker = os.getenv("CONFLUENT_CLOUD_BOOTSTRAP_SERVER")
hdinsight_kafka_bootstrap_server = os.getenv("HDINSIGHT_KAFKA_BOOTSTRAP_SERVER")
users_json_topic = os.getenv("KAFKA_TOPIC_USERS_JSON")
agent_json_topic = os.getenv("KAFKA_TOPIC_AGENT_JSON")
credit_card_json_topic = os.getenv("KAFKA_TOPIC_CREDIT_CARD_JSON")
musics_json_topic = os.getenv("KAFKA_TOPIC_APP_MUSICS_JSON")
movies_titles_data_json_topic = os.getenv("KAFKA_TOPIC_APP_MOVIES_JSON")
movies_keywords_data_json_topic = os.getenv("KAFKA_TOPIC_APP_KEYWORDS_JSON")
movies_ratings_data_json_topic = os.getenv("KAFKA_TOPIC_APP_RATINGS_JSON")
rides_json_topic = os.getenv("KAFKA_TOPIC_APP_RIDES_JSON")
schema_registry_server = os.getenv("KAFKA_SCHEMA_REGISTRY")
kafka_topic_users_avro = os.getenv("KAFKA_TOPIC_USERS_AVRO")
kafka_topic_credit_card_avro = os.getenv("KAFKA_TOPIC_CREDIT_CARD_AVRO")
kafka_topic_agent_avro = os.getenv("KAFKA_TOPIC_AGENT_AVRO")
kafka_topic_musics_avro = os.getenv("KAFKA_TOPIC_APP_MUSICS_AVRO")
kafka_topic_movies_avro = os.getenv("KAFKA_TOPIC_APP_MOVIES_AVRO")
kafka_topic_rides_avro = os.getenv("KAFKA_TOPIC_APP_RIDES_AVRO")
kafka_topic_users_without_log_compaction_avro = os.getenv("KAFKA_TOPIC_USERS_WITHOUT_LOG_COMPACTION_AVRO")
kafka_topic_users_with_log_compaction_avro = os.getenv("KAFKA_TOPIC_USERS_WITH_LOG_COMPACTION_AVRO")
kafka_topic_users_without_log_compaction_json = os.getenv("KAFKA_TOPIC_USERS_WITHOUT_LOG_COMPACTION_JSON")
kafka_topic_users_with_log_compaction_json = os.getenv("KAFKA_TOPIC_USERS_WITH_LOG_COMPACTION_JSON")

# main
if __name__ == '__main__':

    # instantiate arg parse
    parser = argparse.ArgumentParser(description='python application for ingesting data & events into a data store')

    # add parameters to arg parse
    parser.add_argument('entity', type=str, choices=[
        'strimzi-users-json',
        'strimzi-users-json-ssl',
        'strimzi-users-without-log-compaction-json',
        'strimzi-users-with-log-compaction-json',
        'strimzi-agent-json',
        'strimzi-credit-card-json',
        'strimzi-musics-json',
        'strimzi-movies-titles-json',
        'strimzi-movies-keywords-json',
        'strimzi-movies-ratings-json',
        'strimzi-rides-json',
        'strimzi-users-avro',
        'strimzi-users-without-log-compaction-avro',
        'strimzi-users-with-log-compaction-avro',
        'strimzi-agent-avro',
        'strimzi-credit-card-avro',
        'strimzi-musics-avro',
        'strimzi-rides-avro',
        'mssql',
        'sqldb',
        'postgres',
        'ysql',
        'mysql',
        'mongodb',
        'ycql',
        'minio',
        'minio-movies',
    ], help='entities')

    # invoke help if null
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    # init variables
    users_object_name = Users().get_multiple_rows(get_dt_rows)
    agent_object_name = Agent().get_multiple_rows(get_dt_rows)
    credit_card_object_name = CreditCard().get_multiple_rows(get_dt_rows)
    musics_object_name = Musics().get_multiple_rows(get_dt_rows)
    movies_titles_object_name = Movies().get_movies(get_dt_rows)
    movies_keywords_object_name = Movies().get_keywords(get_dt_rows)
    movies_ratings_object_name = Movies().get_ratings(get_dt_rows)
    rides_object_name = Rides().get_multiple_rows(get_dt_rows)

    # apache kafka ~ strimzi
    if sys.argv[1] == 'strimzi-users-json':
        Kafka().json_producer(broker=kafka_broker, object_name=users_object_name, kafka_topic=users_json_topic)

    if sys.argv[1] == 'strimzi-users-json-ssl':
        KafkaScramSha512().json_producer(broker=kafka_broker_ssl, object_name=users_object_name, kafka_topic=users_json_topic)

    if sys.argv[1] == 'strimzi-users-without-log-compaction-json':
        LogCompactionUsersJson().json_producer(broker=kafka_broker, object_name=users_object_name, kafka_topic=kafka_topic_users_without_log_compaction_json)

    if sys.argv[1] == 'strimzi-users-with-log-compaction-json':
        LogCompactionUsersJson().json_producer(broker=kafka_broker, object_name=users_object_name, kafka_topic=kafka_topic_users_with_log_compaction_json)

    if sys.argv[1] == 'strimzi-agent-json':
        Kafka().json_producer(broker=kafka_broker, object_name=agent_object_name, kafka_topic=agent_json_topic)

    if sys.argv[1] == 'strimzi-credit-card-json':
        Kafka().json_producer(broker=kafka_broker, object_name=credit_card_object_name, kafka_topic=credit_card_json_topic)

    if sys.argv[1] == 'strimzi-musics-json':
        Kafka().json_producer(broker=kafka_broker, object_name=musics_object_name, kafka_topic=musics_json_topic)

    if sys.argv[1] == 'strimzi-movies-titles-json':
        Kafka().json_producer(broker=kafka_broker, object_name=movies_titles_object_name, kafka_topic=movies_titles_data_json_topic)

    if sys.argv[1] == 'strimzi-movies-keywords-json':
        Kafka().json_producer(broker=kafka_broker, object_name=movies_keywords_object_name, kafka_topic=movies_keywords_data_json_topic)

    if sys.argv[1] == 'strimzi-movies-ratings-json':
        Kafka().json_producer(broker=kafka_broker, object_name=movies_ratings_object_name, kafka_topic=movies_ratings_data_json_topic)

    if sys.argv[1] == 'strimzi-rides-json':
        Kafka().json_producer(broker=kafka_broker, object_name=rides_object_name, kafka_topic=rides_json_topic)

    if sys.argv[1] == 'strimzi-users-avro':
        schema_key = sch_users.key
        schema_value = sch_users.value
        UsersAvro().avro_producer(kafka_broker, schema_registry_server, schema_key, schema_value, kafka_topic_users_avro, get_dt_rows)

    if sys.argv[1] == 'strimzi-users-without-log-compaction-avro':
        schema_key = sch_users.key
        schema_value = sch_users.value
        LogCompactionUsersAvro().avro_producer(kafka_broker, schema_registry_server, schema_key, schema_value, kafka_topic_users_without_log_compaction_avro, get_dt_rows)

    if sys.argv[1] == 'strimzi-users-with-log-compaction-avro':
        schema_key = sch_users.key
        schema_value = sch_users.value
        LogCompactionUsersAvro().avro_producer(kafka_broker, schema_registry_server, schema_key, schema_value, kafka_topic_users_with_log_compaction_avro, get_dt_rows)

    if sys.argv[1] == 'strimzi-agent-avro':
        schema_key = sch_agent.key
        schema_value = sch_agent.value
        AgentAvro().avro_producer(kafka_broker, schema_registry_server, schema_key, schema_value, kafka_topic_agent_avro, get_dt_rows)

    if sys.argv[1] == 'strimzi-credit-card-avro':
        schema_key = sch_credit_card.key
        schema_value = sch_credit_card.value
        CreditCardAvro().avro_producer(kafka_broker, schema_registry_server, schema_key, schema_value, kafka_topic_credit_card_avro, get_dt_rows)

    if sys.argv[1] == 'strimzi-musics-avro':
        schema_key = sch_music_data.key
        schema_value = sch_music_data.value
        MusicsAvro().avro_producer(kafka_broker, schema_registry_server, schema_key, schema_value, kafka_topic_musics_avro, get_dt_rows)

    if sys.argv[1] == 'strimzi-rides-avro':
        schema_key = sch_rides.key
        schema_value = sch_rides.value
        RidesAvro().avro_producer(kafka_broker, schema_registry_server, schema_key, schema_value, kafka_topic_rides_avro, get_dt_rows)

    # relational databases
    if sys.argv[1] == 'mssql':
        MSSQL().insert_rows()

    if sys.argv[1] == 'postgres':
        Postgres().insert_rows()

    if sys.argv[1] == 'ysql':
        YSQL().insert_rows()

    if sys.argv[1] == 'mysql':
        MySQL().insert_rows()

    # nosql databases
    if sys.argv[1] == 'mongodb':
        MongoDB().insert_rows()

    if sys.argv[1] == 'ycql':
        YCQL().insert_rows()

    # object stores
    if sys.argv[1] == 'minio':
        MinioStorage().write_all()

    if sys.argv[1] == 'minio-movies':
        MinioStorage().write_movies_json()