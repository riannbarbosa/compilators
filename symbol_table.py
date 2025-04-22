class SymbolTable:
    def __init__(self):
        self.table = []
        self.indexId = 0

    def add_symbol(self, attributes):
        attributes['id'] = self.indexId
        self.table.append(attributes)
        self.indexId += 1

    def get_symbol(self, identifier):
        for symbol in self.table:
            if symbol.get('identifier') == identifier:
                return symbol
        return None

    def update_symbol(self, identifier, attributes):
        for symbol in self.table:
            if symbol.get('identifier') == identifier:
                symbol.update(attributes)
                return
        print(f"Symbol with identifier '{identifier}' not found.")