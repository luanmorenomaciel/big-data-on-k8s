# import libraries
import logging
from src.app import app, get_input_topic_src_app_rides_json

# add logging capabilities
logger = logging.getLogger(__name__)


# read raw data [event]
# src-app-rides-json
@app.agent(get_input_topic_src_app_rides_json)
async def event_stream_rides(events):
    async for event in events:
        logger.info(event)