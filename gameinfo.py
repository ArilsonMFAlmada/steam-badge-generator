import requests

def get_game_info(app_id):
        try:
            url = f"https://store.steampowered.com/api/appdetails/?appids={app_id}"
            response = requests.get(url)
            return response.json()   
        except requests.exceptions.RequestException as e:
            return {
                "statusCode": 500,
                "body": "An error occurred while fetching game information."
            }