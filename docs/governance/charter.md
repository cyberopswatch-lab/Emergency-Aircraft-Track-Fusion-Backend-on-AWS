# Project Charter

## Project title
Emergency Aircraft Tracking Backend (AWS SAM Prototype)

## Purpose
Build a cloud-native backend that can ingest sparse aircraft observations, fuse them into a near-real-time track, and disseminate alerts and track state to authorized responders.

## Business need
Current oceanic tracking coverage may be intermittent, and a resilient event-driven backend is needed to support degraded communications and limited sensor environments.

## Measurable objectives
- Deploy a working AWS SAM stack in the selected AWS region.
- Ingest normalized observation events and persist them.
- Produce a fused current track record with confidence scoring.
- Expose read-only APIs for track retrieval and health status.
- Maintain PMI-aligned project artifacts in GitHub `docs/`.

## Success criteria
- Successful `sam build` and `sam deploy` execution.
- API health endpoint returns success.
- Sample observation updates a current track in DynamoDB.
- Risks, issues, and changes are documented and version controlled.

## High-level scope
### In scope
- AWS SAM infrastructure
- Lambda ingestion, fusion, and API handlers
- DynamoDB track and observation storage
- EventBridge alert publication
- GitHub Actions deployment workflow
- Project documentation and control artifacts

### Out of scope
- Aircraft command or flight-control takeover
- Certified operational avionics integration
- Production incident response center tooling
- Classified or export-controlled sensor integrations

## Major milestones
1. Charter approved
2. Repository and baseline documentation created
3. SAM infrastructure committed
4. GitHub OIDC deployment configured
5. First successful deployment completed
6. Monitoring and closeout artifacts completed

## Constraints
- AWS Free Tier or low-cost usage preferred
- GitHub used as source of truth for code and documents
- Prototype timeline constrained by part-time effort

## Assumptions
- AWS account and GitHub repository are available
- IAM role and OIDC federation can be configured
- Simulated observations will be sufficient for prototype validation

## High-level risks
- IAM/OIDC deployment friction
- Scope creep into autonomous control functions
- Limited time for full documentation upkeep
- Cost leakage from misconfigured services

## Key stakeholders
- Sponsor / Product Owner: CyberOpsWatch
- Project Manager: CyberOpsWatch
- Technical Lead: Dr Claude
- End users: authorized responders and technical reviewers

## Approval approach
Approval is represented by accepted pull requests to the `main` branch and milestone completion in GitHub.
