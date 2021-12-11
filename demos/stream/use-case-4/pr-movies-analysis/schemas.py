# import libraries
from pyspark.sql.types import *

# users
jsc_users = StructType(
        [
            StructField('user_id', IntegerType(), True),
            StructField('uuid', StringType(), True),
            StructField('first_name', StringType(), True),
            StructField('last_name', StringType(), True),
            StructField('date_birth', IntegerType(), True),
            StructField('city', StringType(), True),
            StructField('country', StringType(), True),
            StructField('company_name', StringType(), True),
            StructField('job', StringType(), True),
            StructField('phone_number', StringType(), True),
            StructField('last_access_time', StringType(), True),
            StructField('time_zone', StringType(), True),
            StructField('dt_current_timestamp', TimestampType(), True)
        ])

# movies
jsc_movies_titles = StructType(
        [
            StructField('user_id', IntegerType(), True),
            StructField('adult', StringType(), True),
            StructField('belongs_to_collection', StringType(), True),
            StructField('genres', StringType(), True),
            StructField('id', IntegerType(), True),
            StructField('imdb_id', StringType(), True),
            StructField('original_language', StringType(), True),
            StructField('original_title', StringType(), True),
            StructField('overview', StringType(), True),
            StructField('popularity', StringType(), True),
            StructField('production_companies', StringType(), True),
            StructField('production_countries', StringType(), True),
            StructField('release_date', StringType(), True),
            StructField('revenue', StringType(), True),
            StructField('status', StringType(), True),
            StructField('title', StringType(), True),
            StructField('vote_average', IntegerType(), True),
            StructField('vote_count', IntegerType(), True),
            StructField('dt_current_timestamp', TimestampType(), True)
        ])
