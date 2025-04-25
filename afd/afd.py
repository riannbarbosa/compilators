from afnd import AFND
from states import STATE
import queue

class AFD(AFND):
    def __init__(self, path):
        self.afnd = AFND(path)
        super().__init__(path)
        self.table.clear()
        self.__make_deterministic()
        self._remove_unreachable_states()
        
    def __make_deterministic(self):
        afnd = self.afnd
        state_queue = queue.Queue()
        processed_states = set()
        
        start_state = afnd.findState('S')
        if start_state is None or start_state is False:
            raise ValueError("Estado inicial 'S' não encontrado no AFND. Verifique o arquivo de entrada.")
        state_queue.put(start_state)
        
        while not state_queue.empty():
            current_state = state_queue.get()
            if current_state.index in processed_states:
                continue
            processed_states.add(current_state.index)
            
            new_state = STATE(current_state.index)
            new_state.setFinal(current_state.final)
            
            for transition  in current_state.next_states:
                symbol = transition[0]
                next_states = transition[1:]
                
                if len(next_states) > 1:
                    combined_index = ''.join(sorted(next_states))
                    new_state.next_states.append([symbol, combined_index])
                    if combined_index not in processed_states:
                        combined_state = STATE(combined_index)
                        merged_transitions = self._merge_transitions(next_states)
                        combined_state.addNextStateArray(merged_transitions)
                        combined_state.setFinal(any(afnd.findState(s).final for s in next_states))
                        state_queue.put(combined_state)
                else:
                    next_state_index = next_states[0]
                    new_state.next_states.append([symbol, next_state_index])
                    if next_state_index not in processed_states:
                        state_queue.put(afnd.findState(next_state_index))
                        
                        
                    
            self.table.append(new_state)
            
    def _merge_transitions(self, state_indices):
        transition_dict = {}
        for index in state_indices:
            state = self.afnd.findState(index)
            for trans in state.next_states:
                symbol = trans[0]
                if symbol not in transition_dict:
                    transition_dict[symbol] = set()
                transition_dict[symbol].update(trans[1:])

        return [[symbol] + list(states) for symbol, states in transition_dict.items()]
    
    def _can_reach_final(self, start_index):
        visited = set()
        state_queue = queue.Queue()
        state_queue.put(start_index)
        visited.add(start_index)
        
        while not state_queue.empty():
            current_index = state_queue.get()
            current = self.findState(current_index)
            if current and current.final:
                return True
            if current:
                for trans in current.next_states:
                    for next_index in trans[1:]:
                        if next_index not in visited:
                            visited.add(next_index)
                            state_queue.put(next_index)
        return False
    
    def _remove_unreachable_states(self):
        states_to_remove = [state.index for state in self.table if not self._can_reach_final(state.index)]
        for state_index in states_to_remove:
            self.deleteState(state_index)
            
    def goTo(self, state_index, symbol):
        """Return the next state for a given symbol."""
        state = self.findState(state_index)
        if state:
            for trans in state.next_states:
                if trans[0] == symbol:
                    return trans[1]
        return False
    
    def deleteState(self, state_index):
        self.table = [state for state in self.table if state.index != state_index]
        for state in self.table:
            state.next_states = [t for t in state.next_states if state_index not in t[1:]]
            
    def findState(self, index):
        for state in self.table:
            if state.index == index:
                return state
        return None 
    