# import libraries
from datastore.kafka import delivery_reports, producer_settings
from objects.users import Users
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from random import seed

# incremental seed of 1
seed(1)


class LogCompactionUsersAvro(object):

    # use __slots__ to explicitly declare all schema members
    __slots__ = ["user_id", "uuid", "first_name", "last_name", "date_birth", "city", "country", "company_name", "job", "phone_number", "last_access_time", "time_zone", "dt_current_timestamp"]

    # define init function based on the expected input
    def __init__(self, user_id=None, uuid=None, first_name=None, last_name=None, date_birth=None, city=None, country=None, company_name=None, job=None, phone_number=None, last_access_time=None, time_zone=None, dt_current_timestamp=None):

        self.user_id = user_id
        self.uuid = uuid
        self.first_name = first_name
        self.last_name = last_name
        self.date_birth = date_birth
        self.city = city
        self.country = country
        self.company_name = company_name
        self.job = job
        self.phone_number = phone_number
        self.last_access_time = last_access_time
        self.time_zone = time_zone
        self.dt_current_timestamp = dt_current_timestamp

    # avro does not support code generation
    # need to provide dict representation
    def to_dict(self):

        return {
            "user_id": self.user_id,
            "uuid": self.uuid,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_birth": self.date_birth,
            "city": self.city,
            "country": self.country,
            "company_name": self.company_name,
            "job": self.job,
            "phone_number": self.phone_number,
            "last_access_time": self.last_access_time,
            "time_zone": self.time_zone,
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
        get_data = Users().log_compaction(gen_dt_rows)

        # loop to insert data
        inserts = 0
        while inserts < len(get_data):

            # instantiate new records, execute callbacks
            record = LogCompactionUsersAvro()

            try:

                # map columns and access using dict values
                record.user_id = get_data[inserts]['user_id']
                record.uuid = get_data[inserts]['uuid']
                record.first_name = get_data[inserts]['first_name']
                record.last_name = get_data[inserts]['last_name']
                record.date_birth = get_data[inserts]['date_birth']
                record.city = get_data[inserts]['city']
                record.country = get_data[inserts]['country']
                record.company_name = get_data[inserts]['company_name']
                record.job = get_data[inserts]['job']
                record.phone_number = get_data[inserts]['phone_number']
                record.last_access_time = get_data[inserts]['last_access_time']
                record.time_zone = get_data[inserts]['time_zone']
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
