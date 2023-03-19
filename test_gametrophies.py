import requests_mock
import requests
import gametrophies

def test_get_game_info_successful():
    with requests_mock.Mocker() as m:
        mock_response = {
            "12345": {
                "data": "Some game data"
            }
        }
        m.get("https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=12345&key=354FE0F772D87A675323E45C5C8350AD&steamids&steamid=12345", json=mock_response)
        assert gametrophies.get_game_trophies("12345", "12345") == mock_response

def test_get_game_info_timeout_error():
    with requests_mock.Mocker() as m:
        m.get("https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=12345&key=354FE0F772D87A675323E45C5C8350AD&steamids&steamid=12345", exc=requests.exceptions.Timeout)
        expected_response = {
            "statusCode": 500,
            "body": "The request to the Steam API timed out after multiple retries."
        }
        assert gametrophies.get_game_trophies("12345", "12345") == expected_response

def test_get_game_info_general_error():
    with requests_mock.Mocker() as m:
        m.get("https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=12345&key=354FE0F772D87A675323E45C5C8350AD&steamids&steamid=12345", exc=Exception)
        expected_response = {
            "statusCode": 500,
            "body": "An error occurred while fetching user trophies information."
        }
        assert gametrophies.get_game_trophies("12345", "12345") == expected_response

