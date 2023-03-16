import requests

def get_game_trophies(steam_id, app_id):
        try:
            url = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key=354FE0F772D87A675323E45C5C8350AD&steamids&steamid={steam_id}"
            response = requests.get(url)
            return response.json()   
        except requests.exceptions.RequestException as e:
            return {
                "statusCode": 500,
                "body": "An error occurred while fetching user trophies information."
            }