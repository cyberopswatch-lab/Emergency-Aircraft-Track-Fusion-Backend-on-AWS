******** Project is still in work ************
## Overview
This repository demonstrates how to design and deploy a cloud-native backend for a safety-critical tracking scenario where an aircraft may be operating over the Pacific with degraded communications and limited ground radar coverage.
The implementation is intentionally framed as a portfolio and learning project, combining AWS serverless architecture, CI/CD automation, and PMI-style project documentation in one repository.

## Objectives
	- Build a working serverless backend using AWS SAM and AWS Free Tier friendly services. 
	- Deploy the application from GitHub to AWS using GitHub Actions. 
	- Store and retrieve aircraft track and incident data using CRUD-style APIs. 
    - Document the project using project management artifacts aligned to PMI principles. 
	- Create a portfolio-ready example that demonstrates architecture, planning, and delivery discipline.
	
## Architecture 
	The backend is designed around a lightweight serverless pattern:
	- API Gateway HTTP API for HTTPS endpoints.
	- AWS Lambda for ingestion, fusion, retrieval, and notification logic.
	- Amazon DynamoDB for current aircraft track state and incident records.
	- Amazon EventBridge for event-driven fan-out and workflow decoupling.
	- Amazon S3 for optional archival of raw observation payloads and reports.
	- Amazon CloudWatch for logs, metrics, and operational visibility tied to Lambda and API activity.
	- GitHub Actions for CI/CD deployment of the SAM stack into AWS.
	
## Initial workflow
	1.	A simulated sensor observation is sent to the API.
	2.	A Lambda function validates and stores the event.
	3.	The fusion logic updates the latest aircraft track in DynamoDB.
	4.	EventBridge distributes state-change events to downstream consumers.
	5.	Query endpoints return the current aircraft track or incident status.
	
## Repository structure
	aircraft-track-fusion-aws/
		├── .github/
		│   └── workflows/
		│       └── deploy.yml
		├── docs/
		│   ├── architecture.md
		│   └── deployment.md
		├── events/
		│   └── sample-observation.json
		├── src/
		│   ├── api/
		│   │   └── app.py
		│   ├── fusion/
		│   │   └── app.py
		│   └── ingest/
		│       └── app.py
		├── README.md
		├── samconfig.toml
		└── template.yaml

## Project management approach

This repository is also structured as a PMP-aligned case study. The project artifacts are intended to show how PMI-style project planning can be applied to a real technical build through a charter, scope definition, work breakdown structure, risk register, schedule, stakeholder communication approach, and lessons learned documentation.
	
The GitHub repository supports both technical delivery and project management discipline by using Markdown documentation, Issues, Milestones, and GitHub Projects to track scope, tasks, and progress. GitHub recommends using repository READMEs, issue breakdown, project descriptions, and status updates to share work clearly across a project.

## Getting started
	Prerequisites
	•	AWS account with Free Tier access and an IAM user with programmatic credentials configured for deployment.
	•	Git installed locally for source control and repository operations.
	•	AWS CLI installed and configured locally.
	•	AWS SAM CLI installed locally.
	•	A GitHub repository for source control and CI/CD workflow execution.
	
## Set secrets in your GitHub Repo

	Now wire those values into GitHub as secrets so the  configure-aws-credentials  action can read them.
	-	In GitHub, go to your repo → Settings → Secrets and variables → Actions.
	-	Click “New repository secret” and create:
	-	Name:  AWS_ROLE_TO_ASSUME 
	-	Value: paste your role ARN, for example: arn:aws:iam::123456789012:role/github-actions-aircraft-track-fusion 
	-	Name:  AWS_REGION 
	-	Value: your region string, e.g.: us-east-1  or  us-west-2 
