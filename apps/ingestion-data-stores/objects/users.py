# import libraries
from random import randint
from datetime import datetime
from faker import Faker
import pandas as pd

# set faker class
fake = Faker()

# get seed
Faker.seed(randint(0, 10000000000))


# tester class
class Users(object):

    # explicitly declare all schema members
    __slots__ = [
                    "user_id",
                    "uuid",
                    "first_name",
                    "last_name",
                    "date_birth",
                    "city",
                    "country",
                    "company_name",
                    "job",
                    "phone_number",
                    "last_access_time",
                    "time_zone",
                    "dt_current_timestamp"
                ]

    # define init 
    def __init__(self):

        self.user_id = randint(0, 1000)
        self.uuid = fake.uuid4()
        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.date_birth = fake.date_of_birth()
        self.city = fake.city()
        self.country = fake.country()
        self.company_name = fake.company()
        self.job = fake.job()
        self.phone_number = fake.phone_number()
        self.last_access_time = fake.iso8601()
        self.time_zone = fake.timezone()
        self.dt_current_timestamp = datetime.now()

    # dict [output] = to_dict_rows
    def to_dict_rows(self):

        return {
            "user_id": self.user_id,
            "uuid": self.uuid,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_birth": self.date_birth,
            "city": self.city,
            "country": self.country,
            "company_name": self.company_name,
            "job": self.job,
            "phone_number": self.phone_number,
            "last_access_time": self.last_access_time,
            "time_zone": self.time_zone,
            "dt_current_timestamp": self.dt_current_timestamp
        }

    # dict [output] = to_dict_events
    def to_dict_events(self):

        return {
            "user_id": self.user_id,
            "uuid": self.uuid,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_birth": str(self.date_birth),
            "city": self.city,
            "country": self.country,
            "company_name": self.company_name,
            "job": self.job,
            "phone_number": self.phone_number,
            "last_access_time": self.last_access_time,
            "time_zone": self.time_zone,
            "dt_current_timestamp": str(self.dt_current_timestamp)
        }

    # request multiple rows (events) at a time
    @staticmethod
    def get_multiple_rows(gen_dt_rows):

        # set init variables
        i = 0
        list_return_data = []
        while i < int(gen_dt_rows):

            # generate faker data
            get_faker_dt = {
                "user_id": randint(0, 1000),
                "uuid": fake.uuid4(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "date_birth": str(fake.date_of_birth()),
                "city": fake.city(),
                "country": fake.country(),
                "company_name": fake.company(),
                "job": fake.job(),
                "phone_number": fake.phone_number(),
                "last_access_time": fake.iso8601(),
                "time_zone": fake.timezone(),
                "dt_current_timestamp": str(datetime.now())
            }
            # append each run into a list of dictionaries
            list_return_data.append(get_faker_dt)
            i += 1

        # convert list to pandas dataframe
        df_list_data = pd.DataFrame(list_return_data)
        return_dt = df_list_data.to_dict('records')
        return return_dt

    # log compaction demo
    @staticmethod
    def log_compaction(gen_dt_rows):

        # set init variables
        i = 0
        list_return_data = []
        while i < int(gen_dt_rows):
            # generate faker data
            get_faker_dt = {
                "user_id": randint(0, 100),
                "uuid": fake.uuid4(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "date_birth": str(fake.date_of_birth()),
                "city": fake.city(),
                "country": fake.country(),
                "company_name": fake.company(),
                "job": fake.job(),
                "phone_number": fake.phone_number(),
                "last_access_time": fake.iso8601(),
                "time_zone": fake.timezone(),
                "dt_current_timestamp": str(datetime.now())
            }
            # append each run into a list of dictionaries
            list_return_data.append(get_faker_dt)
            i += 1

        # convert list to pandas dataframe
        df_list_data = pd.DataFrame(list_return_data)
        return_dt = df_list_data.to_dict('records')
        return return_dt