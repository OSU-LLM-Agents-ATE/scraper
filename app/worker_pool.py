import random
import re
import threading
import time

from app.constants import Status
from app.scraper import download_page, extract_urls, save_page_to_s3
from app.url_manager import add_urls, get_next_url, update_url_status

MAX_RETRIES = 3


def url_to_filename(url):
    # Remove the scheme (http, https) and "www." prefix if present
    clean_url = re.sub(r"^(https?:\/\/)?(www\.)?", "", url)
    # Replace non-alphanumeric characters with underscores
    filename = re.sub(r"[^a-zA-Z0-9]", "_", clean_url)
    # Remove any trailing underscores from the filename
    filename = filename.rstrip("_")
    return filename


def worker(base_url) -> None:
    """Worker function that processes one URL at a time."""
    retry_count = 0
    while True:
        url = get_next_url()
        if not url:
            if retry_count < MAX_RETRIES:
                delay = min(30, (2**retry_count) + random.uniform(0, 1))
                print(f"No available URLs. Retrying in {delay:.2f} seconds...")
                retry_count += 1
                time.sleep(delay)
                continue
            print("No available URLs after maximum retries. Worker exiting.")
            break
        retry_count = 0  # Reset retry count if a URL is found
        try:
            html = download_page(url)
            urls = extract_urls(html, base_url)

            # Add new links to the queue
            add_urls(urls=urls)

            # Save page content to S3
            save_page_to_s3(file_name=url_to_filename(url), html_content=html)

            # Mark URL as done
            update_url_status(url, Status.DONE.value)
        except Exception as e:
            print(f"Error processing {url}: {e}")
            update_url_status(url, Status.FAILED.value)
        time.sleep(1)


def run_worker_pool(base_url: str, num_workers: int = 3) -> None:
    """Run a pool of worker threads to process URLs concurrently."""
    threads = []
    for _ in range(num_workers):
        thread = threading.Thread(target=worker, args=(base_url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
