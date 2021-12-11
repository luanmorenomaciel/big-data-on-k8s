# import libraries
from dotenv import load_dotenv
from datetime import datetime
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
music_file_location = os.getenv("MUSIC_FILES")


# csv reader class for music data
class Musics:

    def __init__(self):
        self.music_file_location = music_file_location

    def get_multiple_rows(self, gen_dt_rows):

        # reading files
        get_music_data = pd.read_csv(self.music_file_location)

        # fixing column names
        get_music_data.columns = get_music_data.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

        # replace nan to none
        get_music_data = get_music_data.replace({np.nan: None})

        # add new column [identity] = [0,1000]
        # add timestamp column
        get_music_data['user_id'] = np.random.randint(0, 1000, size=(len(get_music_data), 1))
        get_music_data['dt_current_timestamp'] = str(datetime.now())

        # select column ordering
        # add sample to retrieve different values
        # for every single call
        df = get_music_data[['user_id', 'genre', 'artist_name', 'track_name', 'track_id', 'popularity', 'duration_ms', 'dt_current_timestamp']].sample(int(gen_dt_rows))

        # convert to dictionary
        df_dict = df.to_dict('records')

        return df_dict
