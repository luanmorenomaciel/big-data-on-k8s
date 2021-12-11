# import libraries
import os
import pandas as pd
from dotenv import load_dotenv
from data_requests.api_requests import Requests
from pymongo import MongoClient
from objects.payments import Payments

# get env
load_dotenv()

# load variables
mongodb = os.getenv("MONGODB")
mongodb_database = os.getenv("MONGODB_DATABASE")
size = os.getenv("SIZE")

# set up parameters to request from api call
params = {'size': size}
url_get_user = 'https://random-data-api.com/api/users/random_user'
url_get_restaurant = 'https://random-data-api.com/api/restaurant/random_restaurant'
url_get_vehicle = 'https://random-data-api.com/api/vehicle/random_vehicle'
url_get_stripe = 'https://random-data-api.com/api/stripe/random_stripe'
url_get_google_auth = 'https://random-data-api.com/api/omniauth/google_get'
url_get_facebook_auth = 'https://random-data-api.com/api/omniauth/facebook_get'
url_get_twitter_auth = 'https://random-data-api.com/api/omniauth/twitter_get'
url_get_linkedin_auth = 'https://random-data-api.com/api/omniauth/linkedin_get'
url_get_github_auth = 'https://random-data-api.com/api/omniauth/github_get'
url_get_apple_auth = 'https://random-data-api.com/api/omniauth/apple_get'


# class to insert into datastore
class MongoDB(object):

    @staticmethod
    def insert_rows():
        # get request [api] to store in a variable
        # using method get to retrieve data
        dt_user = Requests.api_get_request(url=url_get_user, params=params)
        dt_restaurant = Requests.api_get_request(url=url_get_restaurant, params=params)
        dt_vehicle = Requests.api_get_request(url=url_get_vehicle, params=params)
        dt_stripe = Requests.api_get_request(url=url_get_stripe, params=params)
        dt_google_auth = Requests.api_get_request(url=url_get_google_auth, params=params)
        dt_facebook_auth = Requests.api_get_request(url=url_get_facebook_auth, params=params)
        dt_twitter_auth = Requests.api_get_request(url=url_get_twitter_auth, params=params)
        dt_linkedin_auth = Requests.api_get_request(url=url_get_linkedin_auth, params=params)
        dt_github_auth = Requests.api_get_request(url=url_get_github_auth, params=params)
        dt_apple_auth = Requests.api_get_request(url=url_get_apple_auth, params=params)

        # convert python list (dict)
        # use pandas dataframe to ease the insert of the data
        pd_df_user = pd.DataFrame.from_dict(dt_user)
        pd_df_restaurant = pd.DataFrame.from_dict(dt_restaurant)
        pd_df_vehicle = pd.DataFrame.from_dict(dt_vehicle)
        pd_df_stripe = pd.DataFrame.from_dict(dt_stripe)
        pd_df_google_auth = pd.DataFrame.from_dict(dt_google_auth)
        pd_df_facebook_auth = pd.DataFrame.from_dict(dt_facebook_auth)
        pd_df_twitter_auth = pd.DataFrame.from_dict(dt_twitter_auth)
        pd_df_linkedin_auth = pd.DataFrame.from_dict(dt_linkedin_auth)
        pd_df_github_auth = pd.DataFrame.from_dict(dt_github_auth)
        pd_df_apple_auth = pd.DataFrame.from_dict(dt_apple_auth)

        # add [user_id] into dataframe
        # add [dt_current_timestamp] into dataframe
        pd_df_user['user_id'] = Requests().gen_user_id()
        pd_df_restaurant['user_id'] = Requests().gen_user_id()
        pd_df_vehicle['user_id'] = Requests().gen_user_id()
        pd_df_stripe['user_id'] = Requests().gen_user_id()
        pd_df_user['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_restaurant['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_vehicle['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_stripe['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_google_auth['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_facebook_auth['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_twitter_auth['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_linkedin_auth['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_github_auth['dt_current_timestamp'] = Requests().gen_timestamp()
        pd_df_apple_auth['dt_current_timestamp'] = Requests().gen_timestamp()

        # connecting into mongodb
        # set database connectivity
        client = MongoClient(mongodb)
        db = client[mongodb_database]

        # setting up collection to insert data
        # pandas dataframe
        collection_user = db['user']
        collection_restaurant = db['restaurant']
        collection_vehicle = db['vehicle']
        collection_stripe = db['stripe']
        collection_google_auth = db['google_auth']
        collection_facebook_auth = db['facebook_auth']
        collection_twitter_auth = db['twitter_auth']
        collection_linkedin_auth = db['linkedin_auth']
        collection_github_auth = db['github_auth']
        collection_apple_auth = db['apple_auth']
        collection_payments = db['payments']

        # user [df]
        # get records from dataframe
        # insert into collection
        pd_df_user.reset_index(inplace=True)
        data_dict_user = pd_df_user.to_dict("records")
        collection_user.insert_many(data_dict_user)

        # restaurant [df]
        # get records from dataframe
        # insert into collection
        pd_df_restaurant.reset_index(inplace=True)
        data_dict_restaurant = pd_df_restaurant.to_dict("records")
        collection_restaurant.insert_many(data_dict_restaurant)

        # vehicle [df]
        # get records from dataframe
        # insert into collection
        pd_df_vehicle.reset_index(inplace=True)
        data_dict_vehicle = pd_df_vehicle.to_dict("records")
        collection_vehicle.insert_many(data_dict_vehicle)

        # stripe [df]
        # get records from dataframe
        # insert into collection
        pd_df_stripe.reset_index(inplace=True)
        data_dict_stripe = pd_df_stripe.to_dict("records")
        collection_stripe.insert_many(data_dict_stripe)

        # google_auth [df]
        # get records from dataframe
        # insert into collection
        pd_df_google_auth.reset_index(inplace=True)
        data_dict_google_auth = pd_df_google_auth.to_dict("records")
        collection_google_auth.insert_many(data_dict_google_auth)

        # facebook [df]
        # get records from dataframe
        # insert into collection
        pd_df_facebook_auth.reset_index(inplace=True)
        data_dict_facebook_auth = pd_df_facebook_auth.to_dict("records")
        collection_facebook_auth.insert_many(data_dict_facebook_auth)

        # twitter [df]
        # get records from dataframe
        # insert into collection
        pd_df_twitter_auth.reset_index(inplace=True)
        data_dict_twitter_auth = pd_df_twitter_auth.to_dict("records")
        collection_twitter_auth.insert_many(data_dict_twitter_auth)

        # linkedin [df]
        # get records from dataframe
        # insert into collection
        pd_df_linkedin_auth.reset_index(inplace=True)
        data_dict_linkedin_auth = pd_df_linkedin_auth.to_dict("records")
        collection_linkedin_auth.insert_many(data_dict_linkedin_auth)

        # github [df]
        # get records from dataframe
        # insert into collection
        pd_df_github_auth.reset_index(inplace=True)
        data_dict_github_auth = pd_df_github_auth.to_dict("records")
        collection_github_auth.insert_many(data_dict_github_auth)

        # apple [df]
        # get records from dataframe
        # insert into collection
        pd_df_apple_auth.reset_index(inplace=True)
        data_dict_apple_auth = pd_df_apple_auth.to_dict("records")
        collection_apple_auth.insert_many(data_dict_apple_auth)

        # payments [df]
        # get records from dataframe
        # insert into collection
        collection_payments.insert_many(Payments().csv_reader(gen_dt_rows=size))
