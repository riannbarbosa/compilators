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
                for index, action in enumerate(row[1:], 1):
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
            print(f"Parsing table: {self.parsing_table.get(estado_atual, {})}")
            action = self.parsing_table.get(estado_atual, {}).get(token, None)
            print(f"Current state: {estado_atual}, Token: {token}, Action: {action}")
            if action is None:
                self.error(f"Unexpected token '{token}' at line {token_data.get('line')}")
                return
            # FAZ SHIFT
            if action.startswith('s'):
                next_state = int(action[1:])
                consumed_token = self.input_stack.pop(0)
                self.symbol_stack.append(consumed_token)
                self.state_stack.append(next_state)
                print(f"Shifted to state {next_state}")
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
        # S' -> PROGRAMA
        if production == 1:
            # S' -> PROGRAMA
            self.state_stack.pop()  # Remove PROGRAMA
            goto_state = self.goto(self.state_stack[-1], "S'")
            self.state_stack.append(goto_state)
            self.symbol_stack.append("S'")
        # PROGRAMA -> STATEMENT PROGRAMA
        elif production == 2:
            for _ in range(2):  # Remove PROGRAMA, STATEMENT
                self.state_stack.pop()
                self.symbol_stack.pop()
            goto_state = self.goto(self.state_stack[-1], "PROGRAMA")
            if goto_state is None:
                return False
            self.state_stack.append(goto_state)
            self.symbol_stack.append("PROGRAMA")
        # PROGRAMA -> ε
        elif production == 3:
            # Não remove nada da pilha para produção vazia
            goto_state = self.goto(self.state_stack[-1], "PROGRAMA")
            if goto_state is None:
                return False
            self.state_stack.append(goto_state)
            self.symbol_stack.append("PROGRAMA")
        # STATEMENT -> LETSTATEMENT
        elif production == 4:
            for _ in range(4):
                self.state_stack.pop() # Remove states for let IDENT = IDENT
                self.symbol_stack.pop() # Remove symbols for let IDENT = IDENT
            goto_state = self.goto(self.state_stack[-1], "STATEMENT")
            if goto_state is None:
                return False
            self.state_stack.append(goto_state)
            self.symbol_stack.append("STATEMENT")
        # STATEMENT -> IFSTATEMENT
        elif production == 5:
            self.state_stack.pop()  # Remove IFSTATEMENT state
            self.symbol_stack.pop()  # Remove IFSTATEMENT symbol
            goto_state = self.goto(self.state_stack[-1], "STATEMENT")
            if goto_state is None:
                return False
            self.state_stack.append(goto_state)
            self.symbol_stack.append("STATEMENT")
        # LETSTATEMENT -> let IDENT = IDENT
        elif production == 6:
            self.state_stack.pop()
            self.symbol_stack.pop()
            self.state_stack.pop()
            self.symbol_stack.pop()
            goto_state = self.goto(self.state_stack[-1], "LETSTATEMENT")
            if goto_state is None:
                return False
            self.state_stack.append(goto_state)
            self.symbol_stack.append("LETSTATEMENT")
        # IFSTATEMENT -> if EXP_BOOL BLOCO_COND
        elif production == 7:
            for _ in range(3):  # Remove if, EXP_BOOL, BLOCO_COND
                self.state_stack.pop()
                self.symbol_stack.pop()
            goto_state = self.goto(self.state_stack[-1], "IFSTATEMENT")
            if goto_state is None:
                return False
            self.state_stack.append(goto_state)
            self.symbol_stack.append("IFSTATEMENT")
        # EXP_BOOL -> true
        elif production == 8:
            self.state_stack.pop()  # Remove true state
            self.symbol_stack.pop()  # Remove true symbol
            goto_state = self.goto(self.state_stack[-1], "EXP_BOOL")
            if goto_state is None:
                return False
            self.state_stack.append(goto_state)
            self.symbol_stack.append("EXP_BOOL")
        # EXP_BOOL -> false
        elif production == 9:
            self.state_stack.pop()  # Remove false state
            self.symbol_stack.pop()  # Remove false symbol
            goto_state = self.goto(self.state_stack[-1], "EXP_BOOL")
            if goto_state is None:
                return False
            self.state_stack.append(goto_state)
            self.symbol_stack.append("EXP_BOOL")
        # BLOCO_COND -> { PROGRAMA }
        elif production == 10:
            for _ in range(3):  # Remove {, PROGRAMA, }
                self.state_stack.pop()
                self.symbol_stack.pop()
            goto_state = self.goto(self.state_stack[-1], "BLOCO_COND")
            if goto_state is None:
                return False
            self.state_stack.append(goto_state)
            self.symbol_stack.append("BLOCO_COND")
        else:
            self.error(f"Produção desconhecida: {production}")
            return False

        print(f"After reduce - State stack: {self.state_stack}")
        print(f"Symbol stack after reduce: {[s.get('label', s) if isinstance(s, dict) else s for s in self.symbol_stack]}")
        return True
    
    def goto(self, current_state, non_terminal):
        action = self.parsing_table.get(current_state, {}).get(non_terminal, None)
        print(f"GOTO: state {current_state}, non-terminal '{non_terminal}' -> action: {action}")
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

