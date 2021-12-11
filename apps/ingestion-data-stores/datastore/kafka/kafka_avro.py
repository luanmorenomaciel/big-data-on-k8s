# import libraries
import random
from datastore.kafka import delivery_reports, producer_settings
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer


# producer function = [agent]
def avro_producer(broker, schema_registry, object_name, schema_key, schema_value, kafka_topic):

    # init producer using key & value [schema registry] integration
    producer = AvroProducer(
        producer_settings.producer_settings_avro(broker, schema_registry),
        default_key_schema=avro.loads(schema_key),
        default_value_schema=avro.loads(schema_value)
    )

    # get data to insert
    object_name.to_dict_events()

    # loop to insert data
    inserts = 0
    while inserts < 1:

        # instantiate new records, execute callbacks
        record = object_name

        try:
            # server on_delivery callbacks from previous asynchronous produce()
            producer.poll(0)

            # message passed to the delivery callback will already be serialized.
            # to aid in debugging we provide the original object to the delivery callback.
            producer.produce(
                topic=kafka_topic,
                key={'user_id': record.user_id},
                value=record.to_dict_events(),
                callback=lambda err, msg, obj=record: delivery_reports.on_delivery_avro(err, msg, obj)
            )

        except BufferError:
            print("buffer full")
            producer.poll(0.1)

        except ValueError:
            print("invalid input")
            raise

        except KeyboardInterrupt:
            raise

        # increment values
        inserts += 1

    print("flushing records...")

    # buffer messages to send
    producer.flush()