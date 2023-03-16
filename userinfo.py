import requests

def get_user_info(steam_id):
        try:
            url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=354FE0F772D87A675323E45C5C8350AD&steamids={steam_id}"
            response = requests.get(url)
            return response.json()
        except requests.exceptions.RequestException as e:       
            return {
                "statusCode": 500,
                "body": "An error occurred while fetching user information.",
            }            