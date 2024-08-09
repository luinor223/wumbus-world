class Program:
    def __init__(self):
        self.size = 0
        self.map = []
        
    def create_world(self, filename: str):
        with open(filename) as f:
            self.size = int(f.readline())
            self.map.append(['X'] * (self.size + 2))
            for line in f:
                self.map.append(['X'] + line.split('.')[:-1] + ['X'])
            self.map.append(['X'] * (self.size + 2))            
        self.apply_percepts_to_map()
    
    def apply_percept_to_pos(self, i, j, percept: str):
        if self.map[i][j] == 'X':
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
                if cell == 'X':
                    continue
                for trigger, perception in percepts.items():
                    if trigger in cell:
                        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            self.apply_percept_to_pos(i + di, j + dj, perception)
    
    def cell(self, i, j):
        return self.map[i][j].split(",")
    
    def remove_object(self, i, j, object: str):
        self.map[i][j] = self.map[i][j].replace(object, '')
        if self.map[i][j] == '':
            self.map[i][j] = '-'
        if ',,' in self.map[i][j]:
            self.map[i][j] = self.map[i][j].replace(',,', ',')
        if self.map[i][j][0] == ',' or self.map[i][j][-1] == ',':
            self.map[i][j] = self.map[i][j][1:-1]
        
    def print_world(self):
        for line in self.map:
            print(line)