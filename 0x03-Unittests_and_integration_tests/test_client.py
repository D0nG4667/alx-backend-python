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
from unittest.mock import MagicMock, PropertyMock, patch

from parameterized import parameterized
from utils.client import GithubOrgClient
from utils.fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for the `GithubOrgClient` class."""

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo: Dict[str, Dict[str, str]], 
        license_key: str, expected: bool
    ):
        """
        Test that `has_license` correctly checks if a repo has the
        specified license.

        Args:
            repo (dict): A dictionary representing a GitHub repository.
            license_key (str): The license key to check for.
            expected (bool): Expected result of the license check.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

    @parameterized.expand(
        [
            ("google",),
            ("abc",),
        ]
    )
    @patch("utils.client.get_json")
    def test_org(self, org_name: str, mock_get_json) -> None:
        """
        Unit test for the `GithubOrgClient.org` property.

        Verifies that the client correctly delegates to `get_json` and
        return the expected organization payload. Ensures that
        the external API call is made exactly once with the correct URL.

        Args:
            org_name (str): The name of the GitHub organization to test.
            mock_get_json (MagicMock): Mocked version of `get_json`.

        Asserts:
            - `get_json` is called once with the correct URL.
            - The returned value matches the expected mock payload.
        """
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
        Test that `public_repos` returns the expected list of
        repository names.

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


"""
Integration tests for GithubOrgClient.public_repos using fixtures
and patched requests.get.
"""


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test suite for GithubOrgClient.public_repos.

    This class uses fixture-based mocking to simulate GitHub API responses.
    Only external HTTP calls are mocked; internal logic is tested end-to-end.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Start patching requests.get and configure side_effect
        to return fixture payloads."""
        (
            cls.org_payload,
            cls.repos_payload,
            cls.expected_repos,
            cls.apache2_repos,
        ) = TEST_PAYLOAD[0]

        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            response = MagicMock()
            if url.endswith("/repos"):
                response.json.return_value = cls.repos_payload
            else:
                response.json.return_value = cls.org_payload
            return response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test that public_repos returns expected repo names
        from fixture payload."""
        client = GithubOrgClient("testorg")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Test that public_repos filters repos by 'apache-2.0'
        license using fixture payload.
        """
        client = GithubOrgClient("testorg")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
        self.assertEqual(result, self.apache2_repos)
        self.assertEqual(result, self.apache2_repos)
        self.assertEqual(result, self.apache2_repos)
