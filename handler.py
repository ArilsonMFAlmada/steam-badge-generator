import logging
import gameinfo
import gametrophies
import userinfo
import json
 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s',
                     datefmt='%m/%d/%Y %I:%M:%S %p', 
                     handlers=[logging.StreamHandler()])

def lambda_handler(event, context):
    logging.info(f"Received event: {event}")

    event = json.loads(event['body'])
    steam_id = str(event['steam_id'])
    app_id = str(event['app_id'])           
  
    def generate_badge(steam_id, app_id):      
       
        logging.info("fetching user information")
        user_info = userinfo.get_user_info(steam_id)

        logging.info("fetching user trophies information")           
        game_trophies = gametrophies.get_game_trophies(steam_id, app_id)

        logging.info("fetching game information") 
        game_info = gameinfo.get_game_info(app_id)
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
                    "body": json.dumps(f"Congratulations {user_info['response']['players'][0]['personaname']}! You have earned the All Trophies badge for the game {game_name}"),
                    "headers": {
                        "Content-Type": "application/json"
                    }
                }                
            else:
                return {
                    "statusCode": 200,
                    "body": f"Sorry {user_info['response']['players'][0]['personaname']}, you haven't unlocked all the trophies for the game {game_name}, so you didn't get the badge",
                    "headers": {
                        "Content-Type": "application/json"
                    }
                }
        else:
            return {
                "statusCode": 200,
                "body": "No trophies found for this game.",
                "headers": {
                        "Content-Type": "application/json"
                }
            }          

    return generate_badge(steam_id, app_id)
    
