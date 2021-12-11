# import libraries
import os
import json
import pandas as pd
from dotenv import load_dotenv
from data_requests.api_requests import Requests
from sqlalchemy import create_engine

# get env
load_dotenv()

# pandas config
# pd.set_option('display.max_rows', 100000)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)

# load variables
ysql = os.getenv("YSQL")
size = os.getenv("SIZE")

# set up parameters to request from api call
params = {'size': size}
url_get_user = 'https://random-data-api.com/api/users/random_user'
url_get_subscription = 'https://random-data-api.com/api/subscription/random_subscription'
url_get_device = 'https://random-data-api.com/api/device/random_device'

# create table statement on ysql
# json fields
"""
create table "user"
(
    usr_key_id serial primary key,
    id int8,
    uid text,
    first_name text,
    last_name text,
    username text,
    email text,
    gender text,
    date_of_birth text,
    address json,
    subscription json,
    user_id int8,
    dt_current_timestamp timestamp(6)
);
"""


# class to insert into datastore
class YSQL(object):

    @staticmethod
    def insert_rows():
        # get request [api] to store in a variable
        # using method get to retrieve data
        dt_user = Requests.api_get_request(url=url_get_user, params=params)
        dt_subscription = Requests.api_get_request(url=url_get_subscription, params=params)
        dt_device = Requests.api_get_request(url=url_get_device, params=params)

        # convert python list (dict)
        # use pandas dataframe to ease the insert of the data
        # select columns
        pd_df_user = pd.DataFrame.from_dict(dt_user)
        pd_df_user = pd_df_user[['id', 'uid', 'first_name', 'last_name', 'username', 'email', 'gender', 'date_of_birth', 'address', 'subscription']]
        pd_df_subscription = pd.DataFrame.from_dict(dt_subscription)
        pd_df_device = pd.DataFrame.from_dict(dt_device)

        # apply json.dumps transformation to serialize to json format
        pd_df_user['address'] = pd_df_user['address'].apply(json.dumps)
        pd_df_user['subscription'] = pd_df_user['subscription'].apply(json.dumps)

        # add [user_id] into dataframe
        # add [dt_current_timestamp] into dataframe
        pd_df_user['user_id'] = Requests().gen_user_id()
        pd_df_subscription['user_id'] = Requests().gen_user_id()
        pd_df_device['user_id'] = Requests().gen_user_id()
        pd_df_user['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_subscription['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_device['dt_current_timestamp'] = Requests().gen_timestamp()

        # set up sqlalchemy connection
        # insert pandas dataframe into table (append if exists)
        ysql_engine = create_engine(ysql)
        pd_df_user.to_sql('user', ysql_engine, if_exists='append', index=False, chunksize=100)
        pd_df_subscription.to_sql('subscription', ysql_engine, if_exists='append', index=False, chunksize=100)
        pd_df_device.to_sql('device', ysql_engine, if_exists='append', index=False, chunksize=100)
