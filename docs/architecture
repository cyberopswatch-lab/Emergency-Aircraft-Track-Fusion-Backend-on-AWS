## `docs/architecture.md`

```md
# Architecture

This repository provisions a serverless aircraft track-fusion backend on AWS SAM.

## Components
- AWS IoT Core or another publisher sends normalized observation events.
- The ingest Lambda receives observations and forwards them asynchronously to the fusion Lambda.
- The fusion Lambda stores raw observations in DynamoDB, updates the current fused track, and emits alert events to EventBridge.
- API Gateway exposes read-only operational endpoints for tracks and health checks.
- GitHub Actions builds and deploys the stack with SAM.

## Data flow
1. Observation published.
2. Ingest function validates handoff.
3. Fusion function stores the observation.
4. Fusion function updates current track estimate.
5. EventBridge emits degraded confidence or erratic-flight events.
6. API clients query the current operational picture.
