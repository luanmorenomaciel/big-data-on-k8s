# import libraries
import os
from dotenv import load_dotenv

# get env
load_dotenv()

# load variables
kafka_client_id_json = os.getenv("KAFKA_CLIENT_ID_JSON")
kafka_client_id_avro = os.getenv("KAFKA_CLIENT_ID_AVRO")
kafka_bootstrap_server = os.getenv("KAFKA_BOOTSTRAP_SERVER")
kafka_ca_location = os.getenv("KAFKA_CA_LOCATION")
kafka_sasl_username = os.getenv("KAFKA_SASL_USERNAME")
kafka_sasl_password = os.getenv("KAFKA_SASL_PASSWORD")
schema_registry_server = os.getenv("KAFKA_SCHEMA_REGISTRY")


# [json] = producer config
def producer_settings_json(broker):

    json = {
        'client.id': kafka_client_id_json,
        'bootstrap.servers': broker,
        "batch.num.messages": 100000,
        "linger.ms": 1000
        }

    # return data
    return dict(json)


# [json] = producer config
def producer_settings_json_scram_sha_512(broker):

    json = {
        'client.id': kafka_client_id_json,
        'bootstrap.servers': broker,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'SCRAM-SHA-512',
        'ssl.ca.location': kafka_ca_location,
        'sasl.username': kafka_sasl_username,
        'sasl.password': kafka_sasl_password,
        'log.connection.close': True,
        }

    # return data
    return dict(json)


# [avro] = producer config
def producer_settings_avro(broker, schema_registry):

    avro = {
        "client.id": kafka_client_id_avro,
        "bootstrap.servers": broker,
        "schema.registry.url": schema_registry,
        "enable.idempotence": "true",
        "max.in.flight.requests.per.connection": 1,
        "retries": 100,
        "acks": "all",
        "batch.num.messages": 1000,
        "queue.buffering.max.ms": 100,
        "queue.buffering.max.messages": 1000,
        "linger.ms": 100
        }

    # return data
    return dict(avro)
