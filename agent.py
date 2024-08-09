from program import Program
from kb import KB
class Agent:
    def __init__(self, program: Program, start_col: int, start_row: int):
        self.pos = (start_col, start_row)
        self.direction = 'UP'
        self.HP = 100
        self.points = 0
        self.program = program
        self.kb = KB(self.program.size)
        
    def perceive(self):
        percepts = ['S', 'B', 'W_H', 'G_L']
        for percept in percepts:
            if percept in self.program.cell(self.pos[0], self.pos[1]):
                self.kb.add_clause([KB.symbol(percept, self.pos[0], self.pos[1])])
            else:
                self.kb.add_clause([-KB.symbol(percept, self.pos[0], self.pos[1])])
        adj = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            