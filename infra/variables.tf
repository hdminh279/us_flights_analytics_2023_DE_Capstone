variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "ap-southeast-1"
}

variable "aws_access_key" {
  description = "AWS Access Key"
  type        = string
}

variable "aws_secret_key" {
  description = "AWS Secret Key"
  type        = string
}

variable "project_name" {
  description = "AWS Project Name"
  type        = string
  default     = "us-flight-delay-analytics"
}

variable "aws_bucket" {
  description = "AWS Bucket"
  type        = string
  default     = "us-flight-delay-analytics-data-lake/clean/"
}