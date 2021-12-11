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
albums_file_location = os.getenv("ALBUMS_FILES")


# csv reader class for music data
class Albums:

    def __init__(self):
        self.albums_location = albums_file_location

    def to_dict_rows(self, gen_dt_rows):

        # reading files
        get_albums_data = pd.read_csv(self.albums_location)

        # fixing column names
        get_albums_data.columns = get_albums_data.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

        # replace nan to none
        get_albums_data = get_albums_data.replace({np.nan: None})

        # add new column [identity] = [0,1000]
        # add new column = timestamp
        get_albums_data['user_id'] = np.random.randint(0, 1000, size=(len(get_albums_data), 1))
        get_albums_data['dt_current_timestamp'] = datetime.now()

        # select column ordering
        df = get_albums_data[['artist_id', 'album_title', 'genre', 'year_of_pub', 'num_of_tracks', 'num_of_sales', 'rolling_stone_critic', 'mtv_critic', 'music_maniac_critic', 'dt_current_timestamp']].head(int(gen_dt_rows))

        # convert to dictionary
        df_dict = df.to_dict('records')

        return df_dict
