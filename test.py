from kb import KB

kb = KB(4)

kb.add_clause([-KB.symbol('B', 0, 0)])
kb.add_clause([-KB.symbol('B', 1, 0)])
kb.add_clause([KB.symbol('B', 0, 1)])

#kb.remove_clause([-KB.symbol('B', 1, 0)])

for i in range(0, 4):
    for j in range(0, 4):
        if kb.query('P', i, j) == 'exists':
            print(f'There is a Pit at ({i}, {j})')
        elif kb.query('P', i, j) == 'not exists':
            print(f'There is no Pit at ({i}, {j})')
        elif kb.query('P', i, j) == 'unknown':
            print(f'There may or may not be a pit at ({i}, {j})')
        else:
            print(f'The knowledge base is inconsistent for ({i}, {j})')