# AWS CloudTrail Security Alerting System

This project monitors an AWS account and sends email alerts whenever 
someone logs into the console.

Three versions of the same system were built. The first was set up 
manually in the AWS console to understand how the services work 
together. The second was rebuilt using Terraform so it can be deployed 
quickly from scratch. The third adds a CI/CD pipeline so the 
infrastructure deploys automatically on every push to GitHub.


## Version 1 — Manual Setup

This version is in the manual folder.

CloudTrail, S3, Lambda and SNS were configured directly in the AWS 
console. This was useful for understanding what each service does and 
how they connect to each other before writing any code.


## Version 2 — Terraform

This version is in the terraform folder.

The same system was rebuilt using Terraform. Manual setup is hard to 
repeat and easy to get wrong. With Terraform everything is written as 
code and can be deployed or torn down with one command.


## Version 3 — CI/CD Pipeline with GitHub Actions

A GitHub Actions pipeline was added so the infrastructure deploys 
automatically whenever code is pushed to the main branch. No need to 
run terraform apply manually anymore.

The pipeline runs these steps every time:

1. Terraform Init — connects to the S3 backend and downloads providers
2. Terraform Validate — checks the code for errors
3. Terraform Plan — shows what will change before touching anything
4. Terraform Apply — deploys the changes to AWS

On pull requests the pipeline runs everything except apply. This means 
changes can be reviewed before they go live.

AWS credentials are stored as GitHub Secrets so they never appear in 
the code. The Terraform state file is kept in a private S3 bucket so 
the pipeline can access it from anywhere.


## How It Works

CloudTrail records every action in the AWS account and saves the logs 
to S3. When a new log file arrives it triggers a Lambda function. The 
Lambda opens the file, looks for console login events and sends an 
email alert through SNS with the details.


## Full Architecture

Developer pushes code to GitHub
↓
GitHub Actions pipeline triggers
↓
Terraform Init → Validate → Plan → Apply
↓
AWS infrastructure deployed automatically
↓
CloudTrail → S3 → Lambda → SNS → Email alert


## Services Used

- AWS CloudTrail
- Amazon S3
- AWS Lambda (Python 3.12)
- Amazon SNS
- AWS IAM
- Terraform
- GitHub Actions


## Security Decisions

- The Lambda role can only read from S3 and publish to SNS
- The S3 bucket is private with all public access blocked
- CloudTrail log validation is turned on to detect any tampering
- The SNS topic ARN is passed as an environment variable and never 
  written directly in the code
- AWS credentials are kept in GitHub Secrets and never stored in 
  the repository


## Sample Alert

<img width="1179" height="1838" alt="secure alert" src="https://github.com/user-attachments/assets/714ae59c-6fd3-45c8-a00f-81c7c2a3bf4b" />
<img width="1179" height="2293" alt="secure-alert2 png" src="https://github.com/user-attachments/assets/a11239fb-50db-409f-a184-6e2ce229893b" />

The alert arrives a few minutes after a login. It shows the username, 
IP address, region, MFA status and the time of the event.


## How to Deploy

Terraform and the AWS CLI need to be installed before starting.

1. Clone this repo
2. Run aws configure and enter your AWS credentials
3. Create a terraform.tfvars file with your details:

alert_email  = abrahamsheye1@gmail.com
project_name = cloudtrail-security

4. Run:

terraform init
terraform plan
terraform apply

5. Confirm the SNS subscription email that gets sent to your inbox
6. Log out and back into AWS to trigger a test alert

To use the pipeline just push any change to the main branch and 
GitHub Actions will handle the rest automatically.


## Cost

Runs within the AWS Free Tier. The monthly cost at low usage is 
effectively zero.


## What Was Learned

Building the manual version first made everything easier. By the time 
Terraform was introduced it was already clear what each resource needed 
and why.

Writing IAM policies from scratch helped with understanding least 
privilege in a practical way rather than just reading about it.

The CI/CD pipeline showed how infrastructure deployments work in real 
teams. Every change goes through the same automated steps which keeps 
things consistent and reduces mistakes.