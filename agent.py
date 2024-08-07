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