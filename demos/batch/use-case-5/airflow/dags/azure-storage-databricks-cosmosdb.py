# [START import_module]
import time
import tempfile
import requests
import pandas as pd
import numpy as np
from requests.exceptions import HTTPError
from datetime import datetime
from airflow import DAG
from os import getenv
from os import path
from airflow.operators.python import PythonOperator
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow.providers.microsoft.azure.sensors.wasb import WasbPrefixSensor
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
# [END import_module]

# [START env_variables]
BLOB_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=brzluanmoreno;AccountKey=j+LfL1qL8y6GxUFkCriWknFUPzaWeyJKETnqfHVRG9kKvGA5Wsd4xGi8tQ8QHrvGFtueDdtuigibtyJxpCHCwg==;EndpointSuffix=core.windows.net"
CONTAINER_LANDING_ZONE = getenv("CONTAINER_LANDING_ZONE", "landing")
CONTAINER_PROCESSING_ZONE = getenv("CONTAINER_PROCESSING_ZONE", "processing")
CONTAINER_CURATED_ZONE = getenv("CONTAINER_CURATED_ZONE", "curated")
COSMOSDB_ENDPOINT = getenv("COSMOSDB_ENDPOINT", "https://pythian.documents.azure.com:443/")
COSMOSDB_PRIMARY_KEY = getenv("COSMOSDB_PRIMARY_KEY", "o6o58lfQZqQBQJYfOzrTifNGIuwSwi71k2Q76GsYM38XZbUTDIYZnLwog41RN4IibfcKvb7kLfGI7NVri84u0Q==")
# [END env_variables]


# [START functions]
def request_data_from_api(url, amount, entity):
    # prepare api request to retrieve data
    # amount of rows retrieved from the api call
    dt_request = requests.get(url=url, params={'size': amount})

    # formatting into a dictionary
    # get data from site
    for url in [url]:
        try:
            # call service and get response
            response = requests.get(url)
            response.raise_for_status()
            dict_request = dt_request.json()

            # cast into a pandas dataframe
            # add new columns into the set
            pd_df_dt = pd.DataFrame.from_dict(dict_request)
            pd_df_dt['user_id'] = np.random.randint(1, 10000, size=100)
            pd_df_dt['dt_current_timestamp'] = datetime.now()

            # write response from api into temp location
            # file stored as json format
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_path = path.join(tmp_dir, entity)
                print(tmp_path)
                pd_df_dt.to_json(tmp_path, orient="records")

                # upload file to azure blob storage
                # set up file name and additional info
                # get file name
                year = datetime.today().year
                month = datetime.today().month
                day = datetime.today().day
                hour = datetime.today().hour
                minute = datetime.today().minute
                second = datetime.today().second
                file_name = entity + f'/{entity}_{year}_{month}_{day}_{hour}_{minute}_{second}.json'

                # using hook to connect into azure
                # instantiate microsoft azure hook
                hook = WasbHook(wasb_conn_id="azure_blob_storage")
                hook.load_file(tmp_path, container_name=CONTAINER_LANDING_ZONE, blob_name=file_name)

        # verify error messages
        except HTTPError as http_err:
            print(f'http error occurred: {http_err}')
        except Exception as err:
            print(f'api not available at this moment.: {err}')
        else:
            return dict_request
# [END functions]


# [START default_args]
default_args = {
    'owner': 'luan moreno m. maciel',
    'depends_on_past': False,
    'email': ['luan.moreno@owshq.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1}
# [END default_args]

# [START instantiate_dag]
with DAG(
    dag_id="azure-storage-databricks-cosmosdb",
    tags=['development', 'blob storage', 'azure databricks', 'cosmosdb'],
    default_args=default_args,
    start_date=datetime(year=2021, month=7, day=7),
    schedule_interval='@daily',
    catchup=False
) as dag:
# [END instantiate_dag]

# [START set_tasks]
    # retrieve users data
    fetch_users_from_api = PythonOperator(
        task_id="fetch_users_from_api",
        python_callable=request_data_from_api,
        op_kwargs={"url": "https://random-data-api.com/api/users/random_user", "amount": "100", "entity": "users"}
    )

    # retrieve vehicle data
    fetch_vehicles_from_api = PythonOperator(
        task_id="fetch_vehicles_from_api",
        python_callable=request_data_from_api,
        op_kwargs={"url": "https://random-data-api.com/api/vehicle/random_vehicle", "amount": "100", "entity": "vehicles"}
    )

    # sensor for users file
    # 30 minutes delay
    verify_users_blob_storage_sensor = WasbPrefixSensor(
        task_id="verify_users_blob_storage_sensor",
        wasb_conn_id="azure_blob_storage",
        container_name=CONTAINER_LANDING_ZONE,
        prefix='users/',
        timeout=18 * 60 * 60,
        poke_interval=1800
    )

    # sensor for vehicle file
    # 30 minutes delay
    verify_vehicles_blob_storage_sensor = WasbPrefixSensor(
        task_id="verify_vehicles_blob_storage_sensor",
        wasb_conn_id="azure_blob_storage",
        container_name=CONTAINER_LANDING_ZONE,
        prefix='vehicles/',
        timeout=18 * 60 * 60,
        poke_interval=1800
    )

    # read json from landing and appending into parquet on processing [delete from landing]
    # https://adb-8595678128214529.9.azuredatabricks.net/?o=8595678128214529#notebook/2738532016558517/command/2738532016558519
    dbr_notebook_json2parquet = {"notebook_path": "/Users/luanmorenomaciel@hotmail.com/orchestrator-engine/convert_json2parquet_to_processing_zone"}
    json2parquet_landing_to_processing_spark = DatabricksSubmitRunOperator(
        task_id="json2parquet_landing_to_processing_spark",
        databricks_conn_id="azure_databricks",
        existing_cluster_id="0503-151934-hare458",
        notebook_task=dbr_notebook_json2parquet
    )

    # apply business logic to process users and vehicle using spark's engine
    # https://adb-8595678128214529.9.azuredatabricks.net/?o=8595678128214529#notebook/1153292904904631/command/1153292904904641
    dbr_notebook_users_vehicles = {"notebook_path": "/Users/luanmorenomaciel@hotmail.com/orchestrator-engine/process_users_vehicles_logic"}
    process_users_vehicles_logic_spark = DatabricksSubmitRunOperator(
        task_id="process_users_vehicles_logic_spark",
        databricks_conn_id="azure_databricks",
        existing_cluster_id="0503-151934-hare458",
        notebook_task=dbr_notebook_users_vehicles
    )

    # read from curated zone and ingest into cosmosdb collection
    # https://adb-8595678128214529.9.azuredatabricks.net/?o=8595678128214529#notebook/2849104490601336/command/2849104490601342
    dbr_notebook_insert_cosmosdb = {"notebook_path": "/Users/luanmorenomaciel@hotmail.com/orchestrator-engine/insert_cosmosdb_data"}
    insert_cosmosdb_sql_api_call_spark = DatabricksSubmitRunOperator(
        task_id="insert_cosmosdb_sql_api_call_spark",
        databricks_conn_id="azure_databricks",
        existing_cluster_id="0707-185800-meant244",
        notebook_task=dbr_notebook_insert_cosmosdb
    )
# [END set_tasks]

# [START task_sequence]
[fetch_users_from_api >> verify_users_blob_storage_sensor, fetch_vehicles_from_api >> verify_vehicles_blob_storage_sensor] >> json2parquet_landing_to_processing_spark >> process_users_vehicles_logic_spark >> insert_cosmosdb_sql_api_call_spark
# [END task_sequence]