
import json
import os

import boto3

lambda_client = boto3.client("lambda")
FUSION_FUNCTION_NAME = os.environ["FUSION_FUNCTION_NAME"]


def lambda_handler(event, context):
    payload = json.loads(event["message"]) if isinstance(event, dict) and isinstance(event.get("message"), str) else event.get("message", event)
    lambda_client.invoke(
        FunctionName=FUSION_FUNCTION_NAME,
        InvocationType="Event",
        Payload=json.dumps(payload).encode("utf-8"),
    )
    return {"statusCode": 202, "body": json.dumps({"message": "observation accepted"})}
