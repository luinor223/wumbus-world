import pygame

aura_map = {
    'W': 'S',
    'P': 'B',
    'P_G': 'W_H',
    'H_P': 'G_L'
}


def draw_text(text, font_name, size, coordinate, color=(0, 0, 0)) -> tuple:
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

    effects = set()

    for element in ('W', 'P', 'P_G', 'H_P'):
        for neighbor in neighbors:
            if element in input_map[x + neighbor[0]][y + neighbor[1]].split(','):
                effects.add(aura_map[element])

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


def draw_information(scr, agent, cur_state, fog_state):
    info_tab = pygame.transform.scale(pygame.image.load(f"assets/info.png").convert_alpha(), (180, 540))
    scr.blit(info_tab, (590, 40))

    text1, text1_rect = draw_text("Position:", "comicsansms", 20, (610, 70))
    scr.blit(text1, text1_rect)
    text2, text2_rect = draw_text(f"{convert_pos(agent.pos)}", "comicsansms", 20, (610, 95))
    scr.blit(text2, text2_rect)
    text5, text5_rect = draw_text(f"Points: {agent.points}", "comicsansms", 20, (610, 125))
    scr.blit(text5, text5_rect)

    hp_state = pygame.transform.scale(pygame.image.load("assets/HP_" + str(agent.HP) + ".png").convert_alpha(), (40, 40))
    scr.blit(hp_state, (610, 150))
    text3, text3_rect = draw_text(f"{agent.HP * 25}%", "comicsansms", 20, (660, 155))
    scr.blit(text3, text3_rect)

    num_gold = pygame.transform.scale(pygame.image.load("assets/gold_icon.png").convert_alpha(),(40, 40))
    scr.blit(num_gold, (610, 200))
    text4, text4_rect = draw_text(f" x{agent.gold}", "comicsansms", 20, (660, 205))
    scr.blit(text4, text4_rect)

    num_pots = pygame.transform.scale(pygame.image.load("assets/H_P.png").convert_alpha(),(40, 40))
    scr.blit(num_pots, (610, 250))
    text6, text6_rect = draw_text(f" x{agent.pots}", "comicsansms", 20, (660, 255))
    scr.blit(text6, text6_rect)

    for e_index, element in enumerate(('W', 'P', 'P_G', 'H_P')):
        img = pygame.transform.scale(pygame.image.load("assets/" + element + ".png").convert_alpha(), (40, 40))
        scr.blit(img, (620 + 60 * (e_index // 2), 300 + 50 * (e_index % 2)))
        if aura_map[element] in cur_state:
            warn = pygame.transform.scale(pygame.image.load("assets/exclam.png").convert_alpha(), (40, 40))
            scr.blit(warn, (620 + 60 * (e_index // 2), 300 + 50 * (e_index % 2)))

    if agent.scream:
        scream = pygame.transform.scale(pygame.image.load("assets/scream.png").convert_alpha(), (50, 50))
        scr.blit(scream, (630, 400))

    if agent.shoot:
        new_pos = (
            agent.pos[0] + direction_map[agent.facing][0],
            agent.pos[1] + direction_map[agent.facing][1],
        )
        shoot_cursor = pygame.transform.scale(pygame.image.load("assets/shoot.png").convert_alpha(), (50, 50))
        scr.blit(shoot_cursor, (60 + 50 * new_pos[1], 60 + 50 * new_pos[0]))

    fog_states = (
        'Agent',
        'Traced',
        'All'
    )

    text10, text10_rect = draw_text("[TAB]: Change fog", "comicsansms", 15, (610, 460))
    scr.blit(text10, text10_rect)
    text8, text8_rect = draw_text("[SPACE]: Auto play", "comicsansms", 15, (610, 480))
    scr.blit(text8, text8_rect)
    text9, text9_rect = draw_text(f"[->]: Next move", "comicsansms", 15, (610, 500))
    scr.blit(text9, text9_rect)

    text7, text7_rect = draw_text(f"Fog mode: {fog_states[fog_state]}", "comicsansms", 15, (610, 520))
    scr.blit(text7, text7_rect)

    for i in range(10):
        x_label, x_label_rect = draw_text(f"{9 - i + 1}", "comicsansms", 20, (0, 0), (255, 255, 255))
        x_label_rect.center = (20, 80 + 50 * i)
        y_label, y_label_rect = draw_text(f"{i + 1}", "comicsansms", 20, (0, 0), (255, 255, 255))
        y_label_rect.center = (80 + 50 * i, 20)
        scr.blit(x_label, x_label_rect)
        scr.blit(y_label, y_label_rect)


def display_map(input_map, scr, agent, fog, fog_overlay):
    bg_img = pygame.transform.scale(pygame.image.load(f"assets/bg2.png").convert_alpha(), (800, 600))
    scr.blit(bg_img, (0, 0))
    bg_tab = pygame.transform.scale(pygame.image.load(f"assets/bg1.png").convert_alpha(), (540, 540))
    scr.blit(bg_tab, (40, 40))

    for i in range(10):
        for ii in range(10):
            draw_cell(input_map, scr, i, ii)

    if agent.HP > 0:
        agent_sprite = pygame.transform.scale(pygame.image.load(f"assets/A_{agent.facing}.png").convert_alpha(), (50, 50))
    else:
        agent_sprite = pygame.transform.scale(pygame.image.load(f"assets/dead.png").convert_alpha(), (50, 50))
    scr.blit(agent_sprite, (60 + 50 * agent.pos[1], 60 + 50 * agent.pos[0]))

    draw_information(scr, agent, check_local(input_map, agent.pos[0], agent.pos[1]), fog)

    for i in range(10):
        for ii in range(10):
            draw_effect(input_map, scr, i, ii)

    if fog != 2:
        for i in range(10):
            for ii in range(10):
                if agent.pos == (i, ii):
                    continue
                if fog_overlay[i][ii]:
                    foggy = pygame.transform.scale(pygame.image.load(f"assets/fog.png").convert_alpha(), (60, 60))
                    scr.blit(foggy, (55 + 50 * ii, 55 + 50 * i))
                elif fog == 0:
                    foggy = pygame.transform.scale(pygame.image.load(f"assets/fog_less.png").convert_alpha(), (60, 60))
                    scr.blit(foggy, (55 + 50 * ii, 55 + 50 * i))


def convert_pos(pos_):
    return tuple((9 - pos_[0] + 1, pos_[1] + 1))


direction_map = {
    0: (-1, 0),
    1: (0, 1),
    2: (1, 0),
    3: (0, -1)
}


class PseudoAgent:
    valid_objects = ['W', 'P', 'P_G', 'H_P', 'G', 'S', 'B', 'W_H', 'G_L', '-']
    def __init__(self, move_sequence, filename):
        self.pos = (9, 0)
        self.HP = 4
        self.points = 0
        self.facing = 0
        self.move_sequence = move_sequence
        self.agent_map = []
        self.original_map = []
        self.fogged = [[False if (x, y) == (9, 0) else True for y in range(10)] for x in range(10)]
        self.step_index = 0
        self.pots = 0
        self.gold = 0
        self.scream = False
        self.shoot = False

        with open(filename) as f:
            self.size = int(f.readline())
            for line in f:
                line = line.strip()
                self.agent_map.append(line.split('.'))
                self.original_map.append(line.split('.'))

        self.preprocess()

    def preprocess(self):
        for i in range(len(self.agent_map)):
            for j in range(len(self.agent_map[i])):
                cell_contents = self.agent_map[i][j].split(',')
                validated_contents = [obj for obj in cell_contents if obj in self.valid_objects and obj != 'A']
                if not validated_contents:
                    validated_contents = ['-']
                self.agent_map[i][j] = ','.join(validated_contents)
                self.original_map[i][j] = ','.join(validated_contents)
            
    def reset_stats(self):
        self.pos = (9, 0)
        self.HP = 4
        self.points = 0
        self.facing = 0
        self.step_index = 0
        self.pots = 0
        self.gold = 0
        self.scream = False
        self.shoot = False
        self.fogged = [[False if (x, y) == (9, 0) else True for y in range(10)] for x in range(10)]

        self.agent_map = [row[:] for row in self.original_map]

    def go_forward(self):
        new_pos = (
            self.pos[0] + direction_map[self.facing][0],
            self.pos[1] + direction_map[self.facing][1],
        )

        print(f"Agent moved from {convert_pos(self.pos)} to {convert_pos(new_pos)}")
        self.pos = new_pos
        self.points -= 10
        self.fogged[new_pos[0]][new_pos[1]] = False

    def remove_map_object(self, element):
        get_elements = self.agent_map[self.pos[0]][self.pos[1]].split(',')
        get_elements.remove(element)
        if not get_elements:
            self.agent_map[self.pos[0]][self.pos[1]] = '-'
        else:
            self.agent_map[self.pos[0]][self.pos[1]] = ','.join(get_elements)

    def remove_wumbus(self):
        self.scream = True
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
        if self.scream:
            self.scream = False
        if self.shoot:
            self.shoot = False

        if self.step_index == len(self.move_sequence):
            self.reset_stats()
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

        elif movement == 'shoot':
            self.shoot = True
            self.points -= 100
            print('pang!')

        elif movement == 'poisoned':
            print("The agent has been poisoned")
            self.HP -= 1
            self.points -= 10

        elif movement == 'die':
            print("The agent is dead lmao")

        self.step_index += 1
        return True

    def display(self, scr, fog_mode):
        display_map(self.agent_map, scr, self, fog_mode, self.fogged)







