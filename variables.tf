variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "alert_email" {
  description = "Email address to receive security alerts"
  type        = string
}

variable "project_name" {
  description = "Used to name all resources consistently"
  type        = string
  default     = "cloudtrail-security"
}