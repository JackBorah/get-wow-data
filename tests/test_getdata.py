"""This module contains tests for the getwowdata package.

Copyright (c) 2022 JackBorah
MIT License see LICENSE for more details
"""

import unittest
from unittest import mock
import os
import requests
import responses
from responses import matchers
from getwowdata import WowApi
from getwowdata.exceptions import JSONChangedError
from getwowdata.urls import urls


class TestWowApiMethods(unittest.TestCase):
    """Test that all functions from getdata.py returns correctly."""

    """
    functional test data
    #format defaults
    connected_realm_id = 4
    profession_id = 164
    skill_tier_id = 2437
    recipe_id = 1631
    item_class_id = 1
    item_id = 19019

    wow_api = []
    regions = ['us', 'eu', 'kr']

    for index, region in enumerate(regions):
        api_instance = WowApi(region, 'en_US')
        #formats all urls for use in responses
        for key, url in api_instance.urls.items():
            api_instance.urls[key] = url.format(region=region,
            connected_realm_id=connected_realm_id,
            profession_id=profession_id,
            skill_tier_id=skill_tier_id,
            recipe_id=recipe_id,
            item_class_id=item_class_id,
            item_id=item_id
            )
        wow_api.append(api_instance)
    """

    region = "us"

    # Make mock env for all functions?
    # Yes tests should not need actual data set

    @responses.activate
    def test_get_access_token_from_env(self):
        """Test get_access_token() with environment variables."""
        with mock.patch.dict(
            os.environ, {"wow_api_id": "valid", "wow_api_secret": "valid"}
        ):
            responses.post(
                urls["access_token"].format(region=self.region),
                json={"access_token": "0000000000000000000000000000000000"},
            )
            wow_api = WowApi(self.region, "en_US")
            token = wow_api.get_access_token()
            self.assertEqual(type(token), str)
            self.assertEqual(len(token), 34)

    @responses.activate
    def test_get_access_token_from_arg(self):
        """Test get_access_token() with function arguments."""
        with mock.patch.dict(os.environ, {}, clear=True):
            responses.post(
                urls["access_token"].format(region=self.region),
                json={"access_token": "0000000000000000000000000000000000"},
            )
            wow_api = WowApi(
                self.region,
                locale="en_US",
                wow_api_id="wow_api_id",
                wow_api_secret="wow_api_secret",
            )
            token = wow_api.get_access_token()
            self.assertEqual(type(token), str)
            self.assertEqual(len(token), 34)

    @responses.activate
    def test_get_access_token_raises_JSONChangedError_from_env(self):
        """Test get_access_token() raises JSONChangedError with env."""
        with mock.patch.dict(
            os.environ, {"wow_api_id": "valid", "wow_api_secret": "valid"}
        ):
            responses.post(
                urls["access_token"].format(region=self.region),
                json={"access_token_not_found": "0000000000000000000000000000000000"},
            )
            with self.assertRaises(JSONChangedError):
                WowApi(self.region, "en_US")

    @responses.activate
    def test_get_access_token_raises_JSONChangedError_from_arg(self):
        """Test get_access_token() raises JSONChangedError with args."""
        with mock.patch.dict(os.environ, {}, clear=True):

            responses.post(
                urls["access_token"].format(region=self.region),
                json={"access_token_not_found": "0000000000000000000000000000000000"},
            )
            with self.assertRaises(JSONChangedError):
                wow_api = WowApi(
                    self.region,
                    locale="en_US",
                    wow_api_id="wow_api_id",
                    wow_api_secret="wow_api_secret",
                )

    @responses.activate
    def test_get_access_token_no_env_or_param(self):
        """Test get_access_token() raises NameError
        when no wow_api_id or secret is passed in or an env.
        """

        with mock.patch.dict(os.environ, {}, clear=True):
            responses.post(
                urls["access_token"].format(region=self.region),
                json={"access_token_not_found": "0000000000000000000000000000000000"},
            )
            with self.assertRaises(NameError):
                WowApi(self.region, locale="en_US")

    @responses.activate
    def connected_realm_search_timeout_in_querystring(self):
        """Assert that timeout is a part of the querystring"""
        responses.get(urls["search_realm"].format(region=self.region),
            json={"Test worked"}
        )
        wow_api = WowApi(
                    self.region,
                    locale="en_US",
                    wow_api_id="wow_api_id",
                    wow_api_secret="wow_api_secret",
                )
        self.assertEqual(wow_api.connected_realm_search(), "Test worked")


if __name__ == "__main__":
    unittest.main()
