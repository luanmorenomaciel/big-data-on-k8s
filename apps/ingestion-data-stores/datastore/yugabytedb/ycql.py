# import libraries
import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from cassandra.cluster import Cluster
from data_requests.api_requests import Requests
from cassandra import ConsistencyLevel
from cassandra.query import BatchStatement

# get & set env
load_dotenv()
CASSANDRA_PARTITION_NUM = 10

# load variables
ycql = os.getenv("YCQL")
size = os.getenv("SIZE")

# pandas config
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# set up parameters to request from api call
params = {'size': size}
url_get_user = 'https://random-data-api.com/api/users/random_user'

# create table statement on ycql
# json fields
"""
CREATE KEYSPACE IF NOT EXISTS owshq;

CREATE TABLE IF NOT EXISTS owshq.user 
(
    id int PRIMARY KEY,
    uid text,
    first_name text,
    last_name text,
    username text,
    email text,
    gender text,
    date_of_birth text,
    user_id int,
    dt_current_timestamp timestamp
);
"""


# class to insert into datastore
class YCQL(object):

    def split_to_partitions(self, df, partition_number):
        permuted_indices = np.random.permutation(len(df))
        partitions = []
        for i in range(partition_number):
            partitions.append(df.iloc[permuted_indices[i::partition_number]])
        return partitions

    def insert_rows(self):

        # create the cluster connection
        cluster = Cluster([ycql])
        session = cluster.connect()
        print(session)

        # set keyspace
        session.set_keyspace('owshq')

        # get request [api] to store in a variable
        # using method get to retrieve data
        dt_user = Requests.api_get_request(url=url_get_user, params=params)

        # convert python list (dict)
        # use pandas dataframe to ease the insert of the data
        # select columns
        pd_df_user = pd.DataFrame.from_dict(dt_user)
        pd_df_user = pd_df_user[['id', 'uid', 'first_name', 'last_name', 'username', 'email', 'gender', 'date_of_birth']]

        # add [user_id] into dataframe
        # add [dt_current_timestamp] into dataframe
        pd_df_user['user_id'] = Requests().gen_user_id()
        pd_df_user['dt_current_timestamp'] = Requests().gen_timestamp()

        # insert into table
        # using batch operation
        prepared_query = session.prepare("INSERT INTO owshq.user(id,uid,first_name,last_name,username,email,gender,date_of_birth,user_id,dt_current_timestamp) VALUES (?,?,?,?,?,?,?,?,?,?)")
        for partition in self.split_to_partitions(pd_df_user, CASSANDRA_PARTITION_NUM):
            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
            for index, item in partition.iterrows():
                batch.add(prepared_query, (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9]))
            session.execute(batch)

        # close the connection
        cluster.shutdown()
        print(cluster)