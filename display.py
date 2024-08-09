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


def return_map(filename):
    input_map = []
    with open(filename) as file:
        size = int(file.readline())
        for lines in file:
            input_map.append(lines.strip().split('.'))

    return size, input_map


def draw_cell(input_map, size, scr, x, y):
    if input_map[x][y] != '-':
        pygame.draw.rect(scr, color_map[input_map[x][y]], (70 + 50 * y, 70 + 50 * x, 30, 30))


def draw_effect(input_map, size, scr, x, y):
    a = 16
    if input_map[x][y] not in ('A', 'G', '-'):
        if x > 0:
            pygame.draw.circle(scr, color_map[input_map[x][y]],
                               (77 + 50 * y + pos_offset[input_map[x][y]][1] * a,
                                77 + 50 * (x - 1) + pos_offset[input_map[x][y]][0] * a),
                               5)
        if y > 0:
            pygame.draw.circle(scr, color_map[input_map[x][y]],
                               (77 + 50 * (y - 1) + pos_offset[input_map[x][y]][1] * a,
                                77 + 50 * x + pos_offset[input_map[x][y]][0] * a),
                               5)
        if x < size - 1:
            pygame.draw.circle(scr, color_map[input_map[x][y]],
                               (77 + 50 * y + pos_offset[input_map[x][y]][1] * a,
                                77 + 50 * (x + 1) + pos_offset[input_map[x][y]][0] * a),
                               5)
        if y < size - 1:
            pygame.draw.circle(scr, color_map[input_map[x][y]],
                               (77 + 50 * (y + 1) + pos_offset[input_map[x][y]][1] * a,
                                77 + 50 * x + pos_offset[input_map[x][y]][0] * a),
                               5)


def display_map(input_map, size, scr):
    for i in range(size):
        for ii in range(size):
            pygame.draw.rect(scr, (255, 255, 255), (60 + 50 * ii, 60 + 50 * i, 50, 50), width=1)
            draw_cell(input_map, size, scr, i, ii)
    for i in range(size):
        for ii in range(size):
            draw_effect(input_map, size, scr, i, ii)
    pass


if __name__ == '__main__':
    scr_size = (800, 600)
    pygame.init()
    screen = pygame.display.set_mode(scr_size)
    game_size, game_map = return_map('input.txt')

    running = True

    while running:
        screen.fill((0, 0, 0))
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                running = False
                break

        display_map(game_map, game_size, screen)
        pygame.display.flip()

    pygame.quit()
