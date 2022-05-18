import unittest
import os
import requests
import getwowdata
class TestEnvironmentVariables(unittest.TestCase):

    def test_client_id_environment_variable_set(self):
        try:
            os.environ["wow_api_id"]
        except KeyError:
            self.fail("Blizzard API client Id not set as environment variable")

    def test_secret_environment_variable_set(self):
        try:
            os.environ["wow_api_secret"]
        except KeyError:
            self.fail("Blizzard API secret not set as environment variable")

class TestGetFunctions(unittest.TestCase):
    access_token = getwowdata.get_access_token()
    
    def test__connected_realm_index_ok(self):
        try:
            response = getwowdata.get_connected_realm_index(self.access_token)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_connected_realm_index")
        
    def test_get_realm_ok(self):
        try:
            response = getwowdata.get_realm(self.access_token)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_realm")
        
    def test_get_auctions_ok(self):
        try:
            response = getwowdata.get_auctions(self.access_token)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_auctions")
        
    def test_get_profession_index_ok(self):
        try:
            response = getwowdata.get_profession_index(self.access_token)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_profession_index")
        
    def test_get_profession_tiers_ok(self):
        try:
            response = getwowdata.get_profession_tiers(self.access_token)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_profession_tiers")
        
    def test_get_profession_icon_ok(self):
        try:
            response = getwowdata.get_profession_icon(self.access_token)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_profession_icon")
        
    def test_get_profession_tier_details_ok(self):
        try:
            response = getwowdata.get_profession_tier_details(self.access_token)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_profession_tier_details")
        
    def test_get_recipe_details_ok(self):
        try:
            response = getwowdata.get_recipe_details(self.access_token)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_recipe_details")
        
    def test_get_recipe_icon_ok(self):
        try:
            response = getwowdata.get_recipe_icon(self.access_token)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_recipe_icon")
        
    def test_get_item_classes_ok(self):
        try:
            response = getwowdata.get_item_classes(self.access_token)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_item_classes")
        
    def test_get_item_subclasses_ok(self):
        try:
            response = getwowdata.get_item_subclasses(self.access_token)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_item_subclasses")

    def test_get_item_set_index_ok(self):
        try:
            response = getwowdata.get_item_set_index(self.access_token)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_item_set_index")
    
    def test_get_item_list_ok(self):
        try:
            response = getwowdata.get_item_list(self.access_token)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_item_list")

    def test_get_item_icon_ok(self):
        try:
            response = getwowdata.get_item_icon(self.access_token)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_item_icon")

    def test_get_wow_token_ok(self):
        try:
            response = getwowdata.get_wow_token(self.access_token)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail(f"{response.status_code} status code returned from get_wow_token")
