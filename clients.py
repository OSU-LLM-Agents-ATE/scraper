import boto3
from mypy_boto3_dynamodb.client import DynamoDBClient
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
from mypy_boto3_s3.client import S3Client
from mypy_boto3_s3.service_resource import S3ServiceResource

from config import AWS_URL

test_kwargs = {
    "region_name": "us-east-1",
    "aws_access_key_id": "test",
    "aws_secret_access_key": "test",
}

# Type-annotated DynamoDB resource and client
dynamodb_resource: DynamoDBServiceResource = boto3.resource(
    "dynamodb", endpoint_url=AWS_URL, **test_kwargs
)
dynamodb_client: DynamoDBClient = boto3.client(
    "dynamodb", endpoint_url=AWS_URL, **test_kwargs
)

# Type-annotated S3 resource and client
s3_resource: S3ServiceResource = boto3.resource(
    "s3", endpoint_url=AWS_URL, **test_kwargs
)
s3_client: S3Client = boto3.client("s3", endpoint_url=AWS_URL, **test_kwargs)
