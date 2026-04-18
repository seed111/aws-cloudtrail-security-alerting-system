 AWS CloudTrail Security Alerting System

I put this project together to build a proactive security monitoring tool on AWS. The core idea was to create a system that actually reacts to what is happening in an account instead of just letting logs sit in storage. It uses AWS CloudTrail to track every single action and saves that data directly into Amazon S3. The heavy lifting is handled by a Lambda function that triggers automatically whenever a new log arrives. I programmed it to scan for console logins in near real time so that nothing slips under the radar. If someone logs into the account the system immediately sends out an alert through Amazon SNS to notify the user. This project gave me a lot of practical experience with serverless design and showed me how to actually secure a cloud environment in a way that is both fast and efficient.



 
 Architecture

This project uses an event driven setup:

CloudTrail → S3 → Lambda → SNS → Email

CloudTrail records account activity and API calls.
These logs are stored in an S3 bucket.
Whenever a new log file is added, S3 triggers a Lambda function.
The Lambda function reads the logs and checks for console login events.
If a login is detected, an alert is sent through SNS to your email.



Implementation Steps

I first created an S3 bucket to store the CloudTrail logs. Then I enabled CloudTrail and set it to send logs to that bucket.

After that, I created a Lambda function using Python. I connected the S3 bucket to the Lambda function using a trigger, so the function runs whenever a new log file is added.
Inside the Lambda function, I wrote code to read and unzip the log files, then extract the data from them.
I added logic to check for console login events, since they are important for security monitoring.
Finally, I created an SNS topic and subscribed my email to it. I updated the Lambda function to send an alert through SNS whenever a login event is detected.

