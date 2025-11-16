#!/usr/bin/env python3

"""
Unit tests for the `GithubOrgClient.org` method.

This test suite verifies that the client correctly delegates to `get_json`
and returns the expected organization data without making real HTTP calls.
"""

import unittest
from unittest.mock import patch

from parameterized import parameterized
from utils.client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for the `GithubOrgClient` class."""

    @parameterized.expand(
        [
            ("google",),
            ("abc",),
        ]
    )
    @patch("utils.client.get_json")
    def test_org(self, org_name: str, mock_get_json) -> None:
        expected = {"org": org_name}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected)      
        self.assertEqual(result, expected)