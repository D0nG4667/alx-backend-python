#!/usr/bin/env python3

"""
Unit tests for the `GithubOrgClient.org` method.

This test suite verifies that the client correctly
elegates to `get_json`
and returns the expected organization data without
making real HTTP calls.
"""

import unittest
from typing import Dict, List
from unittest.mock import PropertyMock, patch

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

    def test_public_repos_url(self) -> None:
        """
        Test that `_public_repos_url` returns the expected repository URL.

        This test mocks the `org` property to return a known payload,
        and verifies that `_public_repos_url` correctly
        extracts the `repos_url` field.
        """
        mock_payload: Dict[str, str] = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }

        # Patch the `org` property to return the mock payload
        with patch(
            "utils.client.GithubOrgClient.org",
            new_callable=PropertyMock,
            return_value=mock_payload,
        ):
            client = GithubOrgClient("testorg")
            result: str = client._public_repos_url

            # Assert that the extracted URL matches the mocked value
            self.assertEqual(result, mock_payload["repos_url"])
            self.assertEqual(result, mock_payload["repos_url"])

    @patch("utils.client.get_json")
    def test_public_repos(self, mock_get_json) -> None:
        """
        Test that `public_repos` returns the expected list of repository names.

        This test mocks:
        - `get_json` to return a known list of repo dictionaries
        - `_public_repos_url` to return a fake API URL

        It verifies:
        - The returned list of repo names matches the mocked payload
        - Both mocks are called exactly once
        """
        mock_repos_payload: List[Dict[str, str]] = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = mock_repos_payload

        with patch(
            "utils.client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/testorg/repos",
        ) as mock_repos_url:
            client = GithubOrgClient("testorg")
            result = client.public_repos()

            # Validate returned repo names
            self.assertEqual(result, ["repo1", "repo2", "repo3"])

            # Ensure both mocks were called exactly once
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/testorg/repos"
            )
            mock_repos_url.assert_called_once()
            mock_repos_url.assert_called_once()
