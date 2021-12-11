# import libraries
import numpy as np
import requests
from datetime import datetime
from requests.exceptions import HTTPError


# class to request calls from api
# https://random-data-api.com/api/
class Requests(object):

    # create artificial [user_id]
    # set 10.000 users [only]
    @staticmethod
    def gen_user_id():
        return np.random.randint(1, 10000, size=100)

    # current timestamp
    # set date and time
    @staticmethod
    def gen_timestamp():
        return datetime.now()

    # get requests method
    @staticmethod
    def api_get_request(url, params):

        # call request with parameters
        # amount of rows to be requested
        dt_request = requests.get(url=url, params=params)

        # get data from api
        # data is returned as a list (dict)
        # json format applied
        for url in [url]:
            try:
                response = requests.get(url)
                response.raise_for_status()
                dict_request = dt_request.json()

            except HTTPError as http_err:
                print(f'http error occurred: {http_err}')
            except Exception as err:
                print(f'api not available at this moment.: {err}')
            else:
                return dict_request
