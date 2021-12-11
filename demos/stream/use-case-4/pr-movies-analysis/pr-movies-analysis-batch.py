# import libraries
from settings import *
from pyspark.sql.functions import *
from pyspark.sql import SparkSession
from schemas import jsc_users, jsc_movies_titles

# main app
if __name__ == '__main__':

    # init spark session
    spark = SparkSession \
            .builder \
            .appName("pr-movies-analysis-batch") \
            .config("spark.sql.streaming.kafka.useDeprecatedOffsetFetching","false") \
            .getOrCreate()

    # set log level to info
    # [INFO] or [WARN] for more detailed logging info
    spark.sparkContext.setLogLevel("INFO")

    # event schema message [json]
    # refer to schemas.py file
    # set desired timestamp output
    sch_users = jsc_users
    sch_movies_titles = jsc_movies_titles
    jsonOptions = {"timestampFormat": "yyyy-MM-dd'T'HH:mm:ss.sss'Z'"}

    # read variables
    # print env variables from settings.py
    print(BOOTSTRAP_SERVERS)
    print(INPUT_USERS_TOPIC)
    print(INPUT_MOVIES_TITLES_TOPIC)
    print(OUTPUT_TOPIC_COUNTS_PER_COUNTRY_BATCH)

    # read events from [apache kafka]
    # using read coming from apache kafka
    stream_users = spark \
        .read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS) \
        .option("subscribe", INPUT_USERS_TOPIC) \
        .option("startingOffsets", "earliest") \
        .load() \
        .select(from_json(col("value").cast("string"), sch_users, jsonOptions).alias("users"))

    stream_movies_titles = spark \
        .read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS) \
        .option("subscribe", INPUT_MOVIES_TITLES_TOPIC) \
        .option("startingOffsets", "earliest") \
        .load() \
        .select(from_json(col("value").cast("string"), sch_movies_titles, jsonOptions).alias("movies_titles"))

    # select columns [for processing]
    # stateless transformation [does not require info from previous rows]
    # select, explode, map, flatmap, filter, where
    # applied both in batch and stream operations
    get_columns_for_stream_users = stream_users.select(
        col("users.user_id").alias("users_user_id"),
        col("users.first_name"),
        col("users.last_name"),
        col("users.country"),
        col("users.job"),
        col("users.dt_current_timestamp").alias("users_event_time")
    )

    get_columns_for_stream_movies_titles = stream_movies_titles.select(
        col("movies_titles.user_id").alias("movies_user_id"),
        col("movies_titles.genres"),
        col("movies_titles.original_title"),
        col("movies_titles.release_date"),
        col("movies_titles.status"),
        col("movies_titles.dt_current_timestamp").alias("movies_event_time")
    )

    # output selected columns
    # use utf-8
    get_columns_for_stream_users.show()
    get_columns_for_stream_movies_titles.show()

    # register streaming as a temporary view
    # make it available to spark sql engine
    get_columns_for_stream_users.createOrReplaceTempView("vw_users")
    get_columns_for_stream_movies_titles.createOrReplaceTempView("vw_movies_titles")

    # applying transformations into data
    # grouping data read from apache kafka ~ topics
    get_grouped_data_to_insert_full_mode = spark.sql("""
        SELECT u.country, u.users_event_time AS event_time, COUNT(*) AS count 
        FROM vw_users AS u
        INNER JOIN vw_movies_titles AS t
        ON u.users_user_id = t.movies_user_id
        GROUP BY u.country, u.users_event_time
        ORDER BY count DESC
    """)

    # read dataframe data
    # show data into the display
    get_grouped_data_to_insert_full_mode.show()

    # write final output into apache kafka
    # sending to a new topic
    get_grouped_data_to_insert_full_mode \
        .select("country", "event_time", "count") \
        .select(to_json(struct(col("country"), col("event_time"), col("count"))).alias("value")) \
        .write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS) \
        .option("topic", OUTPUT_TOPIC_COUNTS_PER_COUNTRY_BATCH) \
        .save()

    # stop spark session
    spark.stop()