import uuid
from datetime import datetime

AWS_URL = "http://localhost:4566"
DYNAMODB_TABLE_NAME = "URLQueue"
S3_BUCKET_NAME = "scraped-pages"
WORKER_COUNT = 16
JOB_ID = f'{datetime.now().strftime("%Y-%m-%d")}/run-{uuid.uuid4()}'
