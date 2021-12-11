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
class Agent(object):

    # explicitly declare all schema members
    __slots__ = [
                    "uuid",
                    "user_id",
                    "platform",
                    "email",
                    "domain",
                    "hostname",
                    "method",
                    "url",
                    "ipv4",
                    "port_number",
                    "mac_address",
                    "dt_current_timestamp"
                ]

    # define init
    def __init__(self):

        self.uuid = fake.uuid4()
        self.user_id = randint(0, 1000)
        self.platform = fake.user_agent()
        self.email = fake.company_email()
        self.domain = fake.domain_name()
        self.hostname = fake.hostname()
        self.method = fake.http_method()
        self.url = fake.url()
        self.ipv4 = fake.ipv4()
        self.port_number = fake.port_number()
        self.mac_address = fake.mac_address()
        self.dt_current_timestamp = datetime.now()

    # dict [output] = to_dict_rows
    def to_dict_rows(self):

        return {
            "uuid": self.uuid,
            "user_id": self.user_id,
            "platform": self.platform,
            "email": self.email,
            "domain": self.domain,
            "hostname": self.hostname,
            "method": self.method,
            "url": self.url,
            "ipv4": self.ipv4,
            "port_number": self.port_number,
            "mac_address": self.mac_address,
            "dt_current_timestamp": self.dt_current_timestamp
        }

    # dict [output] = to_dict_events
    def to_dict_events(self):

        return {
            "uuid": self.uuid,
            "user_id": self.user_id,
            "platform": self.platform,
            "email": self.email,
            "domain": self.domain,
            "hostname": self.hostname,
            "method": self.method,
            "url": self.url,
            "ipv4": self.ipv4,
            "port_number": str(self.port_number),
            "mac_address": self.mac_address,
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
                "uuid": fake.uuid4(),
                "user_id": randint(0, 1000),
                "platform": fake.user_agent(),
                "email": fake.company_email(),
                "domain": fake.domain_name(),
                "hostname": fake.hostname(),
                "method": fake.http_method(),
                "url": fake.url(),
                "ipv4": fake.ipv4(),
                "port_number": str(fake.port_number()),
                "mac_address": fake.mac_address(),
                "dt_current_timestamp": str(datetime.now())
            }
            # append each run into a list of dictionaries
            list_return_data.append(get_faker_dt)
            i += 1

        # convert list to pandas dataframe
        df_list_data = pd.DataFrame(list_return_data)
        return_dt = df_list_data.to_dict('records')
        return return_dt
