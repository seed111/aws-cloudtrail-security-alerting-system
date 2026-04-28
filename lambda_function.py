import json
import gzip
import os
import boto3

s3 = boto3.client('s3')
sns = boto3.client('sns')

SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']
def get_user(identity):
    if identity.get('type') == 'Root':
        return 'ROOT ACCOUNT'
    return (
        identity.get('userName') or
        identity.get('sessionContext', {})
                .get('sessionIssuer', {})
                .get('userName') or
        identity.get('arn') or
        'Unknown'
    )

def lambda_handler(event, context):
    print("Lambda triggered")

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print(f"Processing file: {key}")

        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            content = gzip.decompress(response['Body'].read())
            log_data = json.loads(content)
        except Exception as e:
            print(f"Failed to read log file: {e}")
            continue

        for log in log_data.get('Records', []):
            if log.get('eventName') == 'ConsoleLogin':
                identity = log.get('userIdentity', {})
                mfa = log.get('additionalEventData', {}).get('MFAUsed', 'No')
                mfa_warning = ' - MFA NOT USED' if mfa != 'Yes' else ''

                message = (
                    "ALERT: Console Login Detected!\n\n"
                    f"User:       {get_user(identity)}\n"
                    f"IP Address: {log.get('sourceIPAddress', 'N/A')}\n"
                    f"Region:     {log.get('awsRegion', 'N/A')}\n"
                    f"MFA Used:   {mfa}{mfa_warning}\n"
                    f"Time:       {log.get('eventTime', 'N/A')}\n"
                )

                print(message)
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=message,
                    Subject="AWS Security Alert"
                )

    return {'statusCode': 200}