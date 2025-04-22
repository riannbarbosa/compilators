from afd import *
from symbol_table import *
class LexicalAnalyzer:
    def __init__(self, afd):
        self.afd = afd

    def analyze(self, file_path):
       symbol_table = SymbolTable()
       tokens = self.read_tokens(file_path)
       
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
       symbol_table.add_symbol({"line": line_number, "identifier": '$', "label": '$'})
       return symbol_table.table

            
    def process_token(self, token):
        current_state = 'S'
        for char in token:
            if char not in self.afd.symbols:
                return False
            current_state = self.afd.goTo(current_state, char)
            if not current_state:
                return False
        
    
    def read_tokens(self, file_path):
        tokens_with_line = []       
        try:  
            with open(file_path, 'r') as file:  
                for line_number, line in enumerate(file, start=1):  
                    line = line.strip()
                    if line:
                        tokens = line.split()
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
            
            