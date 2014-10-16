import inspect
import games

TIMEOUT_SETTINGS = 1000 * 60 * 60 * 24 #1 day

active_games = {}

for name, obj in inspect.getmembers(games):
  if inspect.isclass(obj) and not inspect.isabstract(obj):
    active_game = obj()
    active_games[active_game.name] = active_game
