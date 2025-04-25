from afnd import AFND
from afd import AFD
from lexical_analyzer import LexicalAnalyzer
afnd = AFND("input.in")
afd = AFD("input.in")

afnd.printAttributes()
afd.printWithErrorState()

lexical_analyzer = LexicalAnalyzer(afd)
symbol_table = lexical_analyzer.analyze("input.in")
lexical_analyzer.print_symbol_table(symbol_table)