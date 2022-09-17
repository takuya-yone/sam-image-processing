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

    payload = json.loads(event['body'])

    rawdata = payload['image']
    rawdata_split = rawdata.split(',')
    b64image = rawdata_split[1]
    binimage = base64.b64decode(b64image.encode("UTF-8"))

    try:
        # S3 Put Image
        s3client = boto3.client('s3')
        object_key = 'image/{}.png'.format(uuid.uuid4())
        put_res = s3client.put_object(
            Bucket=IMAGE_BUCKET_NAME,
            Body=binimage,
            Key=object_key
        )
        logger.info(put_res)

        # Generate Presigned URL
        presigned_res = s3client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': IMAGE_BUCKET_NAME, 'Key': object_key},
            ExpiresIn=300,
            HttpMethod='GET'
        )

        # Analyze Picture
        rekognition_client = boto3.client('rekognition')
        presigned_res = s3client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': IMAGE_BUCKET_NAME, 'Key': object_key},
            ExpiresIn=300,
            HttpMethod='GET'
        )

        # return response
        res = {
            "isBase64Encoded": True,
            "statusCode": 200,
            "headers": {},
            "body": json.dumps({"status": 1, "presignURL": presigned_res})
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
