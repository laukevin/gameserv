from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.games_database
collections = db.game_collection

def CreateUser(user_token, timestamp):
  user_document = { '_id': user_token, 'timestamp': timestamp }
  user_id = collections.insert(user_document)

def GetUser(user_token):
  user = collections.find_one({'_id': user_token})
  if user:
    return user
  return False

def GetGameState(user_token, game_id):
  user = collections.find_one({'_id': user_token})
  game_state = user[game_id]['state']
  return game_state

def CreateGame(user_token, game_id):
  game = {game_id: {}}
  collections.update({'_id': user_token}, {'$set': game})

def UpdateState(user_token, game_id, state):
  game_state_posn = str(game_id) + ".state"
  collections.update({'_id': user_token}, {'$set': {game_state_posn: state}})

def AddGameResult(user_token, game_id, result):
  game_total_posn = str(game_id) + ".total"
  game_result_posn = str(game_id) + "." + result
  collections.update({'_id': user_token}, {'$inc': {game_total_posn: 1}})
  collections.update({'_id': user_token}, {'$inc': {game_result_posn: 1}})

def GetPlayerStats(user_token):
  user = GetUser(user_token)
  return user

def GetAllPlayers():
  return collections.find({})
