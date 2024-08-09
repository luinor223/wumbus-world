from pysat.formula import CNF
from pysat.solvers import Solver

class KB:
    def __init__(self, map_size):
        self.KB = CNF()
        self.size = map_size
        self.initialize_kb_relations()
        
    @staticmethod
    def symbol(entity, x, y):
        entity_map = {
            'W': 1,
            'P': 2,
            'P_G': 3,
            'H_P': 4,
            'B': 5,
            'S': 6,
            'W_H': 7,
            'G_L': 8,
            'G': 9
        }
        return entity_map[entity] * 100 + x * 10 + y
        
    def initialize_kb_relations(self):
        # No Wumpus, Pit, Poisonous Gas, or Healing Potion at the beginning
        self.KB.append([-KB.symbol('W', 1, 1)])
        self.KB.append([-KB.symbol('P', 1, 1)])
        self.KB.append([-KB.symbol('P_G', 1, 1)])
        self.KB.append([-KB.symbol('H_P', 1, 1)])
        
        # Pit-Breeze, Wumpus-Stench, Poisonous Gas-Whiff, Healing Potion-Glow rules for each cell
        percepts = {
            'W': 'S',
            'P': 'B',
            'P_G': 'W_H',
            'H_P': 'G_L'
        }
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                for trigger, percept in percepts.items():
                    percept_symbol = KB.symbol(percept, i, j)
                    adjacent_trigger = []
                    
                    if i > 1:  # Up
                        adjacent_trigger.append(KB.symbol(trigger, i-1, j))
                    if i < self.size:  # Down
                        adjacent_trigger.append(KB.symbol(trigger, i+1, j))
                    if j < self.size:  # Right
                        adjacent_trigger.append(KB.symbol(trigger, i, j+1))
                    if j > 1:  # Left
                        adjacent_trigger.append(KB.symbol(trigger, i, j-1))

                    # Px,y => (Tx+1,y v Tx-1,y v Tx,y+1 v Tx,y-1)
                    self.KB.append([-percept_symbol] + adjacent_trigger)
                    
                    # (Tx,y+1 v Tx,y-1 v Tx+1,y v Tx-1,y) => Px,y
                    for trigger_symbol in adjacent_trigger:
                        self.KB.append([percept_symbol, -trigger_symbol])
                        
    def add_clause(self, clause):
        self.KB.append(clause)
    
    def query(self, entity, x, y):
        with Solver(bootstrap_with=self.KB) as solver:
            entity_symbol = self.symbol(entity, x, y)
            
            solver.solve(assumptions=[entity_symbol])
            entity_possible = solver.get_model() is not None
            
            solver.solve(assumptions=[-entity_symbol])
            no_pit_possible = solver.get_model() is not None
            
            if entity_possible and not no_pit_possible:
                return 'exists'
            if not entity_possible and no_pit_possible:
                return 'not exists'
            if entity_possible and no_pit_possible:
                return 'unknown'
            
        return 'inconsistent'
    
    def remove_clause(self, clause):
        new_kb = CNF()
        for cl in self.KB:
            if cl != clause:
                new_kb.append(cl)
        self.KB = new_kb