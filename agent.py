from program import Program
from kb import KB

class Agent:
    direction_map = {
        'NORTH': (1, 0),
        'EAST': (0, 1),
        'SOUTH': (-1, 0),
        'WEST': (0, -1)
    }
    def __init__(self, program: Program, start_row: int, start_col: int):
        self.pos = (start_row, start_col)
        self.caveExit = (start_row, start_col)
        self.healingPotion = 0
        self.direction = 'NORTH'   
        self.HP = 100
        self.points = 0
        self.program = program
        self.kb = KB(self.program.size)

        self.visited = set()  # Set of visited positions
        self.visited.add(self.pos)
        self.safe_cells = set()  # Set of known safe tiles
        self.safe_cells.add(self.pos)
        self.finalPath = [self.pos]
        self.action_log = []
        
    def get_direction_prio(self):
        if self.direction == 'NORTH':
            return ['NORTH', 'EAST', 'WEST', 'SOUTH']
        if self.direction == 'SOUTH':
            return ['SOUTH', 'WEST', 'EAST', 'NORTH']
        if self.direction == 'WEST':
            return ['WEST', 'NORTH', 'SOUTH', 'EAST']
        if self.direction == 'EAST':
            return ['EAST', 'SOUTH', 'NORTH', 'WEST']

    def infer(self, x, y):
        if (x, y) in self.safe_cells:
            return 'safe'
        wumpus_check = self.kb.query('W', x, y)
        pit_check = self.kb.query('P', x, y)
        poison_check = self.kb.query('P_G', x, y)
        
        # Wumpus, Pit
        if wumpus_check == 'not exists' and pit_check == 'not exists' and poison_check == 'not exists':
            return 'safe'
        if wumpus_check == 'exists' or pit_check == 'exists':
            return 'unsafe'

        if wumpus_check == 'unknown' or pit_check == 'unknown':
            return 'unsafe'

        # Poison. We don't check if there is a poison here to handle the blind case
        if self.HP + self.healingPotion * 25 >= 50:
            return 'somewhat safe'

        return 'unsafe'
    
    def get_neighbors(self, position):
        x, y = position
        neighbors = []
        directions = self.get_direction_prio()
        for direction in directions:
            d_x, d_y = Agent.direction_map[direction]
            row = x + d_x
            col = y + d_y
            if 'X' not in self.program.cell(row, col): # X = Wall
                neighbors.append((row, col))
        return neighbors
    
    def get_safe_neighbors(self, position):
        neighbors = self.get_neighbors(position)
        safe_neighbors = []
        
        for neighbor in neighbors:
            if self.infer(neighbor[0], neighbor[1]) == 'safe':
                safe_neighbors.append(neighbor)
                self.safe_cells.add(neighbor)
        
        # Leave the 'somewhat safe' (poison) neighbor to last
        for neighbor in neighbors:
            if self.infer(neighbor[0], neighbor[1]) == 'somewhat safe':
                safe_neighbors.append(neighbor)
                self.safe_cells.add(neighbor)
        
        # Hanlde the unknown poison case
        if 'W_H' in self.program.cell(position[0], position[1]):
            for neighbor in neighbors:
                if self.infer(neighbor[0], neighbor[1]) == 'unsafe':
                    continue
                if self.HP + self.healingPotion * 25 >= 50:
                    safe_neighbors.append(neighbor)
                    self.safe_cells.add(neighbor)
                
        return safe_neighbors
    
    def perceive(self):
        cell_content = self.program.cell(self.pos[0], self.pos[1])
        for object in cell_content:
            if object == '-':
                continue
            self.kb.add_clause([KB.symbol(object, self.pos[0], self.pos[1])])
        
        percepts = ['S', 'B', 'W_H', 'G_L']
        for percept in percepts:
            if percept not in cell_content:
                self.kb.add_clause([-KB.symbol(percept, self.pos[0], self.pos[1])])
    
    def use_healing_potion(self):
        if self.healingPotion > 0 and self.HP < 100:
            self.action_log.append((self.pos, "use healing potion"))
            self.HP = min(100, self.HP + 25)
            self.healingPotion -= 1
            self.points -= 10
    
    def grab_gold(self):
        self.points -= 10 # Grab
        self.action_log.append((self.pos, "grab gold"))
        self.points += 1000
        self.program.remove_object('G', self.pos[0], self.pos[1])

    def climb_out(self):
        if self.pos == self.caveExit:
            self.action_log.append((self.pos, "climb out"))
            self.points += 10  # Bonus for successfully exiting
    
    def hanlde_poison(self):
        self.kb.add_clause([KB.symbol('P_G', self.pos[0], self.pos[1])])
        self.HP -= 25
        self.safe_cells.remove(self.pos)
        if self.HP > 0:
            self.action_log.append((self.pos, "poisoned"))
            return True
        if self.HP <= 0 and self.healingPotion > 0:
            self.use_healing_potion()
            self.action_log.append((self.pos, "poisoned"))
            return True
        return False
    
    def handle_cell_contents(self):
        cell_contents = self.program.cell(self.pos[0], self.pos[1])
        
        if 'G' in cell_contents:
            self.grab_gold()
        
        if 'W' in cell_contents:
            self.HP = 0
            self.points -= 10000
        
        if 'P' in cell_contents:
            self.HP = 0
            self.points -= 10000
        
        if 'P_G' in cell_contents:
            self.hanlde_poison()
        
        if 'H_P' in cell_contents:
            self.points -= 10 # Grab
            self.healingPotion += 1
            self.program.remove_object('H_P', self.pos[0], self.pos[1])
        
        if self.HP <= 0:
            self.points -= 10000  # Large penalty for dying
            self.action_log.append((self.pos, "die"))
    
    def move(self, new_pos):
        new_direction = self.get_direction_to(new_pos)

        if self.direction != new_direction:
            self.turn(new_direction)
        
        # Move forward
        self.action_log.append((self.pos, 'go forward'))
        self.pos = new_pos
        self.finalPath.append(self.pos)
        self.visited.add(self.pos)
        self.points -= 10  # Deduct points for moving

        self.perceive()
        
        # Handle special cell contents
        self.handle_cell_contents()

    def get_direction_to(self, new_pos):
        dx, dy = new_pos[0] - self.pos[0], new_pos[1] - self.pos[1]
        for direction, (dx_dir, dy_dir) in self.direction_map.items():
            if (dx, dy) == (dx_dir, dy_dir):
                return direction
        return self.direction  # Default to current direction if no match

    def turn(self, new_direction):
        current_index = self.get_direction_prio().index(self.direction)
        new_index = self.get_direction_prio().index(new_direction)
        diff = (new_index - current_index) % 4

        if diff == 0:
            turn_sequence = []  # No turn needed
        elif diff == 1:
            turn_sequence = ['right']
        elif diff == 2:
            turn_sequence = ["right", "right"]
        else:  # diff == 3
            turn_sequence = ["left"]

        for turn_action in turn_sequence:
            self.action_log.append((self.pos, f"turn {turn_action}"))
            self.points -= 10  # Deduct points for each turn
        self.direction = new_direction
    
    def shoot(self):
        self.action_log.append((self.pos, 'shoot'))
        self.points -= 100
        target_pos = (self.pos[0] + self.direction_map[self.direction][0], 
                    self.pos[1] + self.direction_map[self.direction][1])
        
        if 'W' in self.program.cell(target_pos[0], target_pos[1]):
            self.kill_wumpus(target_pos)
            return True
        return False
    
    def kill_wumpus(self, position):
        self.program.remove_object('W', position[0], position[1])
        neighbors = self.get_neighbors(position)
        for neighbor in neighbors:
            self.program.remove_object('S', neighbor[0], neighbor[1])
            self.kb.remove_clause([KB.symbol('S', neighbor[0], neighbor[1])])
            if 'S' not in self.program.cell(neighbor[0], neighbor[1]):
                self.kb.add_clause([-KB.symbol('S', neighbor[0], neighbor[1])])
        self.action_log.append((self.pos, 'heard scream'))
        
    def consider_shooting(self):
        for direction in self.get_direction_prio():
            target_pos = (self.pos[0] + self.direction_map[direction][0], 
                        self.pos[1] + self.direction_map[direction][1])
            if self.kb.query('W', target_pos[0], target_pos[1]) == 'exists':
                self.turn(direction)
                if self.shoot():
                    return True
        return False
    
    def explore(self):
        self.perceive()
        while self.HP > 0:
            #print(f"Exploring cave at {self.pos}")
            safe_neighbors = self.get_safe_neighbors(self.pos)
            unvisited_safe_neighbors = [pos for pos in safe_neighbors if pos not in self.visited]
            
            if unvisited_safe_neighbors:
                next_pos = unvisited_safe_neighbors[0]
            else:
                # No safe moves, consider shooting or backtracking
                if self.consider_shooting():
                    continue
                next_pos = self.backtrack()
            
            if next_pos:
                self.move(next_pos)
            # No more moves possible, check if all safe cells have been explored
            elif self.all_safe_cells_explored():
                break # Exit the exploration loop
            else:
                break  # No more moves possible

        # Try to return to cave exit
        if self.HP > 0:
            self.return_to_exit()
    
    def all_safe_cells_explored(self):
        return self.safe_cells.issubset(self.visited)
    
    def find_path(self, start, goal):
        queue = [(start, [start])]
        visited = set([start])

        while queue:
            (vertex, path) = queue.pop(0)
            if vertex == goal:
                return path
            
            for next_pos in self.get_safe_neighbors(vertex):
                if next_pos not in visited:
                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))

        return None  # No path found
    
    def backtrack(self):
        # Find the nearest unexplored safe cell
        unexplored_safe_cells = self.safe_cells - self.visited
        if not unexplored_safe_cells:
            return None  # No unexplored safe cells left

        nearest_cell = min(unexplored_safe_cells, 
                        key=lambda cell: abs(cell[0] - self.pos[0]) + abs(cell[1] - self.pos[1]))

        # Find a path to the nearest unexplored safe cell
        path = self.find_path(self.pos, nearest_cell)
        
        if path:
            # Move to the next position in the path
            next_pos = path[1]  # path[0] is the current position
            return next_pos
        else:
            return None  # No path found
    
    def return_to_exit(self):
        path = self.find_path(self.pos, self.caveExit)
        
        if path:
            for next_pos in path[1:]:  # Skip the first position as it's the current position
                self.move(next_pos)
                if self.HP <= 0:
                    break  # Agent died while trying to return
            
            if self.pos == self.caveExit:
                self.climb_out()
        else:
            self.action_log.append((self.pos, "unable to find path to exit"))
            
    def output_action_log(self, output_file='result.txt'):
        with open(output_file, 'w') as f:
            for action in self.action_log:
                f.write(f"{action[0]} {action[1]}\n")