# https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html

# custom xcom backends = s3, gcs, hdfs and blob storage

# get data from api
# get data from relational database sql server
# get data from nosql db mongodb

# [START import_module]
from airflow import DAG
from airflow.operators.python import PythonOperator
# [END import_module]