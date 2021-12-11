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
class CreditCard(object):

    # explicitly declare all schema members
    __slots__ = [
                    "uuid",
                    "user_id",
                    "provider",
                    "number",
                    "expire_data",
                    "security_code",
                    "dt_current_timestamp"
                ]

    # define init
    def __init__(self):

        self.uuid = fake.uuid4()
        self.user_id = randint(0, 1000)
        self.provider = fake.credit_card_provider()
        self.number = fake.credit_card_number()
        self.expire_data = fake.credit_card_expire()
        self.security_code = fake.credit_card_security_code()
        self.dt_current_timestamp = datetime.now()

    # dict [output] = to_dict_rows
    def to_dict_rows(self):

        return {
            "uuid": self.uuid,
            "user_id": self.user_id,
            "provider": self.provider,
            "number": self.number,
            "expire_data": self.expire_data,
            "security_code": self.security_code,
            "dt_current_timestamp": self.dt_current_timestamp
        }

    # dict [output] = to_dict_events
    def to_dict_events(self):

        return {
            "uuid": self.uuid,
            "user_id": self.user_id,
            "provider": self.provider,
            "number": str(self.number),
            "expire_data": self.expire_data,
            "security_code": self.security_code,
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
                "provider": fake.credit_card_provider(),
                "number": fake.credit_card_number(),
                "expire_data": fake.credit_card_expire(),
                "security_code": fake.credit_card_security_code(),
                "dt_current_timestamp": str(datetime.now())
            }
            # append each run into a list of dictionaries
            list_return_data.append(get_faker_dt)
            i += 1

        # convert list to pandas dataframe
        df_list_data = pd.DataFrame(list_return_data)
        return_dt = df_list_data.to_dict('records')
        return return_dt
