# import libraries
from datastore.kafka import delivery_reports, producer_settings
from objects.agent import Agent
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from random import seed

# incremental seed of 1
seed(1)


class AgentAvro(object):

    # use __slots__ to explicitly declare all schema members
    __slots__ = ["uuid", "user_id", "platform", "email", "domain", "hostname", "method", "url", "ipv4", "port_number", "mac_address", "dt_current_timestamp"]

    # define init function based on the expected input
    def __init__(self, uuid=None, user_id=None, platform=None, email=None, domain=None, hostname=None, method=None, url=None, ipv4=None, port_number=None, mac_address=None, dt_current_timestamp=None):

        self.uuid = uuid
        self.user_id = user_id
        self.platform = platform
        self.email = email
        self.domain = domain
        self.hostname = hostname
        self.method = method
        self.url = url
        self.ipv4 = ipv4
        self.port_number = port_number
        self.mac_address = mac_address
        self.dt_current_timestamp = dt_current_timestamp

    # avro does not support code generation
    # need to provide dict representation
    def to_dict(self):

        return {
            "uuid": self.uuid,
            "user_id": self.user_id,
            "platform": self.platform,
            "email": self.email,
            "domain": self.domain,
            "hostname": self.hostname,
            "method": self.method,
            "url": self.url,
            "ipv4": self.ipv4,
            "port_number": str(self.port_number),
            "mac_address": self.mac_address,
            "dt_current_timestamp": str(self.dt_current_timestamp)
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
        get_data = Agent().get_multiple_rows(gen_dt_rows)

        # loop to insert data
        inserts = 0
        while inserts < len(get_data):

            # instantiate new records, execute callbacks
            record = AgentAvro()

            try:

                # map columns and access using dict values
                record.uuid = get_data[inserts]['uuid']
                record.user_id = get_data[inserts]['user_id']
                record.platform = get_data[inserts]['platform']
                record.email = get_data[inserts]['email']
                record.domain = get_data[inserts]['domain']
                record.hostname = get_data[inserts]['hostname']
                record.method = get_data[inserts]['method']
                record.url = get_data[inserts]['url']
                record.ipv4 = get_data[inserts]['ipv4']
                record.port_number = get_data[inserts]['port_number']
                record.mac_address = get_data[inserts]['mac_address']
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
