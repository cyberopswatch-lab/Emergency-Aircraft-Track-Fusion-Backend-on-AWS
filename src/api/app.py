
import json
import os
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key

TRACKS_TABLE = os.environ["TRACKS_TABLE"]
OBSERVATIONS_TABLE = os.environ["OBSERVATIONS_TABLE"]

dynamodb = boto3.resource("dynamodb")
tracks_table = dynamodb.Table(TRACKS_TABLE)
observations_table = dynamodb.Table(OBSERVATIONS_TABLE)


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def response(status_code, payload):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(payload, cls=DecimalEncoder),
    }


def lambda_handler(event, context):
    path = event.get("resource", "")
    method = event.get("httpMethod", "GET")

    if path == "/health" and method == "GET":
        return response(200, {"status": "ok"})

    if path == "/tracks" and method == "GET":
        items = tracks_table.scan(Limit=100).get("Items", [])
        return response(200, {"items": items})

    if path == "/tracks/{trackId}" and method == "GET":
        track_id = event.get("pathParameters", {}).get("trackId")
        if not track_id:
            return response(400, {"message": "trackId is required"})
        track = tracks_table.get_item(Key={"trackId": track_id}).get("Item")
        obs = observations_table.query(
            KeyConditionExpression=Key("trackId").eq(track_id),
            ScanIndexForward=False,
            Limit=20,
        ).get("Items", [])
        if not track:
            return response(404, {"message": "track not found"})
        return response(200, {"track": track, "recentObservations": obs})

    return response(404, {"message": "route not found"})
