# Project Management Plan

## Delivery approach
Hybrid approach with predictive planning for governance artifacts and iterative delivery for technical implementation.

## Scope management
The approved scope is defined by the charter, repository structure, SAM template, Lambda services, monitoring artifacts, and supporting documentation. Scope changes require an entry in the change log and approval through pull request review.

## Schedule management
Work is organized into milestone-based increments:
1. Initiation and repo setup
2. Core infrastructure deployment
3. Tracking logic and API completion
4. Monitoring and control artifacts
5. Closeout and lessons learned

## Cost management
Use AWS Free Tier-friendly defaults where possible, prefer pay-per-request services, review CloudWatch and service usage weekly, and log cost decisions in status reports.

## Quality management
Definition of done includes successful build, deploy, sample event processing, documentation updates, and peer/self review of changed artifacts.

## Resource management
The current project uses a single accountable owner with multiple roles. If contributors are added later, responsibilities will be tracked through the RACI matrix.

## Communications management
- Weekly status report in `docs/monitoring/status-report.md`
- Risks, issues, assumptions, and changes updated after significant events
- Pull requests used for approval history and change discussions

## Risk management
Risks are logged in the risk register with probability, impact, owner, and response strategy. Review weekly.

## Procurement management
No external procurement is planned for the prototype. Third-party services or datasets require documentation before use.

## Stakeholder engagement
Stakeholder register and communications cadence govern engagement and expectation management.
