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
  billing_mode   = "PAY_PER_REQUEST"  # Use on-demand billing

  hash_key       = "URL"

  attribute {
    name = "URL"
    type = "S"  # string
  }

  # speeds up filtered scan on status code
  global_secondary_index {
    name               = "StatusCodeIndex"
    hash_key           = "StatusCode"
    projection_type    = "ALL"
  }

  attribute {
    name = "StatusCode"
    type = "S"  # string
  }

  # we should consider TTL to manage updating old files.
  # We might be able to overwrite in the same folder in S3

  tags = {
    Environment = "production"
    Name        = "Scraper DynamoDB Table"
  }
}
