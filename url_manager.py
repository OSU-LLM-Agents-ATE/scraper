from typing import Set

from botocore.exceptions import ClientError

from clients import dynamodb_resource
from config import DYNAMODB_TABLE_NAME
from constants import Status


def add_urls(urls: Set[str]) -> None:
    """Add URLs to the DynamoDB table with 'available' status if they don't already exist."""
    table = dynamodb_resource.Table(DYNAMODB_TABLE_NAME)

    for url in urls:
        try:
            # Attempt to add the URL if it doesn't already exist
            table.put_item(
                Item={"ADDRESS": url, "StatusCode": Status.AVAILABLE.value},
                ConditionExpression="attribute_not_exists(ADDRESS)",  # Only add if URL does not exist
            )
            print(f"URL added: {url}")
        except ClientError as e:
            # If the item already exists, a ConditionalCheckFailedException will be raised
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                pass  # TODO: use structlogging and log this as Debug
                # print(f"Duplicate URL skipped: {url}")
            else:
                # Handle unexpected errors
                print(f"Error adding URL {url}: {e}")


def get_next_url():
    """Retrieve an available URL from DynamoDB and mark it as 'in-progress' using a conditional update."""
    table = dynamodb_resource.Table(DYNAMODB_TABLE_NAME)

    # Scan for available URLs
    response = table.scan(
        FilterExpression="StatusCode = :status",
        ExpressionAttributeValues={":status": Status.AVAILABLE.value},
    )  # this will be inefficient with a large number of URLs, maybe it doesn't matter? here? Max results is enough to
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
            return url

        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                # Another worker claimed this URL; continue to the next item
                continue
            else:
                # Other unexpected errors
                print(f"Unexpected error: {e}")
                return None

    # If all items were claimed by other workers, return None
    return None


def update_url_status(url: str, status: Status):
    """Update the status of a URL in the DynamoDB table."""
    table = dynamodb_resource.Table(DYNAMODB_TABLE_NAME)
    table.update_item(
        Key={"ADDRESS": url},
        UpdateExpression="SET StatusCode = :status",
        ExpressionAttributeValues={":status": status},
    )
