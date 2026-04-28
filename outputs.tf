output "s3_bucket_name" {
  value = aws_s3_bucket.cloudtrail_logs.id
}

output "sns_topic_arn" {
  value = aws_sns_topic.security_alerts.arn
}

output "lambda_function_name" {
  value = aws_lambda_function.security_monitor.function_name
}



