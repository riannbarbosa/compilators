import csv
from tabulate import tabulate
from lexical_analyzer import *
from afd import afd

import re
import os

class SintaticalAnalyzer:
    def __init__(self, parsing_table_file):
        self.parsing_table = self.load_parse(parsing_table_file)
        self.state_stack = [0]
        self.symbol_stack = []

        self.symbol_table = {}
        self.current_expression_value = None
        self.current_variable_stack = []

    def load_parse(self, parsing_table_file):
        parsing_table = {}
        with open(parsing_table_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            headers = next(reader)
            for row in reader:
                state = int(row[0])
                parsing_table[state] = {}
                for index, action in enumerate(row[0:]):
                    if action:
                        parsing_table[state][headers[index]] = action
                        
        return parsing_table
    
    def parse(self, tokens):
        self.input_stack = tokens
        while self.input_stack:
            estado_atual = self.state_stack[-1]
            token_data = self.input_stack[0]
            token = token_data['label']
            if token == 'INVALID':
                self.error(f"Syntax error at line {token_data['line']}: {token}")
                return
            
            action = self.parsing_table.get(estado_atual, {}).get(token, None)
            if action is None:
                self.error(f"Unexpected token '{token}' at line {token_data.get('line')}")
                return
            # FAZ SHIFT
            print(action)
            if action.startswith('s'):
                next_state = int(action[1:])
                self.input_stack.append(token_data)
                self.input_stack.pop(0)
                self.state_stack.append(next_state)
            # FAZ REDUCE
            elif action.startswith('r'):
                production_number = int(action[1:])
                if not self.reduce(production_number):
                    return
            elif action == 'acc' or action == '$' and action == 'acc':
                print("Input accepted.")
                return
            else:
                self.error(f"Invalid action '{action}' at state {estado_atual}")
                return

    def error(self, message):
        print(f"Syntax Error: {message}")

    def reduce(self, production):
        print('caiu aqi')
        if production == 0:
            # E' -> S
            self.state_stack.pop() # Pop S
            self.state_stack.append(self.goto(self.state_stack[-1], 'E\''))
        
        elif production == 1:
            # S -> epsilon
            self.state_stack.append(self.goto(self.state_stack[-1], 'S'))
            pass

        return True

if __name__ == '__main__':
    parsing_table_file = 'parsing_table.csv'
    # Provide actual productions dict matching parsing_table
    from lexical_analyzer import LexicalAnalyzer
    lexer = LexicalAnalyzer(afd)
    # Get tokens from lexical analyzer;;
    tokens = lexer.transitions('inputs/testinput.in')[3]
    parser = SintaticalAnalyzer(parsing_table_file)
    result = parser.parse(tokens)
    print('Parsing result:', result)

