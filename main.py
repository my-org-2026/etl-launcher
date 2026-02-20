from google.cloud import pubsub_v1
from bigquery_checker.check import BigQueryClient
import json
from utils.settings import settings
from utils.logger import logger


def main(request):
    launcher = BigQueryClient()
    missing_dates = launcher.get_missing_dates_from_bigquery()
    if not missing_dates:
        logger.info("Missing dates do not exist")
        return {"info": "missing dates do not exist"}

    topic_id = settings.TOPIC_ID
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(settings.PROJECT_ID, topic_id)


    logger.info("Missing dates", missing_dates)

    futures = []

    for date in missing_dates:
        message = {
            "start_date": date,
            "end_date": date
        }

        logger.info("Publishing:", message)

        message_bytes = json.dumps(message).encode("utf-8   ")
        future = publisher.publish(topic_path, message_bytes)
        futures.append(future)

    for future in futures:
        logger.info(future.result())

    return {"success"}, 200
