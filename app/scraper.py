from typing import Set
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from app.clients import s3_client
from config.config import JOB_ID, S3_BUCKET_NAME


def download_page(url: str) -> str:
    """Download the HTML content of a page."""
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.text


def extract_urls(html: str, base_url: str) -> Set[str]:
    """Extract and normalize links from HTML content, keeping only URLs within the specified subdomain."""
    soup = BeautifulSoup(html, "html.parser")
    urls = set()
    base_netloc = urlparse(
        base_url
    ).netloc  # Extract the base domain (e.g., engineering.oregonstate.edu)

    for element in soup.find_all("a", href=True):
        href = element["href"]

        # Skip empty hrefs and fragment-only links (e.g., #top)
        if not href or href.startswith("#"):
            continue

        # Resolve relative URLs to absolute URLs
        full_url = urljoin(base_url, href)

        # Parse the URL to get its domain and path
        parsed_url = urlparse(full_url)
        netloc = parsed_url.netloc

        # Only add URLs that match the base domain and exclude the base URL without a path
        if netloc == base_netloc and (parsed_url.path or parsed_url.fragment):
            urls.add(full_url)

    return urls


def save_page_to_s3(file_name: str, html_content: str) -> None:
    """Save HTML content to S3 with a unique filename."""
    key = f"{JOB_ID}/{file_name}"
    s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=key, Body=html_content)
    print(f"Saved page to S3 with key: {key}")
