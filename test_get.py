import unittest
import os
import getResponse

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

    def test_get_access_token_200(self):
        response = getResponse.get_access_token()
        
