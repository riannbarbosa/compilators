from afd import *

class LexicalAnalyzer:
    def __init__(self, afd):
        self.afd = afd
        self.symbol_table = []
        self.errors = []

    def analyze(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        current_state = self.afd['initial_state']
        path = [current_state]
        
        for line_number, line in enumerate(lines, 1):
            if not line.strip():  # Skip empty lines
                continue
                
            tokens = line.strip().split()
            for token in tokens:
                if current_state in self.afd['transitions'] and token in self.afd['transitions'][current_state]:
                    current_state = self.afd['transitions'][current_state][token]
                    path.append(current_state)
                    
                    if token == 'count':
                        self.symbol_table.append({
                            'line': line_number,
                            'identifier': token,
                            'label': 'VARIABLE'
                        })
                    elif token in ['while', '=']:
                        self.symbol_table.append({
                            'line': line_number,
                            'identifier': token,
                            'label': 'KEYWORD'
                        })
                    elif token in ['<', '+']:
                        self.symbol_table.append({
                            'line': line_number,
                            'identifier': token,
                            'label': 'OPERATOR'
                        })
                    elif token in ['0', '1', '5']:
                        self.symbol_table.append({
                            'line': line_number,
                            'identifier': token,
                            'label': 'NUMBER'
                        })
                    elif token == ':':
                        self.symbol_table.append({
                            'line': line_number,
                            'identifier': token,
                            'label': 'SYMBOL'
                        })
                else:
                    self.errors.append({
                        'line': line_number,
                        'token': token,
                        'message': 'Token invalido "{}" no estado {}'.format(token, current_state)
                    })
                    return False, path, self.errors
        
        if current_state not in self.afd['final_states']:
            self.errors.append({
                'line': line_number,
                'token': '',
                'message': 'Codigo terminou em estado nao final: {}'.format(current_state)
            })
            return False, path, self.errors
            
        return True, path, self.errors

    def print_symbol_table(self):
        print("\nSymbol Table:")
        print("Line\tIdentifier\tLabel")
        print("-" * 40)
        for symbol in self.symbol_table:
            print("{}\t{}\t\t{}".format(
                symbol['line'],
                symbol['identifier'],
                symbol['label']
            ))

    def print_errors(self):
        if self.errors:
            print("\nErrors Found:")
            print("Line\tToken\t\tMessage")
            print("-" * 60)
            for error in self.errors:
                print("{}\t{}\t\t{}".format(
                    error['line'],
                    error['token'],
                    error['message']
                ))
        else:
            print("\nNo errors found.")
            
            