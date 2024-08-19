from agent import Agent
from program import Program
import pygame
from display_mode import PseudoAgent


def main():
    # input_file = 'test_cases/test5_purple_haze.txt'
    input_file = input("Provide the input file (ex: input.txt) :")

    ZaWorld = Program()
    ZaWorld.create_world(input_file)
    ZaWorld.print_world()
    dio = Agent(ZaWorld, 1, 1)
    dio.explore()
    result_file = Program.generate_output_filename(input_file)
    dio.output_action_log(result_file) 

    jotaro = PseudoAgent(dio.action_log, input_file)

    scr_size = (800, 600)
    pygame.init()
    screen = pygame.display.set_mode(scr_size)
    pygame.display.set_caption("Wumpus World")
    pygame.display.set_icon(pygame.image.load("assets/W.png"))
    fps = 20
    frame = 0
    pyclock = pygame.time.Clock()
    fog_mode = 0
    auto_move = False

    running = True
    while running:
        pyclock.tick(60)
        frame += 1
        screen.fill((0, 0, 0))

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                running = False
                break

            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_TAB:
                    fog_mode += 1
                    fog_mode %= 3
                if events.key == pygame.K_SPACE:
                    auto_move = not auto_move
                if events.key == pygame.K_RIGHT:
                    jotaro.next_step()

        if frame == fps:
            jotaro.display(screen, fog_mode)
            pygame.display.flip()

            if auto_move:
                auto_move = jotaro.next_step()

            frame = 0

    pygame.quit()


if __name__ == "__main__":
    main()
