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
    
    def init_breeze(self):
        for x in range(0, 4):
            for y in range(0, 4):
                self.add_breeze_pit_relation(self.KB, x, y)
    
    def add_breeze_pit_relation(self, cnf : CNF, x, y):
        breeze = self.symbol('B', x, y)
        adjacent_pits = []
        
        if y < self.size:  # Up
            adjacent_pits.append(self.symbol('P', x, y+1))
        if y > 0:  # Down
            adjacent_pits.append(self.symbol('P', x, y-1))
        if x < self.size:  # Right
            adjacent_pits.append(self.symbol('P', x+1, y))
        if x > 0:  # Left
            adjacent_pits.append(self.symbol('P', x-1, y))
        
        # Bx,y => (Px,y+1 v Px,y-1 v Px+1,y v Px-1,y)
        cnf.append([-breeze] + adjacent_pits)
        
        # (Px,y+1 v Px,y-1 v Px+1,y v Px-1,y) => Bx,y
        for pit in adjacent_pits:
            cnf.append([breeze, -pit])
        
    def initialize_kb_relations(self):
        # No Wumpus, Pit, Poisonous Gas, or Healing Potion at the beginning
        self.KB.append([-KB.symbol('W', 0, 0)])
        self.KB.append([-KB.symbol('P', 0, 0)])
        self.KB.append([-KB.symbol('P_G', 0, 0)])
        self.KB.append([-KB.symbol('H_P', 0, 0)])
        
        # Pit-Breeze, Wumpus-Stench, Poisonous Gas-Whiff, Healing Potion-Glow rules for each cell
        percepts = {
            'W': 'S',
            'P': 'B',
            'P_G': 'W_H',
            'H_P': 'G_L'
        }
        for i in range(0, self.size):
            for j in range(0, self.size):
                for trigger, percept in percepts.items():
                    percept_symbol = KB.symbol(percept, i, j)
                    adjacent_trigger = []
                    
                    if i > 0:  # Up
                        adjacent_trigger.append(KB.symbol(trigger, i-1, j))
                    if i < self.size - 1:  # Down
                        adjacent_trigger.append(KB.symbol(trigger, i+1, j))
                    if j < self.size - 1:  # Right
                        adjacent_trigger.append(KB.symbol(trigger, i, j+1))
                    if j > 0:  # Left
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