import tabulate as table
from states import State
import re

class AFND:
    def __init__(self, path, list_regular_grammar, list_tokens) -> None:
        self.tokens = list_tokens
        self.states = list()
        self.identifier = 0
        self.regular_grammar = list_regular_grammar
        self.table = list()
        
    def processTokens(self):
        for token in self.tokens:
            if(len(token) == 0):
                continue
            if(len(self.states) == 0):
               initial_state = State(True, self.identifier)
               self.states.append(initial_state)
               self.identifier += 1 
            else:
                for state in self.states:
                    if(state.label == token):
                        self.states.append(state)
                        state = state
                        


