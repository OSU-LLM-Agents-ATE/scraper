import concurrent.futures
import threading
import time
from queue import Queue
from typing import Optional

from app.clients import s3_client
from config.config import JOB_ID, S3_BUCKET_NAME

BATCH_SIZE = 20
BATCH_TIMEOUT = 5

# Create a thread-safe queue for storing items to upload
upload_queue = Queue()
upload_lock = threading.Lock()


def save_page_to_s3_batch(file_name: str, html_content: str) -> None:
    """Add an item to the batch queue for uploading to S3."""
    # Construct the S3 object key
    key = f"{JOB_ID}/{file_name}"

    # Add the item to the queue
    upload_queue.put((key, html_content))
    print(f"Queued page for S3 upload with key: {key}")

    # Check if it's time to flush the batch
    if upload_queue.qsize() >= BATCH_SIZE:
        with upload_lock:
            flush_s3_batch()


def flush_s3_batch(forced: Optional[bool] = False) -> None:
    """Upload all items in the batch queue to S3 concurrently."""
    items_to_upload = []

    # Gather items from the queue up to the batch size
    while not upload_queue.empty() and (len(items_to_upload) < BATCH_SIZE or forced):
        items_to_upload.append(upload_queue.get())

    # Perform concurrent uploads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Schedule the upload tasks concurrently
        futures = [
            executor.submit(upload_to_s3, key, html_content)
            for key, html_content in items_to_upload
        ]
        # Wait for all uploads to complete
        concurrent.futures.wait(futures)

    print(f"Uploaded batch of {len(items_to_upload)} items to S3")


# Helper function for uploading a single item to S3
def upload_to_s3(key: str, html_content: str) -> None:
    """Upload a single file to S3."""
    s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=key, Body=html_content)
    print(f"Saved page to S3 with key: {key}")


# Background func to flush the batch periodically
def background_batch_uploader():
    while True:
        time.sleep(BATCH_TIMEOUT)
        with upload_lock:
            if not upload_queue.empty():
                flush_s3_batch(forced=True)


# Start the background thread to periodically flush the queue
background_thread = threading.Thread(target=background_batch_uploader, daemon=True)
background_thread.start()
