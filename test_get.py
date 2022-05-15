import unittest
import os
import getResponse
import requests

class TestEnvironmentVariables(unittest.TestCase):

    def test_client_id_environment_variable_set(self):
        try:
            os.environ["wowApiId"]
        except KeyError:
            self.fail("Blizzard API client Id not set as environment variable")

    def test_secret_environment_variable_set(self):
        try:
            os.environ["wowApiSecret"]
        except KeyError:
            self.fail("Blizzard API secret not set as environment variable")

class TestGetFunctions(unittest.TestCase):

    def test_get_access_token_status_code_ok(self):
        try:
            response = getResponse.get_access_token()
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_access_token")
    
    def test_get_connected_realm_index_ok(self):
        try:
            response = getResponse.get_connected_realm_index()
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_connected_realm_index")
        
    def test_get_realm_ok(self):
        try:
            response = getResponse.get_realm()
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_realm")
        
    def test_get_auctions_ok(self):
        try:
            response = getResponse.get_auctions()
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_auctions")
        
    def test_get_profession_index_ok(self):
        try:
            response = getResponse.get_profession_index()
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_profession_index")
        
    def test_get_profession_tiers_ok(self):
        try:
            response = getResponse.get_profession_tiers()
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_profession_tiers")
        
    def test_get_profession_icon_ok(self):
        try:
            response = getResponse.get_profession_icon()
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_profession_icon")
        
    def test_get_profession_tier_details_ok(self):
        try:
            response = getResponse.get_profession_tier_details()
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_profession_tier_details")
        
    def test_get_recipe_details_ok(self):
        try:
            response = getResponse.get_recipe_details()
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_recipe_details")
        
    def test_get_recipe_icon_ok(self):
        try:
            response = getResponse.get_recipe_icon()
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_recipe_icon")
        
    def test_get_item_classes_ok(self):
        try:
            response = getResponse.get_item_classes()
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_item_classes")
        
    def test_get_item_subclasses_ok(self):
        try:
            response = getResponse.get_item_subclasses()
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_item_subclasses")

    def test_get_item_set_index_ok(self):
        try:
            response = getResponse.get_item_set_index()
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_item_set_index")
    
    def test_get_item_list_ok(self):
        try:
            response = getResponse.get_item_list()
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_item_list")

    def test_get_item_icon_ok(self):
        try:
            response = getResponse.get_item_icon()
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_item_icon")

    def test_get_wow_token_ok(self):
        try:
            response = getResponse.get_wow_token()
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_wow_token")
