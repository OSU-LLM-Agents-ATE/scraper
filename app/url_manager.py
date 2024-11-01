import time
from typing import Set
from botocore.exceptions import ClientError
from app.clients import dynamodb_resource
from app.constants import Status
from config.config import DYNAMODB_ITEM_TTL_SEC, DYNAMODB_TABLE_NAME, WORKER_COUNT


def add_urls(urls: Set[str], logger) -> None:
    """Add URLs to the DynamoDB table with 'available' status if they don't already exist."""
    table = dynamodb_resource.Table(DYNAMODB_TABLE_NAME)

    for url in urls:
        try:
            # Attempt to add the URL if it doesn't already exist with TTL
            expiration_timestamp = int(time.time()) + DYNAMODB_ITEM_TTL_SEC
            table.put_item(
                Item={
                    "ADDRESS": url,
                    "StatusCode": Status.AVAILABLE.value,
                    "ExpirationTime": expiration_timestamp,
                },
                ConditionExpression="attribute_not_exists(ADDRESS)",  # Only add if URL does not exist
            )
            logger.info("URL added", url=url)
        except ClientError as e:
            # If the item already exists, a ConditionalCheckFailedException will be raised
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                logger.debug("Duplicate URL skipped", url=url)
            else:
                # Handle unexpected errors
                logger.error("Error adding URL", url=url, error=str(e))


def get_next_url(logger):
    """Retrieve an available URL from DynamoDB and mark it as 'in-progress' using a conditional update."""
    table = dynamodb_resource.Table(DYNAMODB_TABLE_NAME)

    # Query for available URLs using the GSI
    response = table.query(
        IndexName="StatusCodeIndex",
        KeyConditionExpression="StatusCode = :status",
        ExpressionAttributeValues={":status": Status.AVAILABLE.value},
        Limit=WORKER_COUNT,
    )

    items = response.get("Items", [])

    # If no available URLs, return None
    if not items:
        return None

    # Attempt to claim the first available URL with a conditional update
    for item in items:
        url = item["ADDRESS"]
        try:
            # Update the URL to 'in-progress' conditionally if it's still 'available'
            table.update_item(
                Key={"ADDRESS": url},
                UpdateExpression="SET StatusCode = :in_progress",
                ConditionExpression="StatusCode = :available",
                ExpressionAttributeValues={
                    ":in_progress": Status.IN_PROGRESS.value,
                    ":available": Status.AVAILABLE.value,
                },
            )
            # Successfully claimed the URL, return it
            logger.info("URL claimed", url=url)
            return url

        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                # Another worker claimed this URL; continue to the next item
                logger.debug("URL already claimed by another worker", url=url)
                continue
            else:
                # Other unexpected errors
                logger.error("Unexpected error", error=str(e))
                return None

    # If all items were claimed by other workers, return None
    return None


def update_url_status(url: str, status: Status, logger):
    """Update the status of a URL in the DynamoDB table."""
    table = dynamodb_resource.Table(DYNAMODB_TABLE_NAME)
    table.update_item(
        Key={"ADDRESS": url},
        UpdateExpression="SET StatusCode = :status",
        ExpressionAttributeValues={":status": status},
    )
    logger.info("URL status updated", url=url, status=status)
