"""This module contains functions to query Blizzards World of Warcraft APIs.

Typical usage example:

access_token = get_access_token()

winterhoof_auctions = get_auctions(access_token, connected_realm_id = 4)
winterhoof_auctions.json()['auctions']

Copyright (c) 2022 JackBorah
MIT License see LICENSE for more details
"""

import os
import re
import requests
from . import exceptions


class GetWowData:
    """Creates an object with access_key, region, and, optionally, locale attributes.

    Attributes:
        region (str): Ex: 'us'. The region where the data will come from.
            See https://develop.battle.net/documentation/world-of-warcraft/guides/namespaces.
        locale (str): Ex: 'en_US'. The language data will be returned in.
            See https://develop.battle.net/documentation/world-of-warcraft/guides/localization.
        access_token (str): Required to query Blizzard APIs. See Setup in readme or
            visit https://develop.battle.net/ and click get started now.
        urls (dict): A collection of urls that will be queried by this classes' methods.
    """

    urls = {
        "access_token": "https://{region}.battle.net/oauth/token",
        "connected_realm_index": "https://{region}.api.blizzard.com/data/wow/connected-realm/index",
        "realm": "https://{region}.api.blizzard.com/data/wow/connected-realm/{connected_realm_id}",
        "auction": "https://{region}.api.blizzard.com/data/wow/connected-realm/{connected_realm_id}/auctions",
        "profession_index": "https://{region}.api.blizzard.com/data/wow/profession/index",
        "profession_skill_tier": "https://{region}.api.blizzard.com/data/wow/profession/{profession_id}",
        "profession_tier_detail": "https://{region}.api.blizzard.com/data/wow/profession/{profession_id}/skill-tier/{skill_tier_id}",
        "profession_icon": "https://{region}.api.blizzard.com/data/wow/media/profession/{profession_id}",
        "recipe_detail": "https://{region}.api.blizzard.com/data/wow/recipe/{recipe_id}",
        "repice_icon": "https://{region}.api.blizzard.com/data/wow/media/recipe/{recipe_id}",
        "item_classes": "https://{region}.api.blizzard.com/data/wow/item-class/index",
        "item_subclass": "https://{region}.api.blizzard.com/data/wow/item-class/{item_class_id}",
        "item_set_index": "https://{region}.api.blizzard.com/data/wow/item-set/index?",
        "item_icon": "https://{region}.api.blizzard.com/data/wow/media/item/{item_id}",
        "wow_token": "https://{region}.api.blizzard.com/data/wow/token/index",
        "search_realm": "https://{region}.api.blizzard.com/data/wow/search/connected-realm",
        "search_item": "https://{region}.api.blizzard.com/data/wow/search/item",
        "search_media": "https://{region}.api.blizzard.com/data/wow/search/media",
    }

    def __init__(
        self,
        region: str,
        locale: str = None,
        wow_api_id: str = None,
        wow_api_secret: str = None,
    ):
        """Sets the access_token and region attributes.

        Args:
            region (str): Example: 'us'. Should be lowercase. Access tokens will
                work for all other regions except 'cn' (China).
            locale (str): Example: 'en_US'. The language that data will be returned in.
                Default = None which returns the data in all supported languages.
                See https://develop.battle.net/documentation/world-of-warcraft/guides/localization.
            wow_api_id (str, optional): Your client id from https://develop.battle.net/.
                Ignore if id is set as environment variable.
            wow_api_secret (str, optional): Your client secret from https://develop.battle.net/.
                Ignore if secret is set as environment variable.
        """
        self.region = region
        self.locale = locale
        self.access_token = self.get_access_token(wow_api_id, wow_api_secret)

    def get_access_token(
        self,
        wow_api_id: str = None,
        wow_api_secret: str = None,
        timeout: int = 30,
    ) -> str:
        """Returns an access token.

        Requires wow_api_id and wow_api_secret to be set as environment variables or
        passed in. Remember not to expose your secret publicly. Each token expires
        after a day. Subsequent get_access_token calls returns the same token until
        it expires.

        Args:
            wow_api_id (str, optional): Your client id from https://develop.battle.net/.
                Ignore if id is set as environment variable.
            wow_api_secret (str, optional): Your client secret from https://develop.battle.net/.
                Ignore if secret is set as environment variable.
            timeout (int): How long (in seconds) until the request to the API timesout
                Default = 30 seconds.

        Returns:
            The access token as a string.

        Raises:
            NameError: If wow_api_id and/or wow_api_secret is not set as
                environment variable or passed in.
            requests.exceptions.HTTPError: If status code 4XX or 5XX.
            exceptions.JSONChangedError: If 'access_token' was not found in
                access_token_response.json()['access_token'].
        """

        token_data = {"grant_type": "client_credentials"}
        self.region = self.region

        try:
            auth = (os.environ["wow_api_id"], os.environ["wow_api_secret"])
            access_token_response = requests.post(
                self.urls["access_token"].format(region=self.region),
                data=token_data,
                auth=auth,
                timeout=timeout,
            )
            access_token_response.raise_for_status()
            try:
                return access_token_response.json()["access_token"]
            except KeyError:
                raise exceptions.JSONChangedError(
                    "access_token not found in access_token_response."
                    "The repsonse's format may have changed."
                ) from KeyError

        except KeyError:
            if wow_api_id is None or wow_api_secret is None:
                raise NameError(
                    "No wow_api_id or wow_api_secret was found."
                    "Set them as environment variables or "
                    "pass into get_access_token."
                ) from KeyError

            auth = (wow_api_id, wow_api_secret)
            access_token_response = requests.post(
                self.urls["access_token"].format(region=self.region),
                data=token_data,
                auth=auth,
                timeout=timeout,
            )
            access_token_response.raise_for_status()
            try:
                return access_token_response.json()["access_token"]
            except KeyError:
                raise exceptions.JSONChangedError(
                    "access_token not found in access_token_response."
                    "The repsonse's format may have changed."
                ) from KeyError

    def connected_realm_search(self, **extra_params: dict) -> dict:
        """Uses the connected realms API's search functionaly for more specific queries.

        Searches can filter by fields returned from the API.
        Ex: filerting realms by slug == illidan.
        Below is the data returned from a regular realm query.
        {
            "page": 1,
            "pageSize": 58,
            "maxPageSize": 100,
            "pageCount": 1,
            "results": [
            {
                ...
            },
            "data": {
                "realms": {
                    ...
                    "slug":"illidan"
                }
        To only return the realm with the slug == illidan pass
        {'data.realms.slug':'illidan'} into **extra_params.
        See https://develop.battle.net/documentation/world-of-warcraft/guides/search
        for more details on search.

        Args:
            **extra_params (int/str, optional): Returned data can be filtered
                by any of its fields. Useful parameters are listed below.
                Parameters must be sent as a dictionary where keys are str and
                values are str or int like {'_page': 1, 'realms.slug':'illidan', ...}
            **timeout (int): How long (in seconds) until the request to the API timesout
                Default = 30 seconds.
            **_pagesize (int, optional): Number of entries in a result page.
                Default = 100, min = 1, max = 1000.
            **_page (int, optional): The page number that will be returned.
                Default = 1.
            **orderby (str, optional): Accepts a comma seperated field of elements to sort by.
                See https://develop.battle.net/documentation/world-of-warcraft/guides/search.
            **data.realms.slug (str, optional): All realm slugs must be lowercase with spaces
                converted to dashes (-)

        Returns:
        A json looking dict with nested dicts and/or lists containing data from the API.
        """
        try:
            timeout = extra_params.pop("timeout", 30)
        except KeyError:
            timeout = 30

        params = {
            **{
                "namespace": f"dynamic-{self.region}",
                "access_token": self.access_token,
                "locale": self.locale,
            },
            **extra_params,
        }

        response = requests.get(
            self.urls["search_realm"].format(region=self.region),
            params=params,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()

    def item_search(self, **extra_params: dict) -> dict:
        """Uses the items API's search functionality to make more specific queries.

        Ex: Filter by required level and name
        {
        "page": 1,
        "pageSize": 3,
        "maxPageSize": 100,
        "pageCount": 1,
        "results": [
            {
                ...
            },
            "data": {
                "level": 35,
                "required_level": 30,
            ...
                ...
                name.en_US: Garrosh
        Pass {"required_level": 30, "name.en_US: "Garrosh"} into **extra_params
        Additional parameters must be sent as a dictionary where the keys strings and
        values are strings or ints.

        Args:
            **extra_params (int/str, optional): Returned data can be filtered by any
                of its fields. Useful parameters are listed below.
                Ex: {'data.required_level':35} will only return items where required_level == 35
            **timeout (int): How long (in seconds) until the request to the API timesout
                Default = 30 seconds.
            **_pagesize (int, optional): Number of entries in a result page.
                Default = 100, min = 1, max = 1000.
            **_page (int, optional): The page number that will be returned.
                Default = 1.
            **orderby (str, optional): Accepts a comma seperated field of elements to sort by.
                See https://develop.battle.net/documentation/world-of-warcraft/guides/search.
            **id (int, optional): An item's id. Enter in the following format
                {'id': '(id_start, id_end)'} to specify a set of id's.
                See https://develop.battle.net/documentation/world-of-warcraft/guides/search.

        Returns:
        A json looking dict with nested dicts and/or lists containing data from the API.
        """
        try:
            timeout = extra_params.pop("timeout", 30)
        except KeyError:
            timeout = 30

        params = {
            **{
                "namespace": f"static-{self.region}",
                "access_token": self.access_token,
                "locale": self.locale,
            }
            ** extra_params
        }

        response = requests.get(
            self.urls["search_item"].format(region=self.region),
            params=params,
            timeout=timeout,
        )
        return response.json()

    def get_connected_realms_by_id(
        self, connected_realm_id: int, timeout: int = 30
    ) -> dict:
        """Gets all the realms that share a connected_realm id.

        Args:
            connected_realm_id (int): The connected realm id. Get from connected_realm_index().
            timeout (int): How long (in seconds) until the request to the API timesout
                Default = 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        params = {
            "namespace": f"dynamic-{self.region}",
            "locale": self.locale,
            "access_token": self.access_token,
        }
        return requests.get(
            self.urls["realm"].format(
                self.region, connected_realm_id=connected_realm_id
            ),
            params=params,
            timeout=timeout,
        ).json()

    def get_auctions(self, connected_realm_id, timeout=30) -> dict:
        """Gets all auctions from a realm by its connected_realm_id.

        Args:
            connected_realm_id (int): The connected realm id.
                Get from connected_realm_index() or use connected_realm_search().
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        params = {
            "namespace": f"dynamic-{self.region}",
            "locale": self.locale,
            "access_token": self.access_token,
        }
        return requests.get(
            self.urls["auction"].format(
                region=self.region, connected_realm_id=connected_realm_id
            ),
            params=params,
            imeout=timeout,
        ).json()

    def get_profession_index(self, timeout=30) -> dict:
        """Gets all professions including their names and ids.

        Args:
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.


        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        params = {
            "namespace": f"static-{self.region}",
            "locale": self.locale,
            "access_token": self.access_token,
        }
        return requests.get(
            self.urls["profession_index"].format(region=self.region),
            params=params,
            timeout=timeout,
        ).json()

    # Includes skill tiers (classic, burning crusade, shadowlands, ...) id
    def get_profession_tiers(self, profession_id, timeout=30) -> dict:
        """Returns all profession teirs from a profession.

        A profession teir includes all the recipes from that expansion.
        Teir examples are classic, tbc, shadowlands, ...

        Args:
            profession_id (int): The profession's id. Found in get_profession_index().
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        params = {
            "namespace": f"static-{self.region}",
            "locale": self.locale,
            "access_token": self.access_token,
        }
        return requests.get(
            self.urls["profession_skill_tier"].format(
                region=self.region, profession_id=profession_id
            ),
            params=params,
            timeout=timeout,
        ).json()

    def get_profession_icon(self, profession_id, timeout=30) -> dict:
        """Returns a profession's icon.

        Args:
            profession_id (int): The profession's id. Found in get_profession_index().
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        params = {
            "namespace": f"static-{self.region}",
            "locale": self.locale,
            "access_token": self.access_token,
        }
        return requests.get(
            self.urls["profession_icon"].format(
                region=self.region, profession_id=profession_id
            ),
            params=params,
            timeout=timeout,
        ).json()

    # Includes the categories (weapon mods, belts, ...) and the recipes (id, name) in them
    def get_profession_tier_recipes(
        self, profession_id, skill_tier_id, timeout=30
    ) -> dict:
        """Returns all crafts from a skill teir.

        Args:
            profession_id (int): The profession's id. Found in get_profession_index().
            skill_tier_id (int): The skill teir id. Found in get_profession_teirs().
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        params = {
            "namespace": f"static-{self.region}",
            "locale": self.locale,
            "access_token": self.access_token,
        }
        return requests.get(
            self.urls["profession_tier_detail"].format(
                region=self.region,
                profession_id=profession_id,
                skill_tier_id=skill_tier_id,
            ),
            params=params,
            timeout=timeout,
        ).json()

    def get_recipe(self, recipe_id, timeout=30) -> dict:
        """Returns a recipes details by its id.

        Args:
            recipe_id (int): The recipe's id. Found in get_profession_tier_details().
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        return requests.get(
            self.urls["recipe_detail"].format(region=self.region, recipe_id=recipe_id),
            params={
                "namespace": f"static-{self.region}",
                "locale": self.locale,
                "access_token": self.access_token,
            },
            timeout=timeout,
        ).json()

    def get_recipe_icon(self, recipe_id, timeout=30) -> dict:
        """Returns a recipes icon.

        Args:
            recipe_id (int): The recipe's id. Found in get_profession_tier_details().
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        return requests.get(
            self.urls["repice_icon"].format(region=self.region, recipe_id=recipe_id),
            params={
                "namespace": f"static-{self.region}",
                "locale": self.locale,
                "access_token": self.access_token,
            },
            timeout=timeout,
        ).json()

    def get_item_classes(self, timeout=30) -> dict:
        """Returns all item classes (consumable, container, weapon, ...).

        Args:
            access_token (str): Returned from get_access_token().
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        return requests.get(
            self.urls["item_classes"].format(region=self.region),
            params={
                "namespace": f"static-{self.region}",
                "locale": self.locale,
                "access_token": self.access_token,
            },
            timeout=timeout,
        ).json()

    # flasks, vantus runes, ...
    def get_item_subclasses(self, item_class_id, timeout=30) -> dict:
        """Returns all item subclasses (class: consumable, subclass: potion, elixir, ...).

        Args:
            item_class_id (int): Item class id. Found with get_item_classes().
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        return requests.get(
            self.urls["item_subclass"].format(
                region=self.region, item_class_id=item_class_id
            ),
            params={
                "namespace": f"static-{self.region}",
                "locale": self.locale,
                "access_token": self.access_token,
            },
            timeout=timeout,
        ).json()

    def get_item_set_index(self, timeout=30) -> dict:
        """Returns all item sets. Ex: teir sets

        Args:
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        return requests.get(
            self.urls["item_set_index"].format(region=self.region),
            params={
                "namespace": f"static-{self.region}",
                "locale": self.locale,
                "access_token": self.access_token,
            },
            timeout=timeout,
        ).json()

    def get_item_icon(self, item_id, timeout=30) -> dict:
        """Returns the icon for an item.

        Args:
            item_id (int): The items id. Get from search() with api = item.
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        return requests.get(
            self.urls["item_icon"].format(region=self.region, item_id=item_id),
            params={
                "namespace": f"static-{self.region}",
                "locale": self.locale,
                "access_token": self.access_token,
            },
            timeout=timeout,
        ).json()

    def get_wow_token(self, timeout=30) -> dict:
        """Returns the price of the wow token and the timestamp of its last update.

        Args:
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        return requests.get(
            self.urls["wow_token"].format(region=self.region),
            params={
                "namespace": f"dynamic-{self.region}",
                "locale": self.locale,
                "access_token": self.access_token,
            },
            timeout=timeout,
        ).json()

    def get_connected_realm_index(self, timeout=30) -> dict:
        """Returns a dict where {key = Realm name: value = connected realm id}

        Args:
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A dict where {realm_name: connected_realm_id}
        """

        index = {}
        id_pattern = re.compile(r"[\d]+")

        response_index = self.connected_realm_search(timeout=timeout)
        for realms in response_index["connected_realms"]:
            realms_response = requests.get(
                realms["href"],
                params={"access_token": self.access_token, "locale": self.locale},
                timeout=timeout,
            ).json()

            for realm in realms_response["realms"]:
                connected_realm_id = id_pattern.search(realm["connected_realm"]["href"])
                index[realm["name"]] = connected_realm_id.group()

        return index
