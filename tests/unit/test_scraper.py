import unittest
from typing import Set

from app.scraper import extract_urls


class TestExtractUrls(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://engineering.oregonstate.edu"

    def test_relative_urls(self):
        html = """
        <html>
            <body>
                <a href="/about">About</a>
                <a href="/contact">Contact</a>
            </body>
        </html>
        """
        expected_urls = {
            "https://engineering.oregonstate.edu/about",
            "https://engineering.oregonstate.edu/contact",
        }
        result = extract_urls(html, self.base_url)
        self.assertEqual(result, expected_urls)

    def test_absolute_urls_within_subdomain(self):
        html = """
        <html>
            <body>
                <a href="https://engineering.oregonstate.edu/research">Research</a>
                <a href="https://engineering.oregonstate.edu/faculty">Faculty</a>
            </body>
        </html>
        """
        expected_urls = {
            "https://engineering.oregonstate.edu/research",
            "https://engineering.oregonstate.edu/faculty",
        }
        result = extract_urls(html, self.base_url)
        self.assertEqual(result, expected_urls)

    def test_absolute_urls_outside_subdomain(self):
        html = """
        <html>
            <body>
                <a href="https://example.com/page">External Page</a>
                <a href="https://anotherdomain.com/page">Another Domain</a>
            </body>
        </html>
        """
        # Should be empty because no URLs match the base subdomain
        expected_urls: Set[str] = set()
        result = extract_urls(html, self.base_url)
        self.assertEqual(result, expected_urls)

    def test_mixed_urls(self):
        html = """
        <html>
            <body>
                <a href="/internal">Internal Link</a>
                <a href="https://engineering.oregonstate.edu/resources">Resources</a>
                <a href="https://external.com/page">External Link</a>
                <a href="https://engineering.oregonstate.edu/contact">Contact</a>
            </body>
        </html>
        """
        expected_urls = {
            "https://engineering.oregonstate.edu/internal",
            "https://engineering.oregonstate.edu/resources",
            "https://engineering.oregonstate.edu/contact",
        }
        result = extract_urls(html, self.base_url)
        self.assertEqual(result, expected_urls)

    def test_edge_cases(self):
        html = """
        <html>
            <body>
                <a href="">Empty Link</a>
                <a href="#fragment">Fragment Only</a>
                <a href="https://engineering.oregonstate.edu/#top">
                    Internal Fragment
                </a>
                <a href="/valid">Valid Relative Link</a>
            </body>
        </html>
        """
        expected_urls = {
            "https://engineering.oregonstate.edu/valid",
            "https://engineering.oregonstate.edu/#top",
        }
        result = extract_urls(html, self.base_url)
        self.assertEqual(result, expected_urls)
