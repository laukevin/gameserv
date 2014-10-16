import gameserver
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/create/<username>", methods=['POST'])
def CreateToken(username):
  username = str(username)
  token = hash(username)
  if not gameserver.IsUser(token):
    gameserver.CreateUser(token)
  return str(token)

@app.route("/start", methods=['POST'])
def Start():
  user_token = int(request.form['token'])
  game_id = request.form['game_id']
  valid = validate(user_token, game_id)
  if not valid == True:
    return valid
  if gameserver.GetGameState(user_token, game_id):
    return jsonify(error=400, text='game is already in progress')
  start_state = gameserver.StartGame(user_token, game_id)
  return jsonify(state=start_state)

@app.route("/move", methods=['POST'])
def Move():
  user_token = int(request.form['token'])
  game_id = request.form['game_id']
  move = request.form['move']
  valid = validate(user_token, game_id)
  if not valid == True:
    return valid
  new_state = gameserver.Move(user_token, game_id, move)
  return jsonify(**new_state)

@app.route('/status', methods=['GET'])
def Status():
  user_token = int(request.args.get('token'))
  game_id = request.args.get('game_id')
  valid = validate(user_token, game_id)
  if not valid == True:
    return valid
  game_state = gameserver.GetGameState(user_token, game_id)
  if game_state == False:
    return jsonify(error=400, text='game not started')
  return jsonify(**game_state)

@app.route("/metrics", methods=['GET'])
def GetMetrics():
  user_token = int(request.args.get('token'))
  metrics = gameserver.GetMetric(user_token)
  return jsonify(**metrics)

@app.route("/allmetrics", methods=['GET'])
def GetAllMetrics():
  return json.dumps(gameserver.GetAllMetrics())

def validate(user_token, game_id):
  if not user_token or not game_id:
    return jsonify(error=400, text='no token or game_name')
  if not gameserver.IsUser(user_token):
    return jsonify(error=400, text='not a valid user')
  if not gameserver.IsGame(game_id):
    return jsonify(error=400, text='not a valid game')
  return True

if __name__ == "__main__":
  app.run()

