# Scope Statement

## Product scope description
The product is a serverless backend that ingests sparse aircraft observation events, stores raw observations, computes a current track estimate with confidence, and exposes responder-facing APIs.

## Deliverables
- AWS SAM template
- Lambda functions for ingest, fusion, and API delivery
- DynamoDB-backed observation and track data model
- EventBridge alert event publication
- GitHub Actions deployment workflow
- PMI-aligned documentation artifacts under `docs/`

## Acceptance criteria
- Infrastructure deploys successfully
- Health API returns `ok`
- Sample observation generates a current fused track
- Documentation is current and cross-referenced

## Exclusions
- Operational flight control functions
- Production-grade sensor integrations
- Mobile or dashboard front-end application