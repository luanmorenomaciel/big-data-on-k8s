# import libraries
from datastore.kafka import delivery_reports, producer_settings
from objects.rides import Rides
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from random import seed

# incremental seed of 1
seed(1)


class RidesAvro(object):

    # use __slots__ to explicitly declare all schema members
    __slots__ = ["user_id", "time_stamp", "source", "destination", "distance", "price", "surge_multiplier", "id", "product_id", "name", "cab_type", "dt_current_timestamp"]

    # define init function based on the expected input
    def __init__(self, user_id=None, time_stamp=None, source=None, destination=None, distance=None, price=None, surge_multiplier=None, id=None, product_id=None, name=None, cab_type=None, dt_current_timestamp=None):

        self.user_id = user_id
        self.time_stamp = time_stamp
        self.source = source
        self.destination = destination
        self.distance = distance
        self.price = price
        self.surge_multiplier = surge_multiplier
        self.id = id
        self.product_id = product_id
        self.name = name
        self.cab_type = cab_type
        self.dt_current_timestamp = dt_current_timestamp

    # avro does not support code generation
    # need to provide dict representation
    def to_dict(self):

        return {
            "user_id": self.user_id,
            "time_stamp": self.time_stamp,
            "source": self.source,
            "destination": self.destination,
            "distance": self.distance,
            "price": self.price,
            "surge_multiplier": self.surge_multiplier,
            "id": self.id,
            "product_id": self.product_id,
            "name": self.name,
            "cab_type": self.cab_type,
            "dt_current_timestamp": self.dt_current_timestamp
        }

    @staticmethod
    def avro_producer(broker, schema_registry, schema_key, schema_value, kafka_topic, gen_dt_rows):

        # init producer using key & value [schema registry] integration
        producer = AvroProducer(
            producer_settings.producer_settings_avro(broker, schema_registry),
            default_key_schema=avro.loads(schema_key),
            default_value_schema=avro.loads(schema_value)
        )

        # get data to insert
        get_data = Rides().get_multiple_rows(gen_dt_rows)

        # loop to insert data
        inserts = 0
        while inserts < len(get_data):

            # instantiate new records, execute callbacks
            record = RidesAvro()

            try:

                # map columns and access using dict values
                record.user_id = get_data[inserts]['user_id']
                record.time_stamp = get_data[inserts]['time_stamp']
                record.source = get_data[inserts]['source']
                record.destination = get_data[inserts]['destination']
                record.distance = get_data[inserts]['distance']
                record.price = get_data[inserts]['price']
                record.surge_multiplier = get_data[inserts]['surge_multiplier']
                record.id = get_data[inserts]['id']
                record.product_id = get_data[inserts]['product_id']
                record.name = get_data[inserts]['name']
                record.cab_type = get_data[inserts]['cab_type']
                record.dt_current_timestamp = get_data[inserts]['dt_current_timestamp']

                # print(record.to_dict())

                # server on_delivery callbacks from previous asynchronous produce()
                producer.poll(0)

                # message passed to the delivery callback will already be serialized.
                # to aid in debugging we provide the original object to the delivery callback.
                producer.produce(
                    topic=kafka_topic,
                    key={'user_id': record.user_id},
                    value=record.to_dict(),
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
