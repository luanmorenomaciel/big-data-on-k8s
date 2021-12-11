# import libraries
import os
import pandas as pd
from dotenv import load_dotenv
from data_requests.api_requests import Requests
from sqlalchemy import create_engine
from objects.albums import Albums

# get env
load_dotenv()

# load variables
postgres = os.getenv("POSTGRES")
size = os.getenv("SIZE")

# set up parameters to request from api call
params = {'size': size}
url_get_beer = 'https://random-data-api.com/api/beer/random_beer'
url_get_coffee = 'https://random-data-api.com/api/coffee/random_coffee'
url_get_food = 'https://random-data-api.com/api/food/random_food'
url_get_dessert = 'https://random-data-api.com/api/dessert/random_dessert'


# class to insert into datastore
class Postgres(object):

    @staticmethod
    def insert_rows():
        # get request [api] to store in a variable
        # using method get to retrieve data
        dt_beer = Requests.api_get_request(url=url_get_beer, params=params)
        dt_coffee = Requests.api_get_request(url=url_get_coffee, params=params)
        dt_food = Requests.api_get_request(url=url_get_food, params=params)
        dt_dessert = Requests.api_get_request(url=url_get_dessert, params=params)

        # convert python list (dict)
        # use pandas dataframe to ease the insert of the data
        pd_df_beer = pd.DataFrame.from_dict(dt_beer)
        pd_df_coffee = pd.DataFrame.from_dict(dt_coffee)
        pd_df_food = pd.DataFrame.from_dict(dt_food)
        pd_df_dessert = pd.DataFrame.from_dict(dt_dessert)

        # add [user_id] into dataframe
        # add [dt_current_timestamp] into dataframe
        pd_df_beer['user_id'] = Requests().gen_user_id()
        pd_df_coffee['user_id'] = Requests().gen_user_id()
        pd_df_food['user_id'] = Requests().gen_user_id()
        pd_df_dessert['user_id'] = Requests().gen_user_id()
        pd_df_beer['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_coffee['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_food['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_dessert['dt_current_timestamp'] = Requests().gen_timestamp()

        # get albums
        # pd_df_albums = pd.DataFrame.from_dict(Albums().to_dict_rows(gen_dt_rows=size))

        # set up sqlalchemy connection
        # insert pandas dataframe into table (append if exists)
        postgres_engine = create_engine(postgres)

        pd_df_beer.to_sql('beer', postgres_engine, index=False, if_exists='append', chunksize=100)
        pd_df_coffee.to_sql('coffee', postgres_engine, if_exists='append', index=False, chunksize=100)
        pd_df_food.to_sql('food', postgres_engine, if_exists='append', index=False, chunksize=100)
        pd_df_dessert.to_sql('dessert', postgres_engine, if_exists='append', index=False, chunksize=100)
        # pd_df_albums.to_sql('albums', postgres_engine, if_exists='append', index=False, chunksize=100)
