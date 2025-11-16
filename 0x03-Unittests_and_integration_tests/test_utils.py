#!/usr/bin/env python3
"""Unit tests for validating nested dictionary access via the access_nested_map utility.

This module ensures that the access_nested_map function correctly traverses nested
dictionaries using a sequence of keys, returning the expected value or structure.
"""

import unittest
from parameterized import parameterized
from typing import Any, Dict, Tuple
from utils.utils import access_nested_map
from unittest import TestCase
from unittest.mock import patch, Mock
from utils import get_json


class TestAccessNestedMap(unittest.TestCase):
    """Structured test suite for access_nested_map, verifying key-path resolution in nested mappings.

    These tests confirm that the utility behaves predictably across varying depths of nested
    dictionaries, ensuring robust access logic for both intermediate and terminal values.
    """

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(
        self, nested_map: Dict[str, Any], path: Tuple[str, ...], expected: Any
    ) -> None:
        """Assert that access_nested_map returns the correct value for a given key path.

        Args:
            nested_map (Dict[str, Any]): The dictionary to traverse.
            path (Tuple[str, ...]): A sequence of keys representing the access path.
            expected (Any): The expected value retrieved from the nested structure.

        Raises:
            AssertionError: If the returned value does not match the expected result.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    # 🧪 Parameterized test for exception handling in access_nested_map
    # Validates that a KeyError is raised when accessing missing keys in nested maps.
    # Ensures the exception message matches the final key in the path.

    @parameterized.expand(
        [
            ({}, ("a",)),
            ({"a": 1}, ("a", "b")),
        ]
    )
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that access_nested_map raises KeyError with correct message"""
        with self.assertRaises(KeyError) as ctx:
            access_nested_map(nested_map, path)
        self.assertEqual(str(ctx.exception), f"'{path[-1]}'")


"""
Unit tests for the `utils.get_json` function.

This module tests that `get_json` correctly retrieves and returns JSON data
from a given URL using mocked HTTP GET requests.
"""


class TestGetJson(TestCase):
    """Test suite for the `get_json` utility function."""

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    def test_get_json(
        self, test_url: str, test_payload: Dict[str, Any]
    ) -> None:
        """
        Test that `get_json` returns the expected payload from a mocked HTTP GET request.

        Args:
            test_url (str): The URL to fetch JSON from.
            test_payload (Dict[str, Any]): The expected JSON payload to be returned.
        """
        with patch("utils.get_json.requests.get") as mock_get:
            # Create a mock response object with a .json() method
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            # Call the function under test
            result = get_json(test_url)

            # Ensure requests.get was called exactly once with the correct URL
            mock_get.assert_called_once_with(test_url)

            # Verify the returned result matches the expected payload
            self.assertEqual(result, test_payload)


# How to Run
# Requires parameterized and requests installed
# Run test
# python -m unittest test_utils.TestAccessNestedMap
