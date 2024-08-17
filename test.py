from kb import KB
from program import Program


kb = KB(4)

kb.add_clause([KB.symbol('S', 2, 1)])
kb.add_clause([-KB.symbol('S', 1, 2)])
kb.add_clause([KB.symbol('S', 2, 1)])
kb.remove_clause([KB.symbol('S', 2, 1)])
kb.remove_clause([KB.symbol('S', 2, 1)])
print(kb.query('W', 3, 1))