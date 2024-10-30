import os
import uuid
from datetime import datetime

AWS_URL = os.getenv("AWS_URL", "")
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "ScraperTable")
DYNAMODB_ITEM_TTL_SEC = int(os.getenv("DYNAMODB_ITEM_TTL_SEC", 86400))
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "osu-llm-ate-scraped-pages")
WORKER_COUNT = int(os.getenv("WORKER_COUNT", 16))
JOB_ID = f'{datetime.now().strftime("%Y-%m-%d")}/run-{uuid.uuid4()}'
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
