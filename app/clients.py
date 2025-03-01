import boto3
from mypy_boto3_dynamodb.client import DynamoDBClient
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
from mypy_boto3_s3.client import S3Client
from mypy_boto3_s3.service_resource import S3ServiceResource

from config.config import (AWS_ACCESS_KEY_ID, AWS_REGION,
                           AWS_SECRET_ACCESS_KEY, AWS_URL)

aws_resource_kwargs = {
    "region_name": AWS_REGION,
    "aws_access_key_id": AWS_ACCESS_KEY_ID,
    "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
}

if AWS_URL:
    aws_resource_kwargs["endpoint_url"] = AWS_URL

dynamodb_resource: DynamoDBServiceResource = boto3.resource(
    "dynamodb", **aws_resource_kwargs
)
dynamodb_client: DynamoDBClient = boto3.client("dynamodb", **aws_resource_kwargs)

s3_resource: S3ServiceResource = boto3.resource("s3", **aws_resource_kwargs)
s3_client: S3Client = boto3.client("s3", **aws_resource_kwargs)
