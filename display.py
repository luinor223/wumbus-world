import pygame

color_map = {
    'A': (255, 128, 0),  # Agent
    'W': (255, 0, 255),  # Wumbussy
    'G': (255, 255, 0),  # Gold
    'P': (69, 69, 69),  # Pit
    'P_G': (100, 255, 100),  # Poisonous Gas
    'H_P': (255, 0, 0)  # Healing Pot
}

pos_offset = {
    'W': (0, 0),  # Wumbussy
    'P': (0, 1),  # Pit
    'P_G': (1, 0),  # Poisonous Gas
    'H_P': (1, 1)  # Healing Pot
}


class AgentStats:
    def __init__(self):
        self.pos = (0, 0)
        self.is_alive = True
        self.facing = 's'
        self.HP = 100
        self.gold = 0
        self.points = 0

    def update_game_state(self, input_map, fog_state):
        if self.facing == 'w' and self.pos[0] > 0:
            new_pos = (self.pos[0] - 1, self.pos[1])
        elif self.facing == 's' and self.pos[0] < len(input_map) - 1:
            new_pos = (self.pos[0] + 1, self.pos[1])
        elif self.facing == 'a' and self.pos[1] > 0:
            new_pos = (self.pos[0], self.pos[1] - 1)
        elif self.facing == 'd' and self.pos[1] < len(input_map[0]) - 1:
            new_pos = (self.pos[0], self.pos[1] + 1)
        else:
            new_pos = self.pos

        fog_state[new_pos[0]][new_pos[1]] = False
        if input_map[new_pos[0]][new_pos[1]] in ('W', 'P'):
            self.HP = 0
        elif input_map[new_pos[0]][new_pos[1]] == 'P_G':
            self.HP -= 25
        elif input_map[new_pos[0]][new_pos[1]] == 'H_P':
            if self.HP < 100:
                self.HP += 25
            input_map[new_pos[0]][new_pos[1]] = '-'
        elif input_map[new_pos[0]][new_pos[1]] == 'G':
            self.gold += 1
            self.points += 5000
            input_map[new_pos[0]][new_pos[1]] = '-'

        if self.HP <= 0:
            self.points -= 10000
            print('Game over lmao')
            self.is_alive = False
        else:
            self.pos = new_pos
        return input_map, fog_state

    def shoot_wumpus(self, input_map):
        if not self.is_alive:
            return input_map

        if self.facing == 'w' and self.pos[0] > 0:
            if input_map[self.pos[0] - 1][self.pos[1]] == 'W':
                print("Killed Wumpus!")
                input_map[self.pos[0] - 1][self.pos[1]] = '-'
            else:
                print("You missed...")
        elif self.facing == 's' and self.pos[0] < len(input_map) - 1:
            if input_map[self.pos[0] + 1][self.pos[1]] == 'W':
                print("Killed Wumpus!")
                input_map[self.pos[0] + 1][self.pos[1]] = '-'
            else:
                print("You missed...")
        elif self.facing == 'a' and self.pos[1] > 0:
            if input_map[self.pos[0]][self.pos[1] - 1] == 'W':
                print("Killed Wumpus!")
                input_map[self.pos[0]][self.pos[1] - 1] = '-'
            else:
                print("You missed...")
        elif self.facing == 'd' and self.pos[1] < len(input_map[0]) - 1:
            if input_map[self.pos[0]][self.pos[1] + 1] == 'W':
                print("Killed Wumpus!")
                input_map[self.pos[0]][self.pos[1] + 1] = '-'
            else:
                print("You missed...")
        self.points -= 100
        return input_map


def draw_text(text, font_name, size, coordinate, color=(255, 255, 255)) -> tuple:
    display_font = pygame.font.SysFont(font_name, size)
    display_text = display_font.render(text, True, color)
    display_text_rect = display_text.get_rect()
    display_text_rect.topleft = coordinate
    return display_text, display_text_rect


def return_map(filename):
    input_map = []
    with open(filename) as file:
        size = int(file.readline())
        for lines in file:
            input_map.append(lines.replace(' ', '').strip().split('.'))

    return size, input_map


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
            if input_map[x + neighbor[0]][y + neighbor[1]] == element:
                effects.append(element)

    return effects


def draw_cell(input_map, scr, x, y):
    if input_map[x][y] != '-':
        pygame.draw.rect(scr, color_map[input_map[x][y]], (70 + 50 * y, 70 + 50 * x, 30, 30))


def draw_effect(input_map, scr, x, y):
    effects = check_local(input_map, x, y)
    for element in effects:
        pygame.draw.circle(scr, color_map[element],
                           (77 + 50 * y + pos_offset[element][1] * 16,
                            77 + 50 * x + pos_offset[element][0] * 16),
                           5)


def draw_information(scr, agent):
    # Draw the facing direction
    if agent.facing == 'w':
        triangle = [
            (70 + 50 * agent.pos[1], 65 + 50 * agent.pos[0]),
            (100 + 50 * agent.pos[1], 65 + 50 * agent.pos[0]),
            (85 + 50 * agent.pos[1], 50 + 50 * agent.pos[0]),
        ]
    elif game_agent.facing == 'a':
        triangle = [
            (65 + 50 * agent.pos[1], 70 + 50 * agent.pos[0]),
            (65 + 50 * agent.pos[1], 100 + 50 * agent.pos[0]),
            (50 + 50 * agent.pos[1], 85 + 50 * agent.pos[0]),
        ]
    elif game_agent.facing == 's':
        triangle = [
            (70 + 50 * agent.pos[1], 105 + 50 * agent.pos[0]),
            (100 + 50 * agent.pos[1], 105 + 50 * agent.pos[0]),
            (85 + 50 * agent.pos[1], 120 + 50 * agent.pos[0]),
        ]
    elif game_agent.facing == 'd':
        triangle = [
            (105 + 50 * agent.pos[1], 70 + 50 * agent.pos[0]),
            (105 + 50 * agent.pos[1], 100 + 50 * agent.pos[0]),
            (120 + 50 * agent.pos[1], 85 + 50 * agent.pos[0]),
        ]
    else:
        triangle = []
    pygame.draw.polygon(scr, color_map['A'], triangle)

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


def display_map(input_map, size, scr, fog_state, agent):
    for i in range(size):
        for ii in range(size):
            if fog_state[i][ii]:
                pygame.draw.rect(scr, (100, 100, 100), (60 + 50 * ii, 60 + 50 * i, 50, 50))
            else:
                draw_cell(input_map, scr, i, ii)
            pygame.draw.rect(scr, (255, 255, 255), (60 + 50 * ii, 60 + 50 * i, 50, 50), width=1)

    pygame.draw.rect(scr, color_map['A'], (70 + 50 * agent.pos[1], 70 + 50 * agent.pos[0], 30, 30))
    draw_information(scr, agent)

    for i in range(size):
        for ii in range(size):
            if not fog_state[i][ii]:
                draw_effect(input_map, scr, i, ii)


if __name__ == '__main__':
    scr_size = (800, 600)
    pygame.init()
    screen = pygame.display.set_mode(scr_size)
    game_size, game_map = return_map('input.txt')
    game_agent = AgentStats()
    is_fogged = True

    for _ in range(len(game_map)):
        for __ in range(len(game_map[0])):
            if game_map[_][__] == 'A':
                game_agent.pos = (_, __)
                game_map[_][__] = '-'

    running = True
    fog = [[False if game_agent.pos == (_, __) else True for _ in range(len(game_map[0]))] for __ in range(len(game_map))]
    no_fog = [[False for _ in range(len(game_map[0]))] for __ in range(len(game_map))]

    while running:
        screen.fill((0, 0, 0))
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                running = False
                break
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_ESCAPE:
                    running = False
                    break
                if events.key == pygame.K_w and game_agent.facing != 'w':
                    game_agent.facing = 'w'
                    game_agent.points -= 10
                if events.key == pygame.K_s and game_agent.facing != 's':
                    game_agent.facing = 's'
                    game_agent.points -= 10
                if events.key == pygame.K_d and game_agent.facing != 'd':
                    game_agent.facing = 'd'
                    game_agent.points -= 10
                if events.key == pygame.K_a and game_agent.facing != 'a':
                    game_agent.facing = 'a'
                    game_agent.points -= 10
                if events.key == pygame.K_q:
                    game_map = game_agent.shoot_wumpus(game_map)
                if game_agent.is_alive and events.key == pygame.K_SPACE:
                    game_map, fog = game_agent.update_game_state(game_map, fog)
                    game_agent.points -= 10
                if events.key == pygame.K_TAB:
                    is_fogged = not is_fogged

        if is_fogged:
            display_map(game_map, game_size, screen, fog, game_agent)
        else:
            display_map(game_map, game_size, screen, no_fog, game_agent)
        pygame.display.flip()

    pygame.quit()
