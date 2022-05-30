"""This module contains tests for the getwowdata package.

Copyright (c) 2022 JackBorah
MIT License see LICENSE for more details
"""

import unittest
from unittest import mock
import os
import responses
from getwowdata import WowApi
from getwowdata.exceptions import JSONChangedError
from getwowdata.urls import urls


class TestWowApiMethods(unittest.TestCase):
    """Test that all functions from getdata.py returns correctly."""

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
            token = wow_api._get_access_token()
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
            token = wow_api._get_access_token()
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
                WowApi(
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
    def test_connected_realm_search(self):
        """Assert that connected_realm_search returns the proper value."""
        responses.post(
            urls["access_token"].format(region=self.region),
            json={"access_token": "0000000000000000000000000000000000"},
        )
        responses.get(
            urls["search_realm"].format(region=self.region),
            json={"sucess": "Test worked"},
        )
        wow_api = WowApi(
            self.region,
            locale="en_US",
            wow_api_id="wow_api_id",
            wow_api_secret="wow_api_secret",
        )

        self.assertEqual(wow_api.connected_realm_search(), {"sucess": "Test worked"})

    @responses.activate
    def test_item_search(self):
        """Assert that item_search returns the proper value."""
        responses.post(
            urls["access_token"].format(region=self.region),
            json={"access_token": "0000000000000000000000000000000000"},
        )
        responses.get(
            urls["search_item"].format(region=self.region),
            json={"sucess": "Test worked"},
        )
        wow_api = WowApi(
            self.region,
            locale="en_US",
            wow_api_id="wow_api_id",
            wow_api_secret="wow_api_secret",
        )

        self.assertEqual(wow_api.item_search(), {"sucess": "Test worked"})

    @responses.activate
    def test_get_connected_realms_by_id(self):
        """Assert that get_connected_realms_by_id returns the proper value."""
        responses.post(
            urls["access_token"].format(region=self.region),
            json={"access_token": "0000000000000000000000000000000000"},
        )
        responses.get(
            urls["realm"].format(region=self.region, connected_realm_id=4),
            json={"sucess": "Test worked"},
        )
        wow_api = WowApi(
            self.region,
            locale="en_US",
            wow_api_id="wow_api_id",
            wow_api_secret="wow_api_secret",
        )

        self.assertEqual(
            wow_api.get_connected_realms_by_id(4), {"sucess": "Test worked"}
        )

    @responses.activate
    def test_get_auctions(self):
        """Assert that get_auctions returns the proper value."""
        responses.post(
            urls["access_token"].format(region=self.region),
            json={"access_token": "0000000000000000000000000000000000"},
        )
        responses.get(
            urls["auction"].format(region=self.region, connected_realm_id=4),
            json={"sucess": "Test worked"},
        )
        wow_api = WowApi(
            self.region,
            locale="en_US",
            wow_api_id="wow_api_id",
            wow_api_secret="wow_api_secret",
        )

        self.assertEqual(wow_api.get_auctions(4), {"sucess": "Test worked"})

    @responses.activate
    def test_get_profession_index(self):
        """Assert that get_profession_index returns the proper value."""
        responses.post(
            urls["access_token"].format(region=self.region),
            json={"access_token": "0000000000000000000000000000000000"},
        )
        responses.get(
            urls["profession_index"].format(region=self.region),
            json={"sucess": "Test worked"},
        )
        wow_api = WowApi(
            self.region,
            locale="en_US",
            wow_api_id="wow_api_id",
            wow_api_secret="wow_api_secret",
        )

        self.assertEqual(wow_api.get_profession_index(), {"sucess": "Test worked"})

    @responses.activate
    def test_get_profession_tiers(self):
        """Assert that get_profession_tiers returns the proper value."""
        responses.post(
            urls["access_token"].format(region=self.region),
            json={"access_token": "0000000000000000000000000000000000"},
        )
        responses.get(
            urls["profession_skill_tier"].format(region=self.region, profession_id=1),
            json={"sucess": "Test worked"},
        )
        wow_api = WowApi(
            self.region,
            locale="en_US",
            wow_api_id="wow_api_id",
            wow_api_secret="wow_api_secret",
        )

        self.assertEqual(wow_api.get_profession_tiers(1), {"sucess": "Test worked"})

    @responses.activate
    def test_get_profession_icon(self):
        """Assert that get_profession_icon returns the proper value."""
        responses.post(
            urls["access_token"].format(region=self.region),
            json={"access_token": "0000000000000000000000000000000000"},
        )
        responses.get(
            urls["profession_icon"].format(region=self.region, profession_id=1),
            json={"assets": [{"value": urls["icon_test"]}]},
        )
        responses.get(
            "https://render.worldofwarcraft.com/",
            body="test",
        )
        wow_api = WowApi(
            self.region,
            locale="en_US",
            wow_api_id="wow_api_id",
            wow_api_secret="wow_api_secret",
        )

        self.assertEqual(wow_api.get_profession_icon(1), b"test")

    @responses.activate
    def test_get_profession_tier_recipes(self):
        """Assert that get_profession_tier_recipes returns the proper value."""
        responses.post(
            urls["access_token"].format(region=self.region),
            json={"access_token": "0000000000000000000000000000000000"},
        )
        responses.get(
            urls["profession_tier_detail"].format(
                region=self.region, profession_id=1, skill_tier_id=2
            ),
            json={"sucess": "Test worked"},
        )
        wow_api = WowApi(
            self.region,
            locale="en_US",
            wow_api_id="wow_api_id",
            wow_api_secret="wow_api_secret",
        )

        self.assertEqual(
            wow_api.get_profession_tier_recipes(1, 2), {"sucess": "Test worked"}
        )

    @responses.activate
    def test_get_recipe(self):
        """Assert that get_recipe returns the proper value."""
        responses.post(
            urls["access_token"].format(region=self.region),
            json={"access_token": "0000000000000000000000000000000000"},
        )
        responses.get(
            urls["recipe_detail"].format(region=self.region, recipe_id=1),
            json={"sucess": "Test worked"},
        )
        wow_api = WowApi(
            self.region,
            locale="en_US",
            wow_api_id="wow_api_id",
            wow_api_secret="wow_api_secret",
        )

        self.assertEqual(wow_api.get_recipe(1), {"sucess": "Test worked"})

    @responses.activate
    def test_get_recipe_icon(self):
        """Assert that get_recipe_icon returns the proper value."""
        responses.post(
            urls["access_token"].format(region=self.region),
            json={"access_token": "0000000000000000000000000000000000"},
        )
        responses.get(
            urls["repice_icon"].format(region=self.region, recipe_id=1),
            json={"assets": [{"value": "https://render.worldofwarcraft.com/"}]},
        )
        responses.get(
            "https://render.worldofwarcraft.com/",
            body="test",
        )
        wow_api = WowApi(
            self.region,
            locale="en_US",
            wow_api_id="wow_api_id",
            wow_api_secret="wow_api_secret",
        )

        self.assertEqual(wow_api.get_recipe_icon(1), b"test")

    @responses.activate
    def test_get_item_classes(self):
        """Assert that get_item_classes returns the proper value."""
        responses.post(
            urls["access_token"].format(region=self.region),
            json={"access_token": "0000000000000000000000000000000000"},
        )
        responses.get(
            urls["item_classes"].format(region=self.region),
            json={"sucess": "Test worked"},
        )
        wow_api = WowApi(
            self.region,
            locale="en_US",
            wow_api_id="wow_api_id",
            wow_api_secret="wow_api_secret",
        )

        self.assertEqual(wow_api.get_item_classes(), {"sucess": "Test worked"})

    @responses.activate
    def test_get_item_subclasses(self):
        """Assert that get_item_subclasses returns the proper value."""
        responses.post(
            urls["access_token"].format(region=self.region),
            json={"access_token": "0000000000000000000000000000000000"},
        )
        responses.get(
            urls["item_subclass"].format(region=self.region, item_class_id=1),
            json={"sucess": "Test worked"},
        )
        wow_api = WowApi(
            self.region,
            locale="en_US",
            wow_api_id="wow_api_id",
            wow_api_secret="wow_api_secret",
        )

        self.assertEqual(wow_api.get_item_subclasses(1), {"sucess": "Test worked"})

    @responses.activate
    def test_get_item_set_index(self):
        """Assert that get_item_set_index returns the proper value."""
        responses.post(
            urls["access_token"].format(region=self.region),
            json={"access_token": "0000000000000000000000000000000000"},
        )
        responses.get(
            urls["item_set_index"].format(region=self.region),
            json={"sucess": "Test worked"},
        )
        wow_api = WowApi(
            self.region,
            locale="en_US",
            wow_api_id="wow_api_id",
            wow_api_secret="wow_api_secret",
        )

        self.assertEqual(wow_api.get_item_set_index(), {"sucess": "Test worked"})

    @responses.activate
    def test_get_item_icon(self):
        """Assert that get_item_icon returns the proper value."""
        responses.post(
            urls["access_token"].format(region=self.region),
            json={"access_token": "0000000000000000000000000000000000"},
        )
        responses.get(
            urls["item_icon"].format(region=self.region, item_id=1),
            json={"assets": [{"value": "https://render.worldofwarcraft.com/"}]},
        )
        responses.get(
            "https://render.worldofwarcraft.com/",
            body="test",
        )
        wow_api = WowApi(
            self.region,
            locale="en_US",
            wow_api_id="wow_api_id",
            wow_api_secret="wow_api_secret",
        )

        self.assertEqual(wow_api.get_item_icon(1), b"test")

    @responses.activate
    def test_get_wow_token(self):
        """Assert that get_wow_token returns the proper value."""
        responses.post(
            urls["access_token"].format(region=self.region),
            json={"access_token": "0000000000000000000000000000000000"},
        )
        responses.get(
            urls["wow_token"].format(region=self.region),
            json={"sucess": "Test worked"},
        )
        wow_api = WowApi(
            self.region,
            locale="en_US",
            wow_api_id="wow_api_id",
            wow_api_secret="wow_api_secret",
        )

        self.assertEqual(wow_api.get_wow_token(), {"sucess": "Test worked"})

    @responses.activate
    def test_get_connected_realm_index(self):
        """Assert that get_connected_realm_index returns the proper value."""
        #connected_realm_search returns results[] where each index in a connected-realm cluster
        #each cluster has its own href linking to itself and the slugs of the individual realms
        search_realm_json = {
            "results": [
                {
                    "key": {"href": "1"},
                    "data": {"realms": [{"slug": "Test worked"}]}
                }
            ]
        }
        responses.post(
            urls["access_token"].format(region=self.region),
            json={"access_token": "0000000000000000000000000000000000"},
        )
        responses.get(
            urls["search_realm"].format(region=self.region),
            json=search_realm_json,
        )
        wow_api = WowApi(
            self.region,
            locale="en_US",
            wow_api_id="wow_api_id",
            wow_api_secret="wow_api_secret",
        )

        self.assertEqual(wow_api.get_connected_realm_index(), {"Test worked": "1"})


if __name__ == "__main__":
    unittest.main()
