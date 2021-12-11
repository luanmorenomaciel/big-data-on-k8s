# import libraries
from datastore.kafka import delivery_reports, producer_settings
from objects.credit_card import CreditCard
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from random import seed

# incremental seed of 1
seed(1)


class CreditCardAvro(object):

    # use __slots__ to explicitly declare all schema members
    __slots__ = ["uuid", "user_id", "provider", "number", "expire_data", "security_code", "dt_current_timestamp"]

    # define init function based on the expected input
    def __init__(self, uuid=None, user_id=None, provider=None, number=None, expire_data=None, security_code=None, dt_current_timestamp=None):

        self.uuid = uuid
        self.user_id = user_id
        self.provider = provider
        self.number = number
        self.expire_data = expire_data
        self.security_code = security_code
        self.dt_current_timestamp = dt_current_timestamp

    # avro does not support code generation
    # need to provide dict representation
    def to_dict(self):

        return {
            "uuid": self.uuid,
            "user_id": self.user_id,
            "provider": self.provider,
            "number": self.number,
            "expire_data": self.expire_data,
            "security_code": self.security_code,
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
        get_data = CreditCard().get_multiple_rows(gen_dt_rows)

        # loop to insert data
        inserts = 0
        while inserts < len(get_data):

            # instantiate new records, execute callbacks
            record = CreditCardAvro()

            try:

                # map columns and access using dict values
                record.uuid = get_data[inserts]['uuid']
                record.user_id = get_data[inserts]['user_id']
                record.provider = get_data[inserts]['provider']
                record.number = get_data[inserts]['number']
                record.expire_data = get_data[inserts]['expire_data']
                record.security_code = get_data[inserts]['security_code']
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
