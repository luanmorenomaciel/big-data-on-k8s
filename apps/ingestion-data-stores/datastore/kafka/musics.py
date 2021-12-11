# import libraries
from datastore.kafka import delivery_reports, producer_settings
from objects.musics import Musics
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from random import seed

# incremental seed of 1
seed(1)


class MusicsAvro(object):

    # use __slots__ to explicitly declare all schema members
    __slots__ = ["user_id", "genre", "artist_name", "track_name", "track_id", "popularity", "duration_ms", "id"]

    # define init function based on the expected input
    def __init__(self, user_id=None, genre=None, artist_name=None, track_name=None, track_id=None, popularity=None, duration_ms=None):

        self.user_id = user_id
        self.genre = genre
        self.artist_name = artist_name
        self.track_name = track_name
        self.track_id = track_id
        self.popularity = popularity
        self.duration_ms = duration_ms

    # avro does not support code generation
    # need to provide dict representation
    def to_dict(self):

        return {
            "user_id": self.user_id,
            "genre": self.genre,
            "artist_name": self.artist_name,
            "track_name": self.track_name,
            "track_id": self.track_id,
            "popularity": self.popularity,
            "duration_ms": self.duration_ms
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
        get_data = Musics().get_multiple_rows(gen_dt_rows)

        # loop to insert data
        inserts = 0
        while inserts < len(get_data):

            # instantiate new records, execute callbacks
            record = MusicsAvro()

            try:

                # map columns and access using dict values
                record.user_id = get_data[inserts]['user_id']
                record.genre = get_data[inserts]['genre']
                record.artist_name = get_data[inserts]['artist_name']
                record.track_name = get_data[inserts]['track_name']
                record.track_id = get_data[inserts]['track_id']
                record.popularity = get_data[inserts]['popularity']
                record.duration_ms = get_data[inserts]['duration_ms']

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
