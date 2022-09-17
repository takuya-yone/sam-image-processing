import json
import os
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Logger

tracer = Tracer()
logger = Logger()

IMAGE_BUCKET_NAME = os.environ['IMAGE_BUCKET_NAME']


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):

    logger.info(IMAGE_BUCKET_NAME)
    logger.info(event)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
