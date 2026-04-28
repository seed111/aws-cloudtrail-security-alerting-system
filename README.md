# AWS CloudTrail Security Alerting System

I built this project to monitor my AWS account and get email alerts whenever someone logs into the console.

I created two versions of the same system. First, I built everything manually in the AWS console so I could understand how the services work together. After that, I rebuilt it using Terraform so it can be deployed quickly from scratch.

## Version 1 Manual Setup

This version is in the manual folder.

I set up CloudTrail, S3, Lambda and SNS directly in the AWS console. This helped me understand what each service does and how they connect.

## Version 2 Terraform

This version is in the terraform folder.

I rebuilt the same system using Terraform because manual setup is not easy to repeat and can lead to mistakes. With Terraform, everything is defined in code and can be deployed or removed easily.

## How It Works

CloudTrail to S3 to Lambda to SNS to Email

CloudTrail records activity in the account and stores logs in S3.
When a new log file is added, it triggers the Lambda function.
The Lambda reads the log file, checks for login events and sends an alert through SNS.

## Services Used

AWS CloudTrail
Amazon S3
AWS Lambda Python 3.12
Amazon SNS
AWS IAM
Terraform

## Security Decisions

The Lambda role only has permission to read from S3 and send messages to SNS
The S3 bucket is private and public access is blocked
CloudTrail log validation is enabled
The SNS topic ARN is not hardcoded and is passed as an environment variable

## Sample Alert

<img width="1179" height="1838" alt="secure alert" src="https://github.com/user-attachments/assets/714ae59c-6fd3-45c8-a00f-81c7c2a3bf4b" />

<img width="1179" height="2293" alt="secure-alert2 png" src="https://github.com/user-attachments/assets/a11239fb-50db-409f-a184-6e2ce229893b" />

The alert comes a few minutes after a login and shows the username, IP address, region, MFA status and time.

## How to Deploy Terraform Version

You need Terraform and AWS CLI installed

Clone the repo and go into the terraform folder
Run aws configure to set your credentials

Create a terraform.tfvars file

alert_email = abrahamsheye1@gmail.com

project_name = "cloudtrail-security"

Run

terraform init
terraform plan
terraform apply

Confirm the email subscription from SNS
Log out and log back in to AWS to trigger a test alert

## Cost

This runs in the AWS free tier for low usage and should cost almost nothing

## What I Learned

Building it manually first helped me understand how everything works. When I moved to Terraform it became easier because I already knew what was needed.

Writing IAM policies myself helped me understand least privilege better.

Moving the SNS ARN out of the code and into an environment variable made the project cleaner and safer.

## What I Would Add Next

Detect root account logins and IAM changes
Add Slack alerts
Store alerts in DynamoDB
Use EventBridge instead of S3 triggers for faster alerts
