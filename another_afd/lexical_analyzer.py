from afd import *

class LexicalAnalyzer:
    def __init__(self, afd):
        self.afd = afd
        self.symbol_table = []
        self.errors = []

    def tokenize(self, line):
        delimiters = [':', '+', '=', '<']
        result = []
        current_token = ''
        for char in line:
            if char.isspace():
                if current_token:
                    result.append(current_token)
                    current_token = ""
            elif char in delimiters:
                if current_token:
                    result.append(current_token)
                    current_token = ""
                result.append(char)
            else:
                current_token += char
        if current_token:
            result.append(current_token)
        return result
                        
                        
    def classify_token(self, token):
        if token in ['count']:
            return 'VARIABLE'
        elif token in ['while', '=']:
            return 'KEYWORD'
        elif token in ['<', '+']:
            return 'OPERATOR'
        elif token in ['0', '1', '5']:
            return 'NUMBER'
        else:
            return 'INVALID'

    def transitions(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        path = []
        current_state = self.afd['initial_state']
        
        for line_number, line in enumerate(lines, 1):
            if not line.strip():  # Pula linhas vazias
                continue
                
            tokens = self.tokenize(line)
            for token in tokens:
                if current_state in self.afd['transitions'] and token in self.afd['transitions'][current_state]:
                    next_state = self.afd['transitions'][current_state][token]
                    path.append(next_state)
                    label = self.classify_token(token)
                    self.symbol_table.append({
                    'line': line_number,
                    'identifier': token,
                    'label': label
                     })
                    current_state = next_state
                else:
                # Transição inválida
                    self.errors.append({
                        'line': line_number,
                        'token': token,
                        'message': f'No transition for token "{token}" from state {current_state}'
                    })
                    label = 'INVALID'
                    
                    self.symbol_table.append({
                        'line': line_number,
                        'identifier': token,
                        'label': label
                    })

            # Verificar se terminou em um estado final
        if current_state not in self.afd['final_states']:
            self.errors.append({
                'line': line_number,
                'token': '',
                'message': f'Process ended in non-final state {current_state}'
            })
        
        return current_state in self.afd['final_states'], path, self.errors

    # def define_

    def print_symbol_table(self):
        print(self.errors)
        print("\nSymbol Table:")
        print("Line\tIdentifier\tLabel")
        print("-" * 40)
        for symbol in self.symbol_table:
            print("{}\t{}\t\t{}".format(
                symbol['line'],
                symbol['identifier'],
                symbol['label']
            ))