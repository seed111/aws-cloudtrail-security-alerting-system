## AWS CloudTrail Security Alerting System

This project monitors an AWS account and sends email alerts whenever someone logs into the console. The live infrastructure can be deployed from scratch in under five minutes using Terraform and torn down just as easily to avoid unnecessary AWS costs.

Three versions of the same system were built. The first was set up manually in the AWS console to understand how the services work together. The second was rebuilt using Terraform so it can be deployed quickly from scratch. The third adds a CI/CD pipeline so the infrastructure deploys automatically on every push to GitHub.


## Version 1 — Manual Setup

This version is in the manual folder.

CloudTrail, S3, Lambda and SNS were configured directly in the AWS console. This was useful for understanding what each service does and how they connect to each other before writing any code.


## Version 2 — Terraform

This version is in the terraform folder.

The same system was rebuilt using Terraform. Manual setup is hard to repeat and easy to get wrong. With Terraform everything is written as code and can be deployed or torn down with one command.


## Version 3 — CI/CD Pipeline with GitHub Actions

A GitHub Actions pipeline was added so the infrastructure deploys automatically whenever code is pushed to the main branch. No need to run terraform apply manually anymore.

The pipeline runs these steps every time:

1. Terraform Init — connects to the S3 backend and downloads providers
2. Terraform Validate — checks the code for errors
3. Terraform Plan — shows what will change before touching anything
4. Terraform Apply — deploys the changes to AWS

On pull requests the pipeline runs everything except apply. This means changes can be reviewed before they go live.

AWS credentials are stored as GitHub Secrets so they never appear in the code. The Terraform state file is kept in a private S3 bucket so the pipeline can access it from anywhere.


## How It Works

AWS CloudTrail sits at the entry point of the system. It watches every action happening in the AWS account and automatically saves detailed log files to an Amazon S3 bucket. Every login attempt, API call and console access gets recorded here.

When a new log file lands in the S3 bucket it immediately triggers an AWS Lambda function. Lambda is the brain of the system. It opens the log file, reads through the events and looks specifically for console login events. When it finds one it pulls out the important details including the username, IP address, region, MFA status and the exact time of the event.

Lambda then passes all of this information to Amazon SNS which handles the email delivery. SNS sends the alert straight to the configured email address within a few minutes of the login happening.

AWS IAM controls the permissions across the whole system. The Lambda function has a dedicated IAM role that gives it just enough access to read from S3 and publish to SNS and nothing more. This follows the principle of least privilege which means even if something went wrong the damage would be limited.

Terraform manages all of this infrastructure as code. Every resource including the CloudTrail trail, the S3 bucket, the Lambda function, the SNS topic and the IAM roles are all defined in Terraform files. The entire system can be deployed from scratch with one command or torn down just as easily.

GitHub Actions automates the deployment process. Every time code is pushed to the main branch the pipeline runs through Terraform init, validate, plan and apply automatically. No manual steps are needed.


## Full Architecture

```
Developer pushes code to GitHub
↓
GitHub Actions pipeline triggers
↓
Terraform Init → Validate → Plan → Apply
↓
AWS infrastructure deployed automatically
↓
CloudTrail → S3 → Lambda → SNS → Email alert
```


## Services Used

**AWS CloudTrail** — records every action in the AWS account and saves logs to S3

**Amazon S3** — stores the CloudTrail log files and also holds the Terraform remote state

**AWS Lambda Python 3.12** — reads the log files, detects login events and triggers the alert

**Amazon SNS** — sends the email alert with all the login details to the configured address

**AWS IAM** — controls permissions across all services using least privilege roles

**Terraform** — defines and deploys all the infrastructure as code

**GitHub Actions** — automates the full deployment pipeline on every push to main


## IAM Roles and Privileges

Three IAM roles were created for this system. Each one has only the permissions it needs and nothing more.

**Lambda Execution Role**

This is the role the Lambda function uses when it runs. It needs three things. First it needs permission to read log files from the specific S3 bucket where CloudTrail saves them. This is granted using s3:GetObject scoped to that bucket only. Second it needs permission to publish messages to the SNS topic so it can send the email alert. This is granted using sns:Publish scoped to that specific SNS topic ARN. Third it needs permission to write its own logs to CloudWatch so errors and execution details can be monitored. This is granted using logs:CreateLogGroup, logs:CreateLogStream and logs:PutLogEvents.

**CloudTrail Role**

CloudTrail needs permission to write log files to the S3 bucket. This is granted using s3:PutObject scoped to the specific bucket and path where CloudTrail saves its logs. CloudTrail also needs s3:GetBucketAcl to verify it has the correct access before it starts writing.

**GitHub Actions Role**

The CI/CD pipeline needs permission to create, update and destroy all the AWS resources that Terraform manages. This includes permissions for CloudTrail, S3, Lambda, SNS, IAM and CloudWatch. In a production environment this role would be scoped tightly to only the resources in this project. For this personal project the role uses broader permissions to keep things simple during development.

**What Was Not Granted**

Lambda cannot write to S3, cannot delete anything, cannot access any other bucket or SNS topic outside of this project, and cannot make any changes to IAM. This limits the blast radius significantly if the function were ever compromised.


## Security Decisions

The Lambda role can only read from S3 and publish to SNS. The S3 bucket is private with all public access blocked. CloudTrail log validation is turned on to detect any tampering. The SNS topic ARN is passed as an environment variable and never written directly in the code. AWS credentials are kept in GitHub Secrets and never stored in the repository.


## Sample Alert

<img width="1179" height="1838" alt="secure alert" src="https://github.com/user-attachments/assets/714ae59c-6fd3-45c8-a00f-81c7c2a3bf4b" />
<img width="1179" height="2293" alt="secure-alert2 png" src="https://github.com/user-attachments/assets/a11239fb-50db-409f-a184-6e2ce229893b" />

The alert arrives a few minutes after a login. It shows the username, IP address, region, MFA status and the time of the event.


## How to Deploy

Terraform and the AWS CLI need to be installed before starting.

1. Clone this repo
2. Run aws configure and enter your AWS credentials
3. Create a terraform.tfvars file with your details:

```
alert_email  = abrahamsheye1@gmail.com
project_name = cloudtrail-security
```

4. Run the following commands:

```bash
terraform init
terraform plan
terraform apply
```

5. Confirm the SNS subscription email that gets sent to your inbox
6. Log out and back into AWS to trigger a test alert

To use the pipeline just push any change to the main branch and GitHub Actions will handle the rest automatically.


## Cost

Runs within the AWS Free Tier. The monthly cost at low usage is effectively zero.


## What Was Learned

Building the manual version first made everything easier. By the time Terraform was introduced it was already clear what each resource needed and why.

Writing IAM policies from scratch helped with understanding least privilege in a practical way rather than just reading about it.

The CI/CD pipeline showed how infrastructure deployments work in real teams. Every change goes through the same automated steps which keeps things consistent and reduces mistakes.
