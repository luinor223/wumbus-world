import pygame

aura_map = {
    'W': 'S',
    'P': 'B',
    'P_G': 'W_H',
    'H_P': 'G_L'
}


def draw_text(text, font_name, size, coordinate, color=(255, 255, 255)) -> tuple:
    display_font = pygame.font.SysFont(font_name, size)
    display_text = display_font.render(text, True, color)
    display_text_rect = display_text.get_rect()
    display_text_rect.topleft = coordinate
    return display_text, display_text_rect


def check_local(input_map, x, y):
    neighbors = []
    if x > 0:
        neighbors.append((-1, 0))
    if x < len(input_map) - 1:
        neighbors.append((1, 0))
    if y > 0:
        neighbors.append((0, -1))
    if y < len(input_map[0]) - 1:
        neighbors.append((0, 1))

    effects = []

    for element in ('W', 'P', 'P_G', 'H_P'):
        for neighbor in neighbors:
            if element in input_map[x + neighbor[0]][y + neighbor[1]].split(','):
                effects.append(aura_map[element])

    return effects


def draw_cell(input_map, scr, x, y):
    grd = pygame.transform.scale(pygame.image.load("assets/ground.png").convert_alpha(), (50, 50))
    scr.blit(grd, (60 + 50 * y, 60 + 50 * x))
    if input_map[x][y] != '-':
        get_elements = list(set(input_map[x][y].split(',')))
        get_elements.sort(reverse=True)
        for element in get_elements:
            img = pygame.transform.scale(pygame.image.load("assets/" + element + ".png").convert_alpha(), (50, 50))
            scr.blit(img, (60 + 50 * y, 60 + 50 * x))


def draw_effect(input_map, scr, x, y):
    effects = check_local(input_map, x, y)
    for element in effects:
        img = pygame.transform.scale(pygame.image.load("assets/" + element + ".png").convert_alpha(),
                                     (50, 50))
        scr.blit(img, (60 + 50 * y, 60 + 50 * x))


def draw_information(scr, agent):
    # Draw the facing direction
    if agent.facing == 0:
        triangle = [
            (70 + 50 * agent.pos[1], 65 + 50 * agent.pos[0]),
            (100 + 50 * agent.pos[1], 65 + 50 * agent.pos[0]),
            (85 + 50 * agent.pos[1], 50 + 50 * agent.pos[0]),
        ]
    elif agent.facing == 3:
        triangle = [
            (65 + 50 * agent.pos[1], 70 + 50 * agent.pos[0]),
            (65 + 50 * agent.pos[1], 100 + 50 * agent.pos[0]),
            (50 + 50 * agent.pos[1], 85 + 50 * agent.pos[0]),
        ]
    elif agent.facing == 2:
        triangle = [
            (70 + 50 * agent.pos[1], 105 + 50 * agent.pos[0]),
            (100 + 50 * agent.pos[1], 105 + 50 * agent.pos[0]),
            (85 + 50 * agent.pos[1], 120 + 50 * agent.pos[0]),
        ]
    elif agent.facing == 1:
        triangle = [
            (105 + 50 * agent.pos[1], 70 + 50 * agent.pos[0]),
            (105 + 50 * agent.pos[1], 100 + 50 * agent.pos[0]),
            (120 + 50 * agent.pos[1], 85 + 50 * agent.pos[0]),
        ]
    else:
        triangle = []
    pygame.draw.polygon(scr, (255, 128, 0), triangle)

    pygame.draw.rect(scr, (255, 255, 255), (580, 60, 160, 500), width=2)
    text1, text1_rect = draw_text("Position:", "comicsansms", 20, (590, 70))
    scr.blit(text1, text1_rect)
    text2, text2_rect = draw_text(f"{agent.pos}", "comicsansms", 20, (590, 95))
    scr.blit(text2, text2_rect)
    text3, text3_rect = draw_text(f"HP: {agent.HP}", "comicsansms", 20, (590, 125))
    scr.blit(text3, text3_rect)
    text4, text4_rect = draw_text(f"Gold: {agent.gold}G", "comicsansms", 20, (590, 150))
    scr.blit(text4, text4_rect)
    text5, text5_rect = draw_text(f"Points: {agent.points}", "comicsansms", 20, (590, 180))
    scr.blit(text5, text5_rect)


def display_map(input_map, scr, fog_state, agent):
    for i in range(10):
        for ii in range(10):
            if fog_state[i][ii]:
                pygame.draw.rect(scr, (100, 100, 100), (60 + 50 * ii, 60 + 50 * i, 50, 50))
            else:
                draw_cell(input_map, scr, i, ii)
            pygame.draw.rect(scr, (255, 255, 255), (60 + 50 * ii, 60 + 50 * i, 50, 50), width=1)

    pygame.draw.rect(scr, (255, 128, 0), (70 + 50 * agent.pos[1], 70 + 50 * agent.pos[0], 30, 30))
    draw_information(scr, agent)

    for i in range(10):
        for ii in range(10):
            if not fog_state[i][ii]:
                draw_effect(input_map, scr, i, ii)


def convert_pos(pos_):
    return tuple((9 - pos_[0] + 1, pos_[1] + 1))


direction_map = {
    0: (-1, 0),
    1: (0, 1),
    2: (1, 0),
    3: (0, -1)
}


class PseudoAgent:

    def __init__(self, move_sequence, filename):
        self.pos = (9, 0)
        self.HP = 4
        self.points = 0
        self.facing = 0
        self.move_sequence = move_sequence
        self.agent_map = []
        self.original_map = []
        self.step_index = 0
        self.pots = 0
        self.gold = 0

        with open(filename) as f:
            self.size = int(f.readline())
            for line in f:
                line = line.strip()
                self.agent_map.append(line.split('.'))
                self.original_map.append(line.split('.'))

    def go_forward(self):
        new_pos = (
            self.pos[0] + direction_map[self.facing][0],
            self.pos[1] + direction_map[self.facing][1],
        )

        print(f"Agent moved from {convert_pos(self.pos)} to {convert_pos(new_pos)}")
        self.pos = new_pos
        self.points -= 10

    def remove_map_object(self, element):
        get_elements = self.agent_map[self.pos[0]][self.pos[1]].split(',')
        get_elements.remove(element)
        if not get_elements:
            self.agent_map[self.pos[0]][self.pos[1]] = '-'
        else:
            self.agent_map[self.pos[0]][self.pos[1]] = ','.join(get_elements)

    def remove_wumbus(self):
        new_pos = (
            self.pos[0] + direction_map[self.facing][0],
            self.pos[1] + direction_map[self.facing][1],
        )
        get_elements = self.agent_map[new_pos[0]][new_pos[1]].split(',')
        get_elements.remove('W')
        if not get_elements:
            self.agent_map[new_pos[0]][new_pos[1]] = '-'
        else:
            self.agent_map[new_pos[0]][new_pos[1]] = ','.join(get_elements)


    def next_step(self):
        if self.step_index == len(self.move_sequence):
            return False
        movement = self.move_sequence[self.step_index][1]
        if movement == 'go forward':
            self.go_forward()
        elif movement == 'climb out':
            print("Agent has climbed out of the cave.")
            self.points += 10

        elif movement == 'grab gold':
            print("Agent has grabbed gold.")
            self.points += 5000
            self.remove_map_object('G')
            self.gold += 1

        elif movement == 'grab healing potion':
            print("Agent has grabbed the healing potion.")
            self.pots += 1
            self.points -= 10
            self.remove_map_object('H_P')

        elif movement == 'use healing potion':
            print("Agent has used its potion to heal.")
            self.HP += 1
            self.pots -= 1
            self.points -= 10

        elif movement == 'turn right':
            self.facing += 1
            self.facing %= 4
            print("Agent has turned right.")
            self.points -= 10

        elif movement == 'turn left':
            self.facing -= 1
            self.facing %= 4
            print("Agent has turned left.")
            self.points -= 10

        elif movement == 'heard scream':
            print("rawr.")
            self.remove_wumbus()

        elif movement == 'poisoned':
            print("The agent has been poisoned")
            self.HP -= 1
            self.points -= 10

        elif movement == 'die':
            print("The agent is dead lmao")

        self.step_index += 1
        return True

    def display(self, scr):
        fog = [[False for _ in range(10)] for __ in range(10)]
        display_map(self.agent_map, scr, fog, self)







