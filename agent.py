from program import Program
from kb import KB

class Agent:
    def __init__(self, program: Program, start_row: int, start_col: int):
        self.pos = (start_row, start_col)
        self.caveExit = (start_row, start_col)
        self.healingPotion = 0
        self.direction = 'UP'   
        self.HP = 100
        self.points = 0
        self.program = program
        self.kb = KB(self.program.size)

        self.visited = set()  # Set of visited positions
        self.safe_tiles = set()  # Set of known safe tiles
        self.finalPath = [self.pos]
    
    def perceive(self):
        percepts = ['S', 'B', 'W_H', 'G_L', 'P_G', 'H_P']
        for percept in percepts:
            if percept in self.program.cell(self.pos[0], self.pos[1]):
                self.kb.add_clause([KB.symbol(percept, self.pos[0], self.pos[1])])
            else:
                self.kb.add_clause([-KB.symbol(percept, self.pos[0], self.pos[1])])
        self.kb.add_clause([-KB.symbol('W', self.pos[0], self.pos[1])])
        self.kb.add_clause([-KB.symbol('P', self.pos[0], self.pos[1])])
    #     adj = []
    #     for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        
    def setPos(self, x, y):
        self.pos = (x, y)

    def printAgentMap(self):
        for line in self.agentMap:
            print(line)

    def is_safe(self, x, y):
        return self.kb.query('W', x, y) == 'not exists' and self.kb.query('P', x, y) == 'not exists'
    
    def get_neighbors(self, position):
        x, y = position
        # Possible moves: up, down, left, right
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        return [pos for pos in neighbors if self.is_in_bounds(pos)]
    
    def is_in_bounds(self, position):
        return 0 < position[0] < self.program.size + 1 and 0 < position[1] < self.program.size + 1
    
    def bfs_to_goal(self, goal):
        queue = [(self.pos, [])] #the final result not include initial cell
        bfs_visited = set([self.pos])

        while len(queue) != 0:
            current_position, path = queue.pop(0)
            if current_position == goal:
                return path  # Return the path to the goal
            for neighbor in self.get_neighbors(current_position):
                if neighbor not in bfs_visited and neighbor in self.visited:
                    bfs_visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
    def decide_next_move(self):
        self.visited.add(self.pos)
        # print('currently at: ', self.pos)

        self.perceive()
        self.kb.initialize_kb_relations()

        if ('P_G' in self.program.cell(self.pos[0], self.pos[1])):
            if (self.HP == 25 and self.healingPotion > 0):
                self.healingPotion -= 1
            else:
                self.HP -= 25
            if (self.HP == 0):
                print('Agent is gone!\n')
                return False
        elif (any(['W', 'P']) in self.program.cell(self.pos[0], self.pos[1])):
            print('Agent is gone!\n')
            return False
        elif ('G' in self.program.cell(self.pos[0], self.pos[1])):
            self.finalPath += self.bfs_to_goal(self.caveExit)
            print('Gold found, return to cave exit')
            return False
        elif ('H_P' in self.program.cell(self.pos[0], self.pos[1])):
            print('Healing potion found!')
            self.healingPotion += 1
        
        # Update safe tiles based on current knowledge
        neighbors = self.get_neighbors(self.pos)
        for nx, ny in neighbors:
            if (nx, ny) not in self.visited and self.is_safe(nx, ny):
                self.safe_tiles.add((nx, ny))

        # Find the nearest safe unvisited tile
        safe_unvisited_tiles = [tile for tile in self.safe_tiles if tile not in self.visited]
        # print('safe unvisited tiles: ', safe_unvisited_tiles)
        if safe_unvisited_tiles:
            next_tile = min(safe_unvisited_tiles, key=lambda pos: abs(pos[0] - self.pos[0]) + abs(pos[1] - self.pos[1])) #go to nearest cell based on manhattan distance, may use BFS to go to lowest cost cell
            self.visited.add(next_tile)
            self.finalPath += self.bfs_to_goal(next_tile)
            self.pos = next_tile
            return True
        else:  # no safe cell found, implement some shoting Wumpus strategy here
            self.finalPath += self.bfs_to_goal(self.caveExit)
            print('no possible path, climb up the cave')
            self.pos = self.caveExit
            return False
            