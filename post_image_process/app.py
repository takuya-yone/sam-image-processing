import json
import os
import base64
import boto3
import uuid
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Logger

tracer = Tracer()
logger = Logger()

IMAGE_BUCKET_NAME = os.environ['IMAGE_BUCKET_NAME']


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):

    # logger.info(IMAGE_BUCKET_NAME)
    payload = json.loads(event['body'])
    # logger.info(payload['image'])

    # "data:image/png;base64,iVBORw0KG"
    rawdata = payload['image']
    rawdata_split = rawdata.split(',')
    # logger.info(rawdata_split)
    b64image = rawdata_split[1]
    binimage = base64.b64decode(b64image.encode("UTF-8"))

    # S3 Put Image
    try:
        s3client = boto3.client('s3')
        object_key = 'image/{}.png'.format(uuid.uuid4())
        put_res = s3client.put_object(
            Bucket=IMAGE_BUCKET_NAME,
            Body=binimage,
            Key=object_key
        )
        logger.info(put_res)

        presign_res = s3client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': IMAGE_BUCKET_NAME, 'Key': object_key},
            ExpiresIn=300,
            HttpMethod='GET'
        )
        logger.info(presign_res)

        res = {
            "isBase64Encoded": True,
            "statusCode": 200,
            "headers": {},
            "body": json.dumps({"status": 1, "presignURL": presign_res})
        }
        return res

    except Exception as e:
        res = {
            "isBase64Encoded": True,
            "statusCode": 200,
            "headers": {},
            "body": json.dumps({"message": str(e)})
        }
        return res

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "image": binimage
            # "location": ip.text.replace("\n", "")
        }),
    }
