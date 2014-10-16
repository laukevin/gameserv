import abc

class AbstractGame(object):
  __metaclass__ = abc.ABCMeta

  @abc.abstractproperty
  def start(self):
  #needs to return the state of the game at the start
    pass

  @abc.abstractproperty
  #needs to return the state of the game after that move
  #can also include the move of an AI after the player makes a move
  #if the game has an AI
  def move(self, m, state):
    pass

  @abc.abstractproperty
  ##Returning a 1 means you have won the game
  ##Returning a 0 means you have lost the game
  ##Returning a 2 means the game is still playing
  def status(self, state):
    pass

class RandomGame(AbstractGame):
  def __init__(self):
    self.name = "random"

  def start(self):
    return 10

  def move(self, m, state):
    return state + int(m)

  def status(self, state):
    if state % 10 == 0:
      return 1
    elif state % 10 == 4:
      return 0
    else:
      return 2
