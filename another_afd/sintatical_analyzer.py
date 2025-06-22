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
            reader = csv.reader(csvfile)
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
        print(f"Reducing production {production} with current state stack: {self.state_stack}")
        if production == 1:
            # S -> ε
            # Não remove nada da pilha (ε = vazio)
            goto_state = self.goto(self.state_stack[-1], "S")
            self.state_stack.append(goto_state)
        elif production == 2:
            # S -> let var = E
            for _ in range(4):  # Remove E, =, var, let
                self.state_stack.pop()
            goto_state = self.goto(self.state_stack[-1], "S")
            self.state_stack.append(goto_state)
        elif production == 3:
            # E -> TRUE
            self.state_stack.pop()  # Remove TRUE
            goto_state = self.goto(self.state_stack[-1], "E")
            self.state_stack.append(goto_state)
        elif production == 4:
            # E -> FALSE
            self.state_stack.pop()  # Remove FALSE
            goto_state = self.goto(self.state_stack[-1], "E")
            self.state_stack.append(goto_state)
        elif production == 5:
            # E -> var
            self.state_stack.pop()  # Remove var
            goto_state = self.goto(self.state_stack[-1], "E")
            self.state_stack.append(goto_state)
        elif production == 6:
            # E -> { C }
            for _ in range(3):  # Remove }, C, {
                self.state_stack.pop()
            goto_state = self.goto(self.state_stack[-1], "E")
            self.state_stack.append(goto_state)
        elif production == 7:
            # C -> S
            self.state_stack.pop()  # Remove S
            goto_state = self.goto(self.state_stack[-1], "C")
            self.state_stack.append(goto_state)
        else:
            self.error(f"Produção desconhecida: {production}")
            return False

        return True
    
    def goto(self, current_state, non_terminal):
        action = self.parsing_table.get(current_state, {}).get(non_terminal, None)
        print(f"action: {action} for state {current_state} and non-terminal '{non_terminal}'")
        if action and action.isdigit():
            return int(action)
        else:
            self.error(f"GOTO não encontrado para estado {current_state} e não-terminal '{non_terminal}'")
            return None

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

