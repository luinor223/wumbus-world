class Program:
    element_percept = {
            'W': 'S',
            'P': 'B',
            'P_G': 'W_H',
            'H_P': 'G_L'
        }
    def __init__(self):
        self.size = 0
        self.map = []
        
    def create_world(self, filename: str):
        with open(filename) as f:
            self.size = int(f.readline())
            self.map.append(['X'] * (self.size + 2))
            for line in f:
                line = line.strip()
                self.map.append(['X'] + line.split('.') + ['X'])
            self.map.append(['X'] * (self.size + 2)) 
        self.map = self.map[::-1]        
        self.apply_percepts_to_map()
        
    def apply_percept_to_pos(self, i, j, percept: str):
        if self.map[i][j] == 'X':
            return
        cell_contents = self.cell(i, j)
        if cell_contents == ['-']:
            cell_contents = []
        cell_contents.append(percept)
        self.map[i][j] = ','.join(cell_contents)
    
    def apply_percepts_to_map(self):
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                cell_contents = self.cell(i, j)
                for entity in cell_contents:
                    if entity in Program.element_percept:
                        perception = Program.element_percept[entity]
                        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            self.apply_percept_to_pos(i + di, j + dj, perception)
    
    def cell(self, i, j):
        return self.map[i][j].split(',')
    
    def remove_object(self, object, i, j):
        cell_contents = self.cell(i, j)
        cell_contents.remove(object)
        if cell_contents == []:
            cell_contents = ['-']
        self.map[i][j] = ','.join(cell_contents)
        
    def print_world(self):
        for line in self.map[::-1]:
            print(line)

