from botocore.vendored import requests
import logging
 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', handlers=[logging.StreamHandler()])

def lambda_handler(event, context):
    steam_id = event['steam_id']
    app_id = event['app_id']
    
    def get_user_info(steam_id):
        try:
            url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=354FE0F772D87A675323E45C5C8350AD&steamids={steam_id}"
            response = requests.get(url)
            return response.json()
        except requests.exceptions.RequestException as e:
        # Handle the exception here
            return {
                "statusCode": 500,
                "body": "An error occurred while fetching user information.",
            }            
          
    def get_game_info(app_id):
        try:
            url = f"https://store.steampowered.com/api/appdetails/?appids={app_id}"
            response = requests.get(url)
            return response.json()   
        except requests.exceptions.RequestException as e:
        # Handle the exception here
            return {
                "statusCode": 500,
                "body": "An error occurred while fetching game information."
            }
            
    def get_game_trophies(steam_id, app_id):
        try:
            url = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key=354FE0F772D87A675323E45C5C8350AD&steamids&steamid={steam_id}"
            response = requests.get(url)
            return response.json()   
        except requests.exceptions.RequestException as e:
        # Handle the exception here
            return {
                "statusCode": 500,
                "body": "An error occurred while fetching user trophies information."
            }
            
    game_info = get_game_info(app_id)
    game_name = game_info[app_id]["data"]["name"]    
  
    logging.info("generating badge")
    def generate_badge(steam_id, app_id):
        try:
            logging.info("fetching user information")
            user_info = get_user_info(steam_id)

            logging.info("fetching user trophies information")           
            game_trophies = get_game_trophies(steam_id, app_id)

            logging.info("fetching game information") 
            game_info = get_game_info(app_id)
            game_name = game_info[app_id]["data"]["name"]

            if game_trophies['playerstats']['achievements']:
                all_trophies = True
                for trophy in game_trophies['playerstats']['achievements']:
                    if trophy['achieved'] == 0:
                        all_trophies = False
                        break

                if all_trophies:
                    logging.info("drawing the badge")
                                        
                    return {
                        "statusCode": 200,
                        "body": f"Congratulations {user_info['response']['players'][0]['personaname']}! You have earned the All Trophies badge for the game {game_name}",
                    }                
                else:
                    return {
                        "statusCode": 200,
                        "body": f"Sorry {user_info['response']['players'][0]['personaname']}, you haven't unlocked all the trophies for the game {game_name}, so you didn't get the badge"
                    }
            else:
                return {
                    "statusCode": 200,
                    "body": "No trophies found for this game."
                }
        except Exception as e:
        # Handle the exception here
            return {
                "statusCode": 500,
                "body": "An error occurred while generating the badge."
            }

    return generate_badge(steam_id, app_id)
    
