#!/usr/bin/env python3
"""Unit tests for validating nested dictionary access via the access_nested_map utility.

This module ensures that the access_nested_map function correctly traverses nested
dictionaries using a sequence of keys, returning the expected value or structure.
"""

import unittest
from parameterized import parameterized
from typing import Any, Dict, Tuple
from utils.utils import access_nested_map


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


# How to Run
# Requires parameterized and requests installed
# Run test
# python -m unittest test_utils.TestAccessNestedMap
