# import libraries
import json
import os
import logging
import datetime
import pymongo
from dotenv import load_dotenv
from currency_converter import CurrencyConverter
from src.app import app, get_input_topic_src_app_rides_json, output_enriched_rides

# get env
load_dotenv()

# load variables
mongodb_cs = os.getenv("MONGODB_CS")

# build connection string
# for mongodb & mysql
client = pymongo.MongoClient(mongodb_cs)
db = client["owshq"]
user_collection = db["user"]

# add logging capabilities
logger = logging.getLogger(__name__)


# reading events from rides [apache kafka]
# invoking function to deal with transformations
# filtering only rides with price higher than [0]
# some rides are cancelled and price doesn't show up
# specify topics that you want to ingest
@app.agent(get_input_topic_src_app_rides_json)
async def rides_events(events):
    async for event in events.filter(lambda x: x.price > 0):
        # invoke python function for data processing
        transformed_rides = transform_rides_events(event)
        # show raw event
        print(event)
        # show enriched event
        print(transformed_rides)
        # output to a sink topic
        await output_enriched_rides.send(value=transformed_rides)


# python function to enhance rides data
# applying data enrichment rules
def transform_rides_events(events):

    # define global variables
    global gender, country, city

    # convert miles to [km]
    miles2km = 0.621371
    distance_km = float(round(events.distance * miles2km, 2))

    # final price in [real]
    # using external api invoke
    # common problem regarding stream processing
    # increase of latency on the overall event process
    currency_converter = CurrencyConverter()
    dolar2real = currency_converter.convert(events.price, 'USD', 'BRL')
    final_price = float(round(dolar2real * events.surge_multiplier,2))

    # get additional info for surge multiplier
    # dynamic fare > 1.0 (new feature added)
    dynamic_fare = False if events.surge_multiplier <= 1.0 else True

    # working with event time
    # adding processing time to measure time taken for faust
    event_time = datetime.datetime.strptime(events.dt_current_timestamp, "%Y-%m-%d %H:%M:%S.%f")
    processing_time = datetime.datetime.now()

    # dealing with time based
    # types = morning, afternoon, evening
    if event_time.hour < 12:
        time_period = "morning"
    elif event_time.hour < 18:
        time_period = "afternoon"
    else:
        time_period = "night"

    # find clause using user_id ~ seek operation
    # filter columns to output as dict
    find_user_id = {'user_id': events.user_id}
    output_user_columns = {'_id': 0, 'user_id': 1, 'gender': 1, 'address': 1, 'payment_method': 1}

    # submit query to [mongodb] engine
    # find_one function to retrieve data
    get_user_dt = user_collection.find_one(find_user_id, output_user_columns)
    print(get_user_dt)

    # if request does not success add user_id = 0
    # has to be fixed on the upcoming release
    if get_user_dt is None:
        user_id = 0
    else:
        user_id = events.user_id
        gender = get_user_dt['gender']
        country = get_user_dt['address']['country']
        city = get_user_dt['address']['city']

    # create output message
    # this is serve the output kafka topic
    dict_output_events = {
        "user_id": user_id,
        "gender": gender,
        "car_type": events.cab_type,
        "model_type": events.name,
        "country": country,
        "city": city,
        "distance_in_km": distance_km,
        "final_price_real": final_price,
        "dynamic_fare": dynamic_fare,
        "time_period": time_period,
        "event_time": str(event_time),
        "processing_time": str(processing_time)
    }

    # return in [json] format
    return json.dumps(dict_output_events).encode('utf-8')


