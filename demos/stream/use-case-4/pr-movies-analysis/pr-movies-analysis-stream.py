# import libraries
from settings import *
from pyspark.sql.functions import *
from pyspark.sql import SparkSession
from schemas import jsc_users, jsc_movies_titles

# main spark program
if __name__ == '__main__':

    # init spark session
    spark = SparkSession \
            .builder \
            .appName("pr-movies-analysis-stream") \
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
    print(OUTPUT_TOPIC_COUNTS_PER_GENRES_STREAM)

    # reading data from apache kafka
    # stream operation mode
    # latest offset recorded on kafka and spark
    stream_movies_titles = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS) \
        .option("subscribe", INPUT_MOVIES_TITLES_TOPIC) \
        .option("startingOffsets", "latest") \
        .option("checkpoint", "checkpoint") \
        .load() \
        .select(from_json(col("value").cast("string"), sch_movies_titles, jsonOptions).alias("movies_titles"))

    # select columns [for processing]
    # stateless transformation [does not require info from previous rows]
    # select, explode, map, flatmap, filter, where
    # applied both in batch and stream operations
    get_columns_for_stream_movies_titles = stream_movies_titles.select(
        col("movies_titles.user_id"),
        col("movies_titles.genres"),
        col("movies_titles.original_title"),
        col("movies_titles.release_date"),
        col("movies_titles.status"),
        col("movies_titles.dt_current_timestamp").alias("event_time")
    )

    # view raw structured streaming dataframes
    # console [output] = titles
    """
    query_movie_titles = get_columns_for_stream_movies_titles \
        .writeStream \
        .format("console") \
        .start()
    print(query_movie_titles)
    """

    # aggregation based with event-time windows
    # console and apache kafka topic output
    # add window to compute query
    get_genres_per_event_time = get_columns_for_stream_movies_titles \
        .withWatermark("event_time", "1 minute") \
        .groupBy("genres", "event_time") \
        .count()

    """
    query_grouped_streams = get_genres_per_event_time \
        .writeStream \
        .format("console") \
        .start()
    print(query_grouped_streams)
    """

    # trigger using processing time = interval of the micro-batches
    # formatting to deliver to apache kafka payload (value)
    write_into_topic_genres_per_event_time = get_genres_per_event_time \
        .select("genres", "event_time", "count") \
        .select(to_json(struct(col("genres"), col("event_time"), col("count"))).alias("value")) \
        .writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS) \
        .option("topic", OUTPUT_TOPIC_COUNTS_PER_GENRES_STREAM) \
        .option("checkpointLocation", "checkpoint") \
        .outputMode("append") \
        .trigger(processingTime="15 seconds") \
        .start()
        
    # monitoring streaming queries
    # structured streaming output info
    # read last progress & last status of query
    print(write_into_topic_genres_per_event_time.lastProgress)
    print(write_into_topic_genres_per_event_time.status)

    # block until query is terminated
    write_into_topic_genres_per_event_time.awaitTermination()
