import unittest
import requests
import requests_mock
from handler import lambda_handler

class TestLambdaHandler(unittest.TestCase):
    @requests_mock.mock()
    def test_get_user_info_success(self, mock_request):
        mock_request.get("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=354FE0F772D87A675323E45C5C8350AD&steamids=123456789", json={'response': {'players': [{'personaname': 'John Doe'}]}})
        steam_id = 123456789
        result = lambda_handler({'steam_id': steam_id, 'app_id': 123}, {})
        self.assertEqual(result['statusCode'], 200)

    @requests_mock.mock()
    def test_get_user_info_failure(self, mock_request):
        mock_request.get("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=354FE0F772D87A675323E45C5C8350AD&steamids=123456789", exc=requests.exceptions.RequestException)
        steam_id = 123456789
        result = lambda_handler({'steam_id': steam_id, 'app_id': 123}, {})
        self.assertEqual(result['statusCode'], 500)
        self.assertEqual(result['body'], "An error occurred while fetching user information.")

    @requests_mock.mock()
    def test_get_game_info_success(self, mock_request):
        mock_request.get("https://store.steampowered.com/api/appdetails/?appids=123", json={'123': {'data': {'name': 'Game A'}}})
        app_id = 123
        result = lambda_handler({'steam_id': 123456789, 'app_id': app_id}, {})
        self.assertEqual(result['statusCode'], 200)

    @requests_mock.mock()
    def test_get_game_info_failure(self, mock_request):
        mock_request.get("https://store.steampowered.com/api/appdetails/?appids=123", exc=requests.exceptions.RequestException)
        app_id = 123
        result = lambda_handler({'steam_id': 123456789, 'app_id': app_id}, {})
        self.assertEqual(result['statusCode'], 500)
        self.assertEqual(result['body'], "An error occurred while fetching game information.")
    