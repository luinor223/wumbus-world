class Program:
    def __init__(self):
        self.map = []
        
    def create_world(self, filename: str):
        with open(filename) as f:
            for line in f:
                self.map.append(line.split('.')[:-1])            
        self.apply_signal_to_map()
    
    def is_in_bounds(self, pos: tuple):
        return 0 <= pos[0] < len(self.map) and 0 <= pos[1] < len(self.map[pos[0]])
    
    def apply_signal_to_pos(self, post: tuple, signal: str):
        i, j = post
        if not self.is_in_bounds((i, j)):
            return
        if signal in self.map[i][j]:
            return
        self.map[i][j] = self.map[i][j] + ',' + signal if self.map[i][j] != '-' else signal
    
    def apply_signal_to_map(self):
        signals = {
            'W': 'S',
            'P': 'B',
            'P_G': 'W_H',
            'H_P': 'G_L'
        }
        
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                for trigger, perception in signals.items():
                    if trigger in cell:
                        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            self.apply_signal_to_pos(i + di, j + dj, perception)
    
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