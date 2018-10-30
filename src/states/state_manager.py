from game import Game
import logging

class StateManager:
  def __init__(self, state):
    logging.info('Initializing Mr. Manager...')
    self.prev_states = []
    self.state = state
    self.go_to(state)

  def go_to(self, state):
    logging.info('Switching to state: {0}'.format(type(state)))
    self.prev_states.append(self.state)
    self.state = state
    self.state.manager = self

  def go_back_state(self, amount=1):
    if not self.prev_states:
      logging.critical("[!!] State manager cannot go back, no more states in stack.")
      exit()
    else:
      for _ in range(amount):
        self.state = self.prev_states.pop()
      self.state.manager = self
