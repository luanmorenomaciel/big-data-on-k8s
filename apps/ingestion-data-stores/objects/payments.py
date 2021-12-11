# import libraries
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np

# get env
load_dotenv()

# load variables
mongodb_server = os.getenv("MONGODB_SERVER")
payments_file_location = os.getenv("PAYMENTS_FILES")


# csv reader class for payments
class Payments:

    def __init__(self):
        self.user_file_location = payments_file_location

    def csv_reader(self, gen_dt_rows):

        # reading file
        get_user_data = pd.read_csv(self.user_file_location)

        # fixing column names
        get_user_data.columns = get_user_data.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(','').str.replace(')', '')

        # replace [nan] to [none]
        get_user_data = get_user_data.replace({np.nan: None})

        # select column ordering
        user_output = get_user_data[
            [
                'user_id',
                'gender',
                'language',
                'race',
                'job_title',
                'city',
                'country',
                'currency',
                'currency_mode',
                'credit_card_type',
                'subscription_price',
                'time',
                'datetime'
            ]].head(int(gen_dt_rows))

        # convert to list
        payments_list = user_output.to_dict('records')

        return payments_list
