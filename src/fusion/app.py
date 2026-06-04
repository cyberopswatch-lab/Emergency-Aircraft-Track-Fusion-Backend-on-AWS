import json
import math
import os
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import boto3

TRACKS_TABLE = os.environ["TRACKS_TABLE"]
OBSERVATIONS_TABLE = os.environ["OBSERVATIONS_TABLE"]
EVENT_BUS_NAME = os.environ["EVENT_BUS_NAME"]

dynamodb = boto3.resource("dynamodb")
tracks_table = dynamodb.Table(TRACKS_TABLE)
observations_table = dynamodb.Table(OBSERVATIONS_TABLE)
events = boto3.client("events")


def now_utc():
    return datetime.now(timezone.utc)


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def to_decimal(value):
    if value is None:
        return None
    return Decimal(str(value))


def ttl_days(days: int = 7) -> int:
    return int((now_utc() + timedelta(days=days)).timestamp())


def haversine_nm(lat1, lon1, lat2, lon2):
    r_km = 6371.0
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    km = r_km * c
    return km * 0.539957


def blend(previous, current, weight):
    return (previous * (1 - weight)) + (current * weight)


def normalize(event):
    if "Records" in event:
        body = json.loads(event["Records"][0]["body"])
    elif "body" in event:
        body = json.loads(event["body"]) if isinstance(event["body"], str) else event["body"]
    else:
        body = event
    required = ["trackId", "source", "observationTs", "lat", "lon", "altitudeFt", "speedKt", "headingDeg"]
    for key in required:
        if key not in body:
            raise ValueError(f"Missing required field: {key}")
    body.setdefault("quality", 0.7)
    return body


def publish_alert(detail_type, payload):
    events.put_events(
        Entries=[
            {
                "Source": "aircraft.trackfusion",
                "DetailType": detail_type,
                "Detail": json.dumps(payload),
                "EventBusName": EVENT_BUS_NAME,
            }
        ]
    )


def lambda_handler(event, context):
    obs = normalize(event)
    track_id = obs["trackId"]
    quality = float(obs.get("quality", 0.7))
    weight = min(max(quality, 0.2), 0.95)

    observations_table.put_item(
        Item={
            "trackId": track_id,
            "observationTs": obs["observationTs"],
            "source": obs["source"],
            "lat": to_decimal(obs["lat"]),
            "lon": to_decimal(obs["lon"]),
            "altitudeFt": to_decimal(obs["altitudeFt"]),
            "speedKt": to_decimal(obs["speedKt"]),
            "headingDeg": to_decimal(obs["headingDeg"]),
            "quality": to_decimal(obs["quality"]),
            "ttl": ttl_days(7),
            "rawPayload": json.dumps(obs),
        }
    )

    current = tracks_table.get_item(Key={"trackId": track_id}).get("Item")
    if not current:
        estimate = {
            "trackId": track_id,
            "lastUpdateTs": obs["observationTs"],
            "estLat": to_decimal(obs["lat"]),
            "estLon": to_decimal(obs["lon"]),
            "estAltitudeFt": to_decimal(obs["altitudeFt"]),
            "estSpeedKt": to_decimal(obs["speedKt"]),
            "estHeadingDeg": to_decimal(obs["headingDeg"]),
            "confidenceScore": to_decimal(round(quality, 3)),
            "uncertaintyNm": to_decimal(round((1 - quality) * 20, 3)),
            "status": "TRACKING",
            "erraticFlag": False,
            "fuelEmergencyFlag": bool(obs.get("fuelEmergencyFlag", False)),
            "sources": [obs["source"]],
        }
    else:
        prev_lat = float(current["estLat"])
        prev_lon = float(current["estLon"])
        prev_alt = float(current["estAltitudeFt"])
        prev_spd = float(current["estSpeedKt"])
        prev_hdg = float(current["estHeadingDeg"])
        distance_nm = haversine_nm(prev_lat, prev_lon, obs["lat"], obs["lon"])
        heading_change = abs(prev_hdg - float(obs["headingDeg"]))
        heading_change = min(heading_change, 360 - heading_change)
        altitude_change = abs(prev_alt - float(obs["altitudeFt"]))
        erratic = distance_nm > 30 or heading_change > 45 or altitude_change > 3000
        confidence = max(0.05, min(0.99, (float(current["confidenceScore"]) * 0.55) + (quality * 0.45) - (0.1 if erratic else 0.0)))
        estimate = {
            "trackId": track_id,
            "lastUpdateTs": obs["observationTs"],
            "estLat": to_decimal(round(blend(prev_lat, float(obs["lat"]), weight), 6)),
            "estLon": to_decimal(round(blend(prev_lon, float(obs["lon"]), weight), 6)),
            "estAltitudeFt": to_decimal(round(blend(prev_alt, float(obs["altitudeFt"]), weight), 1)),
            "estSpeedKt": to_decimal(round(blend(prev_spd, float(obs["speedKt"]), weight), 1)),
            "estHeadingDeg": to_decimal(round(blend(prev_hdg, float(obs["headingDeg"]), weight), 1)),
            "confidenceScore": to_decimal(round(confidence, 3)),
            "uncertaintyNm": to_decimal(round(max(1.0, (1 - confidence) * 40), 3)),
            "status": "TRACKING" if confidence >= 0.4 else "DEGRADED",
            "erraticFlag": erratic,
            "fuelEmergencyFlag": bool(obs.get("fuelEmergencyFlag", False)),
            "sources": sorted(list(set(current.get("sources", []) + [obs["source"]]))),
        }
        if erratic:
            publish_alert("aircraft.erratic", {"trackId": track_id, "observationTs": obs["observationTs"]})
        if confidence < 0.4:
            publish_alert("track.confidence.low", {"trackId": track_id, "confidenceScore": confidence})

    tracks_table.put_item(Item=estimate)
    return {"statusCode": 200, "body": json.dumps({"message": "track updated", "trackId": track_id}, default=str)}
