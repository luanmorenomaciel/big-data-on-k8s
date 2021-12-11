"""
# sites and links for reference
https://github.com/robinhood/faust
https://faust.readthedocs.io/en/latest/
https://faust.readthedocs.io/_/downloads/en/latest/pdf/

# generation of events for input topics
python3.9 cli.py 'strimzi-users-json'
python3.9 cli.py 'strimzi-rides-json'

# init python faust application
faust -A src.app worker -l info

# manage application
http://localhost:6066/
"""

# import libraries
import os
import datetime
from dotenv import load_dotenv
from faust.app import App
from src.models import RidesEvent

# get env
load_dotenv()

# load variables
app_name = os.getenv("APP_NAME")
app_version = os.getenv("APP_VERSION")
kafka_bootstrap_server = os.getenv("KAFKA_BOOTSTRAP_SERVER")
memory_store = os.getenv("MEMORY_STORE")
auto_discovery = os.getenv("AUTO_DISCOVERY")
dir_app_source = os.getenv("DIR_APP_SOURCE")
processing_guarantee = os.getenv("PROCESSING_GUARANTEE")
topic_src_app_rides_json = os.getenv("TOPIC_SRC_APP_RIDES_JSON")
topic_output_enriched_rides = os.getenv("TOPIC_OUT_RIDES_JSON")

# application parameters [init]
# main location to declare parameters
app = App(
    id=app_name,
    version=int(app_version),
    broker=kafka_bootstrap_server,
    store=memory_store,
    autodiscover=bool(auto_discovery),
    origin=dir_app_source,
    processing_guarantee=processing_guarantee,
    timeonze=datetime.timezone.utc
)

# data source = apache kafka
# get schema from models
# input topics to read [source]
# output topic for downstream [sink]
get_input_topic_src_app_rides_json = app.topic(topic_src_app_rides_json, value_type=RidesEvent)
output_enriched_rides = app.topic(topic_output_enriched_rides)