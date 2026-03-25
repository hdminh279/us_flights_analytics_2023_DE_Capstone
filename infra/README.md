# 🏗️ Infrastructure as Code (Terraform)

## Overview

This directory contains **Terraform** configuration that provisions all AWS cloud infrastructure needed for the data pipeline. Instead of manually clicking through the AWS Console, we define infrastructure as code, making it:

- **Reproducible**: Same setup every time
- **Versionable**: Track infrastructure changes in Git
- **Scalable**: Easy to add/remove resources
- **Cost-controllable**: See exactly what you're paying for

---

## 🛠️ What Gets Provisioned

### AWS Resources Created

```
┌─────────────────────────────────────────────────────────┐
│         AWS Infrastructure (Terraform)                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  S3 Buckets:                                            │
│  ├── us-flight-delay-analytics-data-lake                │
│  │   ├── raw_flights/        (Raw CSV files)            │
│  │   ├── clean_flights/      (Spark Parquet files)      │
│  │   └── business_flights/   (dbt final tables)         │
│  │                                                      │
│  └── us-flight-delay-analytics-athena-result            │
│      └── (Query results from Athena)                    │
│                                                         │
│  AWS Glue Data Catalog:                                 │
│  └── Database: us_flight_database                       │
│      └── Tables auto-registered from S3                 │
│                                                         │
│  AWS Athena:                                            │
│  └── SQL query engine on S3 data                        │
│      (Must be configured manually via console)          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 File Structure

```
infra/
├── main.tf              # Main infrastructure configuration
├── variables.tf         # Input variables (customizable)
├── terraform.tfstate    # State file (DO NOT edit manually)
├── terraform.tfstate.backup
├── .terraform.lock.hcl  # Lock file (dependency versions)
├── .terraform/          # Downloaded provider plugins
└── README.md            # This file
```

---

## ⚙️ Configuration Files

### `main.tf` - Core Resources

#### 1. **Terraform Block**
Specifies required providers and versions

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>5.0"
    }
  }
}
```

#### 2. **AWS Provider**
Configures AWS authentication

```hcl
provider "aws" {
  region     = var.aws_region          # us-east-1, us-west-2, etc.
  access_key = var.aws_access_key      # From environment/tfvars
  secret_key = var.aws_secret_key      # From environment/tfvars
}
```

#### 3. **S3 Data Lake Bucket**

```hcl
resource "aws_s3_bucket" "data_lake" {
  bucket        = "${var.project_name}-data-lake"
  force_destroy = true  # Allow deletion even if not empty
}

# Output: s3://us-flight-delay-analytics-data-lake
#
# Bucket Structure:
# ├── raw_flights/        ← Kaggle CSV files (Stage 1)
# ├── clean_flights/      ← Spark Parquet files (Stage 2)
# └── business_flights/   ← dbt final tables (Stage 3)
```

**Purpose**: Centralized data lake storing all pipeline data

**Access Pattern**:
- Write: Apache Spark writes cleaned Parquet
- Read: Athena queries via dbt, Metabase queries

#### 4. **S3 Athena Results Bucket**

```hcl
resource "aws_s3_bucket" "athena_results" {
  bucket        = "${var.project_name}-athena-result"
  force_destroy = true
}

# Output: s3://us-flight-delay-analytics-athena-result
#
# Purpose: Store Athena query results & logs
```

**Purpose**: Isolated bucket for Athena query metadata

**Typical contents**:
```
athena-results/
├── logs/
│   ├── 2026-03-25/
│   │   └── query_12345.log
│   └── 2026-03-26/...
└── queries/
    ├── query_12345.parquet
    ├── query_12346.parquet
    └── ...
```

#### 5. **AWS Glue Catalog Database**

```hcl
resource "aws_glue_catalog_database" "data_warehouse" {
  name = "us_flight_database"
}

# Purpose: Metadata catalog for S3 data
#
# AWS Glue automatically crawls S3 and registers:
# - Tables (one per Parquet folder)
# - Columns and data types
# - Partitioning information
#
# Tables created:
# ├── flights_raw (from raw_flights/)
# ├── flights_clean (from clean_flights/flights/)
# ├── airports (from clean_flights/airports/)
# ├── stg_flights (from business_flights/stg_flights/)
# ├── fct_flights (from business_flights/fct_flights/)
# └── ... (other dbt models)
```

**Purpose**: Makes S3 data queryable via Athena SQL

---

### `variables.tf` - Configuration Parameters

```hcl
variable "aws_region" {
  description = "AWS Region for all resources"
  type        = string
  default     = "us-east-1"
  # Options: us-east-1, us-west-2, ap-southeast-1, eu-west-1, etc.
}

variable "aws_access_key" {
  description = "AWS Access Key ID"
  type        = string
  sensitive   = true  # Don't print in logs
}

variable "aws_secret_key" {
  description = "AWS Secret Access Key"
  type        = string
  sensitive   = true
}

variable "project_name" {
  description = "Project name (used in resource names)"
  type        = string
  default     = "us-flight-delay-analytics"
  # All resources use this as prefix
}

variable "aws_bucket" {
  description = "S3 bucket path for data"
  type        = string
  default     = "us-flight-delay-analytics-data-lake/clean/"
}
```

**How to override defaults**:

Option 1: Environment variables
```bash
export TF_VAR_aws_region="us-west-2"
export TF_VAR_project_name="my-project"
```

Option 2: terraform.tfvars file
```hcl
aws_region  = "us-west-2"
project_name = "my-project-name"
```

Option 3: Command-line arguments
```bash
terraform apply \
  -var="aws_region=us-west-2" \
  -var="project_name=my-project"
```

---

## 🚀 Quick Start

### Prerequisites

1. **AWS Account** with programmatic access
2. **Terraform CLI** installed (`terraform --version` should work)
3. **AWS CLI configured** (optional but recommended)

### Step 1: Get AWS Credentials

```bash
# From AWS Console:
# 1. IAM → Users → Your User
# 2. Security Credentials → Create Access Key
# 3. Copy: Access Key ID and Secret Access Key

export AWS_ACCESS_KEY_ID="your_access_key_id"
export AWS_SECRET_ACCESS_KEY="your_secret_access_key"
```

### Step 2: Initialize Terraform

```bash
cd infra/

# Download AWS provider plugin
terraform init

# Output:
# Initializing the backend...
# Initializing provider plugins...
# Terraform has been successfully initialized!
```

### Step 3: Plan Infrastructure

```bash
terraform plan

# Shows what resources will be created:
# An execution plan has been generated and is shown below.
# 
# + aws_s3_bucket.data_lake
#   bucket = "us-flight-delay-analytics-data-lake"
# 
# + aws_s3_bucket.athena_results
#   bucket = "us-flight-delay-analytics-athena-result"
# 
# + aws_glue_catalog_database.data_warehouse
#   name = "us_flight_database"
# 
# Plan: 3 to add, 0 to change, 0 to destroy
```

### Step 4: Apply Infrastructure

```bash
# Create resources in AWS
terraform apply

# Review and type 'yes' to confirm
# ...
# Apply complete! Resources: 3 added, 0 changed, 0 destroyed.
```

### Step 5: Verify in AWS Console

```bash
# List created buckets
aws s3 ls

# List Glue databases
aws glue get-databases --region us-east-1
```

---

## 🔗 Related Documentation

- [Main README](../README.md) - Project overview
- [Airflow DAGs](../airflow/README.md) - Pipeline using these resources
- [Spark Jobs](../spark_jobs/README.md) - Data written to S3
- [dbt Models](../airflow/dags/dbt_transform/us_flight_analytics/README.md) - Queries on Athena

---

## 📖 Additional Resources

- [Terraform Documentation](https://www.terraform.io/docs/)
- [AWS S3 Resource Reference](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket)
- [AWS Glue Resource Reference](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_catalog_database)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/recommended-practices/index.html)
- [AWS Free Tier](https://aws.amazon.com/free/)