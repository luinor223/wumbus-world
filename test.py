from kb import KB
from program import Program


kb = KB(10)

kb.add_clause([KB.symbol('G_L', 1, 1)])
kb.remove_clause([KB.symbol('G_L', 1, 1)])
wumpus_check = kb.query('W', 2, 1)
pit_check = kb.query('P', 2, 1)
poison_check = kb.query('P_G', 2, 1)

print(wumpus_check)