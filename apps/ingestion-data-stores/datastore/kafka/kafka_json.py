# import libraries
import json
from datastore.kafka import delivery_reports, producer_settings
from confluent_kafka import Producer


# class to insert into datastore
class Kafka(object):

    # producer function
    @staticmethod
    def json_producer(broker, object_name, kafka_topic):

        # init producer settings
        p = Producer(producer_settings.producer_settings_json(broker))

        # get object [dict] from objects
        # transform into tuple to a multiple insert process
        get_data = object_name
        print(get_data)

        # for loop to insert all data
        for data in get_data:

            try:
                # trigger any available delivery report callbacks from previous produce() calls
                p.poll(0)

                # asynchronously produce a message, the delivery report callback
                # will be triggered from poll() above, or flush() below, when the message has
                # been successfully delivered or failed permanently.
                p.produce(
                    topic=kafka_topic,
                    value=json.dumps(data).encode('utf-8'),
                    callback=delivery_reports.on_delivery_json
                )

            except BufferError:
                print("buffer full")
                p.poll(0.1)

            except ValueError:
                print("invalid input")
                raise

            except KeyboardInterrupt:
                raise

        # wait for any outstanding messages to be delivered and delivery report
        # callbacks to be triggered.
        p.flush()
