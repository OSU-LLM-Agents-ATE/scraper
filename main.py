import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from collections import deque


def crawl_website(start_url):
    visited = set()
    queue = deque([start_url])

    domain = urlparse(start_url).netloc

    rp = RobotFileParser()
    robots_url = urljoin(start_url, '/robots.txt')
    rp.set_url(robots_url)
    rp.read()

    while queue:
        url = queue.popleft()
        if url in visited:
            continue
        if not rp.can_fetch('*', url):
            continue
        try:
            response = requests.get(url)
            if response.status_code != 200:
                continue
            visited.add(url)
            print(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                full_url = urljoin(url, href)
                if urlparse(full_url).netloc == domain:
                    if full_url not in visited:
                        queue.append(full_url)
        except requests.exceptions.RequestException as e:
            print(e)


def read_subdomains_to_list(file_path):
    with open(file_path, 'r') as file:
        domain_list = [line.strip() for line in file]
    return domain_list


def main():
    domain = "oregonstate.edu"
    subdomains = read_subdomains_to_list("subdomains.txt")

    # crawl base domain
    crawl_website(f"https://{domain}")

    # crawl subdomains
    for subdomain in subdomains:
        crawl_website(f"https://{subdomain}.{domain}")


if __name__ == '__main__':
    main()
