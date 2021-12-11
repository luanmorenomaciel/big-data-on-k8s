# import libraries
from pyspark.sql import SparkSession
from pyspark import SparkConf

# main spark program
# init application
if __name__ == '__main__':

    # init session
    # set configs
    spark = SparkSession \
        .builder \
        .appName("write-bg-formats-py") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://20.62.75.137") \
        .config("spark.hadoop.fs.s3a.access.key", "H4aQRS39OITgclWk") \
        .config("spark.hadoop.fs.s3a.secret.key", "wRozzyetjvRrVQS9qpIzFVnimQFm9CqW") \
        .config("spark.hadoop.fs.s3a.path.style.access", True) \
        .config("spark.hadoop.fs.s3a.fast.upload", True) \
        .config("spark.hadoop.fs.s3a.multipart.size", 104857600) \
        .config("fs.s3a.connection.maximum", 100) \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore") \
        .config("spark.memory.fraction", 0.8) \
        .config("spark.executor.memory", "8g") \
        .config("spark.driver.memory", "8g") \
        .config("spark.sql.shuffle.partitions", "800") \
        .config("spark.memory.offHeap.enabled", 'true') \
        .config("spark.memory.offHeap.size", "8g") \
        .getOrCreate()

    # show configured parameters
    print(SparkConf().getAll())

    # set log level
    spark.sparkContext.setLogLevel("INFO")

    # read file [local storage]
    get_ds_gold_reviews = "/Users/luanmorenomaciel/BitBucket/big-data-on-k8s/demos/batch/use-case-4/dataset/ds_gold_reviews"
    df_gold_reviews = spark.read.parquet(get_ds_gold_reviews)

    # get number of partitions
    # count amount of rows
    print(df_gold_reviews.rdd.getNumPartitions())
    df_gold_reviews.count()

    # [write into minio]

    # apache parquet format
    df_gold_reviews.write.mode("overwrite").parquet("s3a://files/parquet/gold_reviews")

    # apache orc format
    df_gold_reviews.write.mode("overwrite").orc("s3a://files/orc/gold_reviews")

    # stop session
    spark.stop()
