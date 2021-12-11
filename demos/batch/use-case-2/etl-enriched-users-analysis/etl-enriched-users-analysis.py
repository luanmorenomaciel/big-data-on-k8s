# import libraries
from delta.tables import *
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.types import DateType, StringType, TimestampType, DecimalType
from pyspark.sql.functions import current_timestamp, col

# main spark program
# init application
if __name__ == '__main__':

    # init session
    # set configs
    spark = SparkSession \
        .builder \
        .appName("etl-enriched-users-analysis-py") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://20.62.75.137") \
        .config("spark.hadoop.fs.s3a.access.key", "H4aQRS39OITgclWk") \
        .config("spark.hadoop.fs.s3a.secret.key", "wRozzyetjvRrVQS9qpIzFVnimQFm9CqW") \
        .config("spark.hadoop.fs.s3a.path.style.access", True) \
        .config("spark.hadoop.fs.s3a.fast.upload", True) \
        .config("spark.hadoop.fs.s3a.multipart.size", 104857600) \
        .config("fs.s3a.connection.maximum", 100) \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

    # show configured parameters
    print(SparkConf().getAll())

    # set log level
    spark.sparkContext.setLogLevel("INFO")

    # set location of files
    # minio data lake engine

    # [landing zone area]
    # device and subscription
    get_device_file = "s3a://landing/device/*.json"
    get_subscription_file = "s3a://landing/subscription/*.json"

    # read device data
    # json file from landing zone
    df_device = spark.read \
        .format("json") \
        .option("inferSchema", "true") \
        .option("header", "true") \
        .json(get_device_file)

    # read subscription data
    # json file from landing zone
    df_subscription = spark.read \
        .format("json") \
        .option("inferSchema", "true") \
        .option("header", "true") \
        .json(get_subscription_file)

    # get number of partitions
    print(df_device.rdd.getNumPartitions())
    print(df_subscription.rdd.getNumPartitions())

    # count amount of rows ingested from lake
    df_device.count()
    df_subscription.count()

    # [bronze zone area]
    # data lakehouse paradigm
    # need to read the entire landing zone
    # usual scenario but not the best practice
    write_delta_mode = "overwrite"
    delta_bronze_zone = "s3a://lakehouse/bronze"
    df_device.write.mode(write_delta_mode).format("delta").save(delta_bronze_zone + "/device/")
    df_subscription.write.mode(write_delta_mode).format("delta").save(delta_bronze_zone + "/subscription/")

    # [silver zone area]
    # applying enrichment
    # select columns from dataframes to reduce footprint
    select_columns_device = df_device.select("user_id", "uid", "model", "manufacturer", "platform", "dt_current_timestamp")
    select_columns_subscription = df_subscription.select("user_id", "plan", "status", "dt_current_timestamp")

    # select columns to be used
    # same data coming from data lake
    enhance_column_selection_device = select_columns_device.select(
        col("user_id").alias("device_user_id"),
        col("model").alias("device_model"),
        col("dt_current_timestamp").alias("device_event_time"),
    ).distinct()

    # make it available into spark's sql engine
    enhance_column_selection_device.createOrReplaceTempView("vw_device")

    # [udf] in python
    # business transformations
    def subscription_importance(subscription_plan):
        if subscription_plan in ("Business", "Diamond", "Gold", "Platinum", "Premium"):
            return "High"
        if subscription_plan in ("Bronze", "Essential", "Professional", "Silver", "Standard"):
            return "Normal"
        else:
            return "Low"

    # register function into spark's engine to make it available
    # once registered you can access in any language
    spark.udf.register("fn_subscription_importance", subscription_importance)

    # select columns of subscription
    # use alias to save your upfront process ~ silver
    # better name understanding for the business
    enhance_column_selection_subscription = select_columns_subscription.select(
        col("user_id").alias("subscription_user_id"),
        col("plan").alias("subscription_plan"),
        col("status").alias("subscription_status"),
        col("dt_current_timestamp").alias("subscription_event_time"),
    ).distinct()

    # register as a spark sql object
    enhance_column_selection_subscription.createOrReplaceTempView("vw_subscription")

    # build another way to create functions
    # using spark sql engine capability to perform a case when
    # save the sql into a dataframe
    enhance_column_selection_subscription = spark.sql("""
    SELECT subscription_user_id, 
           subscription_plan, 
           CASE WHEN subscription_plan = 'Basic' THEN 6.00 
                WHEN subscription_plan = 'Bronze' THEN 8.00 
                WHEN subscription_plan = 'Business' THEN 10.00 
                WHEN subscription_plan = 'Diamond' THEN 14.00
                WHEN subscription_plan = 'Essential' THEN 9.00 
                WHEN subscription_plan = 'Free Trial' THEN 0.00
                WHEN subscription_plan = 'Gold' THEN 25.00
                WHEN subscription_plan = 'Platinum' THEN 9.00
                WHEN subscription_plan = 'Premium' THEN 13.00
                WHEN subscription_plan = 'Professional' THEN 17.00
                WHEN subscription_plan = 'Silver' THEN 11.00
                WHEN subscription_plan = 'Standard' THEN 13.00
                WHEN subscription_plan = 'Starter' THEN 5.00
                WHEN subscription_plan = 'Student' THEN 2.00
           ELSE 0.00 END AS subscription_price,
           subscription_status,
           fn_subscription_importance(subscription_plan) AS subscription_importance,
           subscription_event_time AS subscription_event_time
    FROM vw_subscription
    """)

    # show & count df
    enhance_column_selection_device.explain()
    enhance_column_selection_device.count()
    enhance_column_selection_subscription.explain()
    enhance_column_selection_subscription.count()

    # show df
    enhance_column_selection_device.show()
    enhance_column_selection_subscription.show()

    # perform inner join between the subscription and device
    # figure out which devices are being used to watch movies
    inner_join_subscriptions = enhance_column_selection_subscription.join(
        enhance_column_selection_device,
        enhance_column_selection_subscription.subscription_user_id == enhance_column_selection_device.device_user_id,
        how='inner'
    )

    # show join
    # grouped result set
    inner_join_subscriptions.show()

    # writing into [silver] zone
    # data lakehouse paradigm
    write_delta_mode = "overwrite"
    delta_silver_zone = "s3a://lakehouse/silver"
    inner_join_subscriptions.write.format("delta").mode(write_delta_mode).save(delta_silver_zone + "/subscriptions/")

    # read delta table
    # new feature of delta 1.0.0
    # show info
    # toDF() = dataframe representation
    # of a delta table
    delta_lake_location_subscriptions = "s3a://lakehouse/silver/subscriptions"
    dt_subscriptions = DeltaTable.forPath(spark, delta_lake_location_subscriptions)
    dt_subscriptions.toDF().show()

    # select columns for analysis
    # latest version
    select_columns_subscriptions = dt_subscriptions.toDF().select("subscription_plan", "subscription_price", "subscription_importance", "device_model")
    select_columns_subscriptions.show()

    # add timestamp column
    # generated column into df
    get_plans_df = select_columns_subscriptions.withColumn("subscription_event_time", current_timestamp())
    get_correct_columns = get_plans_df.select(
        col("subscription_plan").alias("plan"),
        col("subscription_price").alias("price"),
        col("subscription_importance").alias("importance"),
        col("device_model").alias("model"),
        col("subscription_event_time").alias("event_time")
    )

    # building [gold zone area]
    # create table in metastore
    # deltatablebuilder api
    delta_gold_tb_plans_location = "s3a://lakehouse/gold/plans"
    DeltaTable.createIfNotExists(spark) \
        .tableName("plans") \
        .addColumn("plan", StringType()) \
        .addColumn("price", DecimalType(4, 2)) \
        .addColumn("importance", StringType()) \
        .addColumn("model", StringType()) \
        .addColumn("event_time", TimestampType()) \
        .addColumn("date", DateType(), generatedAlwaysAs="CAST(event_time AS DATE)") \
        .partitionedBy("date") \
        .location(delta_gold_tb_plans_location) \
        .execute()

    # insert into new table
    get_correct_columns.write.format("delta").mode("overwrite").save(delta_gold_tb_plans_location)

    # delta table name = plans
    # read latest rows added
    dt_plans_delta = DeltaTable.forPath(spark, delta_gold_tb_plans_location)
    dt_plans_delta.toDF().show()

    # describe history
    # find timestamp and version
    dt_subscriptions.history().show()
    dt_plans_delta.history().show()

    # count rows
    # current and previous version
    dt_subscriptions.toDF().count()

    # data retention
    # retain commit history for 30 days
    # not run VACUUM, if so, lose the ability to
    # go back older than 7 days
    # configure retention period
    # delta.logRetentionDuration = "interval <interval>":
    # delta.deletedFileRetentionDuration = "interval <interval>":
    dt_plans_delta.vacuum()

    # stop session
    spark.stop()
