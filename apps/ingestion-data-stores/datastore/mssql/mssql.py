# import libraries
import os
import pandas as pd
from dotenv import load_dotenv
from data_requests.api_requests import Requests
from sqlalchemy import create_engine

# get env
load_dotenv()

# load variables
mssql = os.getenv("MSSQL")
size = os.getenv("SIZE")

# set up parameters to request from api call
params = {'size': size}
url_get_bank = 'https://random-data-api.com/api/bank/random_bank'
url_get_credit_card = 'https://random-data-api.com/api/business_credit_card/random_card'
url_get_subscription = 'https://random-data-api.com/api/subscription/random_subscription'
url_get_company = 'https://random-data-api.com/api/company/random_company'


# class to insert into datastore
class MSSQL(object):

    @staticmethod
    def insert_rows():
        # get request [api] to store in a variable
        # using method get to retrieve data
        dt_bank = Requests.api_get_request(url=url_get_bank, params=params)
        dt_credit_card = Requests.api_get_request(url=url_get_credit_card, params=params)
        dt_subscription = Requests.api_get_request(url=url_get_subscription, params=params)
        dt_company = Requests.api_get_request(url=url_get_company, params=params)

        # convert python list (dict)
        # use pandas dataframe to ease the insert of the data
        pd_df_bank = pd.DataFrame.from_dict(dt_bank)
        pd_df_credit_card = pd.DataFrame.from_dict(dt_credit_card)
        pd_df_subscription = pd.DataFrame.from_dict(dt_subscription)
        pd_df_company = pd.DataFrame.from_dict(dt_company)

        # add [user_id] into dataframe
        # add [dt_current_timestamp] into dataframe
        pd_df_bank['user_id'] = Requests().gen_user_id()
        pd_df_credit_card['user_id'] = Requests().gen_user_id()
        pd_df_subscription['user_id'] = Requests().gen_user_id()
        pd_df_company['user_id'] = Requests().gen_user_id()
        pd_df_bank['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_credit_card['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_subscription['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_company['dt_current_timestamp'] = Requests().gen_timestamp()

        # set up sqlalchemy connection
        # insert pandas dataframe into table (append if exists)
        mssql_engine = create_engine(mssql)

        pd_df_bank.to_sql('bank', mssql_engine, if_exists='append', index=False, chunksize=10)
        pd_df_credit_card.to_sql('credit_card', mssql_engine, if_exists='append', index=False, chunksize=10)
        pd_df_subscription.to_sql('subscription', mssql_engine, if_exists='append', index=False, chunksize=10)
        pd_df_company.to_sql('company', mssql_engine, if_exists='append', index=False, chunksize=10)
