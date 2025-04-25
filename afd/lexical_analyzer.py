from afd import *
from symbol_table import *
class LexicalAnalyzer:
    def __init__(self, afd):
        self.afd = afd

    def analyze(self, file_path):
       symbol_table = SymbolTable()
       tokens = self.read_tokens(file_path)
       last_line_number = 1 
       for token, line_number in tokens:
           label = self.process_token(token)
           if not label:
                label = "REJECTED"  
           elif token in self.afd.tokens:
                label = token
           symbol_table.add_symbol({
                "line": line_number,
                "identifier": token,
                "label": label
            })
           last_line_number = line_number
       symbol_table.add_symbol({"line": last_line_number, "identifier": '$', "label": '$'})
       return symbol_table.table

            
    def process_token(self, token):
        # Checa não terminais (enclosed in < >)
        if token.startswith('<') and token.endswith('>'):
            return "NON_TERMINAL"
        # Checa operadores
        elif token in ['::=', '|']:
            return "OPERATOR"
        # Checa terminais (caracteres únicos ou ε)
        elif len(token) == 1 or token == 'ε':
            return "TERMINAL"
        return "REJECTED"

        
    
    def read_tokens(self, file_path):
        tokens_with_line = []       
        try:  
            with open(file_path, 'r') as file:  
                for line_number, line in enumerate(file, start=1):  
                    line = line.strip()
                    if line:
                            # Divide por espaços mas mantém < > juntos
                        tokens = []
                        current_token = ""
                        i = 0
                        while i < len(line):
                            if line[i] == '<':
                                if current_token:
                                    tokens.append(current_token)
                                    current_token = ""
                                while i < len(line) and line[i] != '>':
                                    current_token += line[i]
                                    i += 1
                                if i < len(line):
                                    current_token += line[i]
                                    i += 1
                                tokens.append(current_token)
                                current_token = ""
                            elif line[i] == ' ':
                                if current_token:
                                    tokens.append(current_token)
                                    current_token = ""
                                i += 1
                            else:
                                current_token += line[i]
                                i += 1
                        if current_token:
                            tokens.append(current_token)
                        tokens_with_line.extend((token, line_number) for token in tokens)
            return tokens_with_line
        except FileNotFoundError:   
            raise FileNotFoundError(f"File '{file_path}' not found.")
        except Exception as e:
            raise Exception(f"Error reading file '{file_path}': {e}")
            
    def print_symbol_table(self, symbol_table):
        print("Symbol Table:")
        print("Line\tIdentifier\tLabel")
        for symbol in symbol_table:
            print(f"\nLine: {symbol['line']}\tIdentifier: {symbol['identifier']}\tLabel: {symbol['label']}")
            
            