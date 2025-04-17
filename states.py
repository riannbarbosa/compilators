class State:
    def __init__(self, initial: bool, id: int):
        self.initial = initial
        self.id = id
        self.isFinal = False
        self.nextStates = list()
        
    def nextState(self, symbol):
        for state in self.nextStates:
            if state.label == symbol:
                self.nextStates.append(state)
                return state
        self.nextStates.append(State(symbol))
        return self.nextStates[-1]
    
    def setFinal(self):
        self.isFinal = True
        
    def printStates(self):
        for state in self.nextStates:
            print(state.label, end=" ")
        print()
        
    
    