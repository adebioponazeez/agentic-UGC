import unittest
from unittest.mock import patch

from tetrative_os.research import ResearchSafetyError, validate_public_url


class ResearchNetworkPolicyTests(unittest.TestCase):
    def test_non_https_and_embedded_credentials_are_blocked(self):
        for url in ("http://example.com", "file:///etc/passwd", "https://user:pass@example.com"):
            with self.subTest(url=url), self.assertRaises(ResearchSafetyError):
                validate_public_url(url)

    @patch("tetrative_os.research.socket.getaddrinfo")
    def test_private_and_loopback_dns_results_are_blocked(self, lookup):
        lookup.return_value = [(2, 1, 6, "", ("127.0.0.1", 443))]
        with self.assertRaises(ResearchSafetyError):
            validate_public_url("https://example.test")
        lookup.return_value = [(2, 1, 6, "", ("10.0.0.4", 443))]
        with self.assertRaises(ResearchSafetyError):
            validate_public_url("https://example.test")

    @patch("tetrative_os.research.socket.getaddrinfo")
    def test_public_dns_result_is_allowed(self, lookup):
        lookup.return_value = [(2, 1, 6, "", ("93.184.216.34", 443))]
        validate_public_url("https://example.com/research")


if __name__ == "__main__":
    unittest.main()
