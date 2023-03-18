import requests_mock
import requests
from gameinfo import get_game_info

def test_get_game_info_successful():
    with requests_mock.Mocker() as m:
        mock_response = {
            "12345": {
                "data": "Some game data"
            }
        }
        m.get("https://store.steampowered.com/api/appdetails/?appids=12345", json=mock_response)
        assert get_game_info("12345") == mock_response

def test_get_game_info_timeout_error():
    with requests_mock.Mocker() as m:
        m.get("https://store.steampowered.com/api/appdetails/?appids=12345", exc=requests.exceptions.Timeout)
        expected_response = {
            "statusCode": 500,
            "body": "The request to the Steam API timed out after multiple retries."
        }
        assert get_game_info("12345") == expected_response

def test_get_game_info_general_error():
    with requests_mock.Mocker() as m:
        m.get("https://store.steampowered.com/api/appdetails/?appids=12345", exc=Exception)
        expected_response = {
            "statusCode": 500,
            "body": "An error occurred while fetching game information."
        }
        assert get_game_info("12345") == expected_response

