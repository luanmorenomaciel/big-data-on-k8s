# import libraries
import os
import pandas as pd
from dotenv import load_dotenv
from data_requests.api_requests import Requests
from sqlalchemy import create_engine
from objects.artists import Artists

# get env
load_dotenv()

# load variables
mysql = os.getenv("MYSQL")
size = os.getenv("SIZE")

# set up parameters to request from api call
params = {'size': size}
url_get_commerce = 'https://random-data-api.com/api/commerce/random_commerce'
url_get_computer = 'https://random-data-api.com/api/computer/random_computer'
url_get_device = 'https://random-data-api.com/api/device/random_device'


# class to insert into datastore
class MySQL(object):

    @staticmethod
    def insert_rows():
        # get request [api] to store in a variable
        # using method get to retrieve data
        dt_commerce = Requests.api_get_request(url=url_get_commerce, params=params)
        dt_computer = Requests.api_get_request(url=url_get_computer, params=params)
        dt_device = Requests.api_get_request(url=url_get_device, params=params)

        # convert python list (dict)
        # use pandas dataframe to ease the insert of the data
        pd_df_commerce = pd.DataFrame.from_dict(dt_commerce)
        pd_df_computer = pd.DataFrame.from_dict(dt_computer)
        pd_df_device = pd.DataFrame.from_dict(dt_device)

        # add [user_id] into dataframe
        # add [dt_current_timestamp] into dataframe
        pd_df_commerce['user_id'] = Requests().gen_user_id()
        pd_df_computer['user_id'] = Requests().gen_user_id()
        pd_df_device['user_id'] = Requests().gen_user_id()
        pd_df_commerce['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_computer['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_device['dt_current_timestamp'] = Requests().gen_timestamp()

        # get artists
        # pd_df_artists = pd.DataFrame.from_dict(Artists().to_dict_rows(gen_dt_rows=size))

        # set up sqlalchemy connection
        # insert pandas dataframe into table (append if exists)
        mysql_engine = create_engine(mysql)

        pd_df_commerce.to_sql('commerce', mysql_engine, if_exists='append', index=False, chunksize=100)
        pd_df_computer.to_sql('computer', mysql_engine, if_exists='append', index=False, chunksize=100)
        pd_df_device.to_sql('device', mysql_engine, if_exists='append', index=False, chunksize=100)
        # pd_df_artists.to_sql('artists', mysql_engine, if_exists='append', index=False, chunksize=100)


