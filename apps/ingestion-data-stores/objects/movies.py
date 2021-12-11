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
movies = os.getenv("MOVIES_FILES")
ratings = os.getenv("RATINGS_FILES")
keywords = os.getenv("KEYWORDS_FILES")


# csv reader class for music data
class Movies:

    def __init__(self):
        self.movies_location = movies
        self.ratings_location = ratings
        self.ratings_keywords = keywords

    def get_movies(self, gen_dt_rows):
        # reading files
        get_movies = pd.read_csv(self.movies_location, low_memory=False)

        # fixing column names
        get_movies.columns = get_movies.columns.str.strip().str.lower().str.replace(' ', '_', regex=True).str.replace('(', '', regex=True).str.replace(')', '', regex=True)

        # replace nan to none
        get_movies = get_movies.replace({np.nan: None})

        # add new column [identity] = [0,1000]
        get_movies['user_id'] = np.random.randint(0, 1000, size=(len(get_movies), 1))
        get_movies['dt_current_timestamp'] = str(datetime.now())

        # select column ordering
        # add sample to retrieve different values
        # for every single call
        df = get_movies[['user_id', 'adult', 'belongs_to_collection', 'genres', 'id', 'imdb_id', 'original_language', 'original_title', 'overview', 'popularity', 'production_companies', 'production_countries', 'release_date', 'revenue', 'status', 'title', 'vote_average', 'vote_count', 'dt_current_timestamp']].sample(int(gen_dt_rows))

        # convert to dictionary
        df_dict = df.to_dict('records')

        return df_dict

    def get_ratings(self, gen_dt_rows):
        # reading files
        get_ratings = pd.read_csv(self.ratings_location, low_memory=False)

        # fixing column names
        get_ratings.columns = get_ratings.columns.str.strip().str.lower().str.replace(' ', '_', regex=True).str.replace('(', '', regex=True).str.replace(')', '', regex=True)

        # replace nan to none
        get_ratings = get_ratings.replace({np.nan: None})

        # add new column [identity] = [0,1000]
        get_ratings['user_id'] = np.random.randint(0, 1000, size=(len(get_ratings), 1))
        get_ratings['dt_current_timestamp'] = str(datetime.now())

        # select column ordering
        # add sample to retrieve different values
        # for every single call
        df = get_ratings[['user_id', 'movieid', 'rating', 'timestamp', 'dt_current_timestamp']].sample(int(gen_dt_rows))

        # convert to dictionary
        df_dict = df.to_dict('records')

        return df_dict

    def get_keywords(self, gen_dt_rows):
        # reading files
        get_keywords = pd.read_csv(self.ratings_keywords, low_memory=False)

        # fixing column names
        get_keywords.columns = get_keywords.columns.str.strip().str.lower().str.replace(' ', '_', regex=True).str.replace('(', '', regex=True).str.replace(')', '', regex=True)

        # replace nan to none
        get_keywords = get_keywords.replace({np.nan: None})

        # add new column [identity] = [0,1000]
        get_keywords['user_id'] = np.random.randint(0, 1000, size=(len(get_keywords), 1))
        get_keywords['dt_current_timestamp'] = str(datetime.now())

        # select column ordering
        # add sample to retrieve different values
        # for every single call
        df = get_keywords[['id', 'keywords', 'user_id', 'dt_current_timestamp']].sample(int(gen_dt_rows))

        # convert to dictionary
        df_dict = df.to_dict('records')

        return df_dict
