import concurrent.futures
import hashlib
import threading
import time
from queue import Queue
from typing import Optional

from app.clients import s3_client
from config.config import JOB_ID, RUN_DATE, S3_BUCKET_NAME

BATCH_SIZE = 20
BATCH_TIMEOUT = 5

# Create a thread-safe queue for storing items to upload
upload_queue = Queue()
upload_lock = threading.Lock()


def sha256_from_string(text) -> str:
    encoded_text = text.encode("utf-8")
    hash_object = hashlib.sha256(encoded_text)
    hex_digest = hash_object.hexdigest()
    return hex_digest


# todo: there is a bug here, if there are concurrent scrapers running, they will not have context to another scraper's already stored hashes
# fix: place this functionality in dynamodb
already_stored_hashes: dict[str, list[str]] = {}


def save_page_to_s3_batch(file_name: str, html_content: str, url: str) -> None:
    """Add an item to the batch queue for uploading to S3."""
    # check if the content is already stored
    content_hash = sha256_from_string(html_content)
    if content_hash in already_stored_hashes:
        print(
            f"Content of {url} has already seen under these url(s): {already_stored_hashes[content_hash]}"
        )
        already_stored_hashes[content_hash].append(url)
        return
    else:
        already_stored_hashes[content_hash] = [url]

    # Construct the S3 object key
    key = f"{JOB_ID}/{file_name}"

    # Add the item to the queue
    upload_queue.put((key, html_content, url))
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
            executor.submit(upload_to_s3, key, html_content, url)
            for key, html_content, url in items_to_upload
        ]
        # Wait for all uploads to complete
        concurrent.futures.wait(futures)

    print(f"Uploaded batch of {len(items_to_upload)} items to S3")


# Helper function for uploading a single item to S3
def upload_to_s3(key: str, html_content: str, url: str) -> None:
    """Upload a single file to S3."""
    s3_client.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=key,
        Body=html_content,
        Metadata={"source-url": url, "scraped-date": RUN_DATE},
    )
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
