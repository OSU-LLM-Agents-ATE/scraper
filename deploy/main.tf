terraform {
  backend "s3" {
    bucket         = "scraper-tf-state"
    key            = "global/s3/terraform.tfstate"            # Path to store the state file in the bucket
    region         = "us-east-1"                              # S3 bucket region
    encrypt        = true                                     # Enable server-side encryption
    dynamodb_table = "terraform-state-locks"                  # DynamoDB table for state locking
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "scraper_bucket" {
  bucket = "osu-llm-ate-scraped-pages"
}

resource "aws_dynamodb_table" "scraper_table" {
  name           = "ScraperTable"
  billing_mode   = "PAY_PER_REQUEST"

  hash_key       = "ADDRESS"

  attribute {
    name = "ADDRESS"
    type = "S"
  }

  attribute {
    name = "StatusCode"
    type = "S"
  }

  # Configure a Global Secondary Index for querying by StatusCode
  global_secondary_index {
    name               = "StatusCodeIndex"
    hash_key           = "StatusCode"
    projection_type    = "ALL"           # Use ALL projection to include all attributes in the index
  }

  # Configure TTL settings
  ttl {
    attribute_name = "ExpirationTime"
    enabled        = true
  }

  tags = {
    Environment = "production"
    Name        = "Scraper DynamoDB Table"
  }
}
