
from afd import afd
from lexical_analyzer import LexicalAnalyzer



lexical_analyzer = LexicalAnalyzer(afd)
symbol_table = lexical_analyzer.analyze("input.in")
lexical_analyzer.print_symbol_table()   
lexical_analyzer.print_errors()