from unittest.mock import patch

from django.test import TestCase
from .utils.metadata_scraper import scrape_metadata


class MetadataScraperTest(TestCase):
    @patch("requests.get")
    def test_returns_metadata(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.url = "https://example.com"
        mock_get.return_value.text = """
        <html>
            <head>
                <meta property="og:type" content="test type">
                <meta property="og:title" content="test title">
                <meta property="og:description" content="test description">
                <meta property="og:site_name" content="test site name">
                <meta property="og:image" content="test image">
            </head>
        """

        data = scrape_metadata("https://example.com")

        if data is None:
            self.fail("data is None")
        self.assertEqual(data["title"], "test title")
        self.assertEqual(data["site_name"], "test site name")
        self.assertEqual(data["description"], "test description")
        self.assertEqual(data["image"], "test image")
