from game import Game

class StateManager:
  def __init__(self, state):
    self.prev_states = []
    self.state = state
    self.go_to(state)

  def go_to(self, state):
    self.prev_states.append(self.state)
    self.state = state
    self.state.manager = self

  def go_back_state(self, amount=1):
    if not self.prev_states:
      print "Error: State manager cannot go back, no more states in stack."
      exit()
    else:
      for _ in range(amount):
        self.state = self.prev_states.pop()
      self.state.manager = self
