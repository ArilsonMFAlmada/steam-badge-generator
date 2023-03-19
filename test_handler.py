import pytest
from unittest.mock import patch, MagicMock
from handler import lambda_handler

@pytest.fixture
def event():
    return {'steam_id': '12345', 'app_id': '67890'}

def test_generate_badge_all_trophies(event):
    user_info_mock = MagicMock(return_value={
        'response': {
            'players': [
                {'personaname': 'John'}
            ]
        }
    })
    gametrophies_mock = MagicMock(return_value={
        'playerstats': {
            'achievements': [
                {'apiname': 'trophy1', 'achieved': 1},
                {'apiname': 'trophy2', 'achieved': 1},
                {'apiname': 'trophy3', 'achieved': 1}
            ]
        }
    })
    gameinfo_mock = MagicMock(return_value={
        '67890': {
            'data': {
                'name': 'Test Game'
            }
        }
    })
    
    with patch('userinfo.get_user_info', user_info_mock), \
         patch('gametrophies.get_game_trophies', gametrophies_mock), \
         patch('gameinfo.get_game_info', gameinfo_mock):
             
        result = lambda_handler(event, None)
        
        assert result['statusCode'] == 200
        assert result['body'] == "Congratulations John! You have earned the All Trophies badge for the game Test Game"

def test_generate_badge_not_all_trophies(event):
    user_info_mock = MagicMock(return_value={
        'response': {
            'players': [
                {'personaname': 'John'}
            ]
        }
    })
    gametrophies_mock = MagicMock(return_value={
        'playerstats': {
            'achievements': [
                {'apiname': 'trophy1', 'achieved': 1},
                {'apiname': 'trophy2', 'achieved': 0},
                {'apiname': 'trophy3', 'achieved': 1}
            ]
        }
    })
    gameinfo_mock = MagicMock(return_value={
        '67890': {
            'data': {
                'name': 'Test Game'
            }
        }
    })
    
    with patch('userinfo.get_user_info', user_info_mock), \
         patch('gametrophies.get_game_trophies', gametrophies_mock), \
         patch('gameinfo.get_game_info', gameinfo_mock):
             
        result = lambda_handler(event, None)
        
        assert result['statusCode'] == 200
        assert result['body'] == "Sorry John, you haven't unlocked all the trophies for the game Test Game, so you didn't get the badge"

def test_generate_badge_no_trophies(event):
    user_info_mock = MagicMock(return_value={
        'response': {
            'players': [
                {'personaname': 'John'}
            ]
        }
    })
    gametrophies_mock = MagicMock(return_value={
        'playerstats': {
            'achievements': []
        }
    })
    gameinfo_mock = MagicMock(return_value={
        '67890': {
            'data': {
                'name': 'Test Game'
            }
        }
    })
    
    with patch('userinfo.get_user_info', user_info_mock), \
         patch('gametrophies.get_game_trophies', gametrophies_mock), \
         patch('gameinfo.get_game_info', gameinfo_mock):
             
        result = lambda_handler(event, None)
        
        assert result['statusCode'] == 200
        assert result['body'] == "No trophies found for this game."
