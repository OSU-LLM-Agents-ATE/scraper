import structlog

from app.clients import dynamodb_resource, s3_client, s3_resource
from app.url_manager import add_urls
from app.worker_pool import run_worker_pool
from config.config import AWS_URL, DYNAMODB_TABLE_NAME, S3_BUCKET_NAME, WORKER_COUNT
from scraper.logging import configure_logging

# Configure logging
configure_logging()

# Initialize logger
logger = structlog.get_logger()


def setup_resources():
    """Create DynamoDB table and S3 bucket if they do not exist."""
    # Create DynamoDB Table
    try:
        table = dynamodb_resource.create_table(
            TableName=DYNAMODB_TABLE_NAME,
            KeySchema=[{"AttributeName": "ADDRESS", "KeyType": "HASH"}],
            AttributeDefinitions=[
                {"AttributeName": "ADDRESS", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        table.wait_until_exists()
        logger.info("DynamoDB table created.", table_name=DYNAMODB_TABLE_NAME)
    except dynamodb_resource.meta.client.exceptions.ResourceInUseException:
        logger.warning("DynamoDB table already exists.", table_name=DYNAMODB_TABLE_NAME)
    except Exception as e:
        logger.exception("Failed to create DynamoDB table.", error=str(e))

    logger.info("DynamoDB table is ready.")

    # Create S3 Bucket
    try:
        s3_resource.create_bucket(Bucket=S3_BUCKET_NAME)
        logger.info("S3 bucket created.", bucket_name=S3_BUCKET_NAME)
    except s3_client.exceptions.BucketAlreadyExists:
        logger.warning("S3 bucket already exists.", bucket_name=S3_BUCKET_NAME)
    except Exception as e:
        logger.exception("Failed to create S3 bucket.", error=str(e))

    logger.info("S3 bucket is ready.")
    logger.info("All resources are ready.")


if __name__ == "__main__":
    if AWS_URL != "":
        setup_resources()  # Setup DynamoDB table and S3 bucket in LocalStack

    base_url = "https://engineering.oregonstate.edu"
    # we can use subdomains.txt to get more initial URLs if we decide to expand our scraping surface area

    # Add initial URLs to the queue
    add_urls(urls={base_url})
    logger.info("Initial URLs added to queue.", base_url=base_url)

    # Start the worker pool
    run_worker_pool(base_url=base_url, num_workers=WORKER_COUNT)
    logger.info("Worker pool started.", base_url=base_url, num_workers=WORKER_COUNT)
