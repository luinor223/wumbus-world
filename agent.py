from program import Program
class Agent:
    def __init__(self, program: Program, start_col: int, start_row: int):
        pos = (start_col, start_row)
        self.direction = 'UP'
        self.is_alive = True
        self.program = program
        self.kb = []