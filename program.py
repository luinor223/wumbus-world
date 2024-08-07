class Program:
    def __init__(self):
        self.size = 0
        self.map = []
        
    def create_world(self, filename: str):
        with open(filename) as f:
            self.size = int(f.readline())
            for line in f:
                self.map.append(line.split('.')[:-1])            
        self.apply_percepts_to_map()
    
    def is_in_bounds(self, pos: tuple):
        return 0 <= pos[0] < len(self.map) and 0 <= pos[1] < len(self.map[pos[0]])
    
    def apply_percept_to_pos(self, pos: tuple, percept: str):
        i, j = pos
        if not self.is_in_bounds((i, j)):
            return
        if percept in self.map[i][j]:
            return
        self.map[i][j] = self.map[i][j] + ',' + percept if self.map[i][j] != '-' else percept
    
    def apply_percepts_to_map(self):
        percepts = {
            'W': 'S',
            'P': 'B',
            'P_G': 'W_H',
            'H_P': 'G_L'
        }
        
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                for trigger, perception in percepts.items():
                    if trigger in cell:
                        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            self.apply_percept_to_pos(i + di, j + dj, perception)
    
    def cell(self, pos: tuple):
        return self.map[pos[0]][pos[1]].split(",")
    
    def remove_object(self, pos: tuple, object: str):
        self.map[pos[0]][pos[1]] = self.map[pos[0]][pos[1]].replace(object, '')
        if self.map[pos[0]][pos[1]] == '':
            self.map[pos[0]][pos[1]] = '-'
        if ',,' in self.map[pos[0]][pos[1]]:
            self.map[pos[0]][pos[1]] = self.map[pos[0]][pos[1]].replace(',,', ',')
        if self.map[pos[0]][pos[1]][0] == ',' or self.map[pos[0]][pos[1]][-1] == ',':
            self.map[pos[0]][pos[1]] = self.map[pos[0]][pos[1]][1:-1]
        
    def print_world(self):
        for line in self.map:
            print(line)
            
a = Program()
a.create_world('test.txt')
a.print_world()