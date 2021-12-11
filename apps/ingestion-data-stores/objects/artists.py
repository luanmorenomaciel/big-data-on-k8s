# import libraries
from datetime import datetime
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np

# get env
load_dotenv()

# pandas config
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# load variables
artists_file_location = os.getenv("ARTISTS_FILES")


# csv reader class for music data
class Artists:

    def __init__(self):
        self.artists_location = artists_file_location

    def to_dict_rows(self, gen_dt_rows):

        # reading files
        get_artists_data = pd.read_csv(self.artists_location)

        # fixing column names
        get_artists_data.columns = get_artists_data.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

        # replace nan to none
        get_artists_data = get_artists_data.replace({np.nan: None})

        # add new column [identity] = [0,1000]
        # add new column = timestamp
        get_artists_data['user_id'] = np.random.randint(0, 1000, size=(len(get_artists_data), 1))
        get_artists_data['dt_current_timestamp'] = datetime.now()

        # select column ordering
        df = get_artists_data[['id', 'real_name', 'art_name', 'role', 'year_of_birth', 'country', 'city', 'email', 'zip_code', 'dt_current_timestamp']].head(int(gen_dt_rows))

        # convert to dictionary
        df_dict = df.to_dict('records')

        return df_dict
