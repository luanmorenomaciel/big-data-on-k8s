# import libraries
from faust import Record


# schema of event [src-app-rides-json]
class RidesEvent(Record, serializer='json'):
    user_id: int
    time_stamp: int
    source: str
    destination: str
    distance: float
    price: float
    surge_multiplier: int
    id: str
    product_id: str
    name: str
    cab_type: str
    dt_current_timestamp: str

