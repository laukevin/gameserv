import settings
import database
import time

def IsGame(game_id):
  if game_id in settings.active_games:
    return True
  return False

def IsUser(user_token):
  user = database.GetUser(user_token)
  if not user:
    return False
  timestamp = time.time()
  if timestamp - user['timestamp'] > settings.TIMEOUT_SETTINGS:
    return False
  return True

def CreateUser(user_token):
  timestamp = time.time()
  database.CreateUser(user_token, timestamp)

def GetGameState(user_token, game_id):
  game_state = database.GetGameState(user_token, game_id)
  if game_state:
    return {'state': game_state}
  return False

def StartGame(user_token, game_id):
  game_state = settings.active_games[game_id].start()
  database.CreateGame(user_token, game_id)
  database.UpdateState(user_token, game_id, game_state)
  return game_state

def ResetGame(user_token, game_id):
  game_state = settings.active_games[game_id].start()
  database.UpdateState(user_token, game_id, game_state)

def Move(user_token, game_id, move):
  game_state = database.GetGameState(user_token, game_id)
  new_game_state = settings.active_games[game_id].move(move, game_state)
  game_status = settings.active_games[game_id].status(new_game_state)
  database.UpdateState(user_token, game_id, new_game_state)
  move_result = {'state': new_game_state}
  if game_status == 1:
    move_result['status'] = 'won'
    database.AddGameResult(user_token, game_id, 'win')
    ResetGame(user_token, game_id)
  elif game_status == 0:
    move_result['status'] = 'lose'
    database.AddGameResult(user_token, game_id, 'lose')
    ResetGame(user_token, game_id)
  else:
    move_result['status'] = 'continue'
  return move_result

def CreateUserMetrics(user_info):
  keys = user_info.keys()
  print user_info
  for key in keys:
    if not key == '_id' and not key == 'timestamp':
      print user_info[key]
      del user_info[key]['state']
  return user_info

def GetMetric(user_token):
  user = database.GetPlayerStats(user_token)
  return CreateUserMetrics(user)

def GetAllMetrics():
  all_players = database.GetAllPlayers()
  all_users_info = []
  for player in all_players:
    all_users_info.append(CreateUserMetrics(player))
  return all_users_info

