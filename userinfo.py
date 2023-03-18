import requests

def get_user_info(steam_id):
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=354FE0F772D87A675323E45C5C8350AD&steamids={steam_id}"
            response = requests.get(url, timeout=5)                           
            return response.json()
        except requests.exceptions.Timeout:
            retry_count += 1
            if retry_count == max_retries:
                return {
                    "statusCode": 500,
                    "body": "The request to the Steam API timed out after multiple retries.",
                }
            
        except Exception as error:
            return {
                "statusCode": 500,
                "body": "An error occurred while fetching user information.",
            }
