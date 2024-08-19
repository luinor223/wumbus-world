class Program:
    element_percept = {
        'W': 'S',
        'P': 'B',
        'P_G': 'W_H',
        'H_P': 'G_L'
    }
    
    valid_objects = ['W', 'P', 'P_G', 'H_P', 'G', 'S', 'B', 'W_H', 'G_L', '-', 'X']

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
        
        self.preprocess()
        self.apply_percepts_to_map()

    def preprocess(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if isinstance(self.map[i][j], str):
                    cell_contents = self.map[i][j].split(',')
                    validated_contents = [obj for obj in cell_contents if obj in self.valid_objects]
                    if not validated_contents:
                        validated_contents = ['-']
                    self.map[i][j] = ','.join(validated_contents)

    def apply_percept_to_pos(self, i, j, percept):
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
    
    @staticmethod
    def generate_output_filename(input_file):
        # Split the input path into directories and filename
        parts = input_file.split('/')
        
        # Get the last part (the filename)
        filename = parts[-1]
        
        # Split the filename and extension
        name_parts = filename.split('.')
        
        # Create the new filename
        new_filename = 'result_' + name_parts[0] + '.txt'
        
        # Construct the full output path
        output_file = 'results/' + new_filename
        
        return output_file