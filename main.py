import time

from agent import Agent
from program import Program
import pygame
from display_mode import PseudoAgent


def main():


    ZaWorld = Program()
    ZaWorld.create_world('input.txt')
    ZaWorld.print_world()
    dio = Agent(ZaWorld, 1, 1)
    dio.explore()
    dio.output_action_log()

    jotaro = PseudoAgent(dio.action_log, 'input.txt')
    scr_size = (800, 600)
    pygame.init()
    screen = pygame.display.set_mode(scr_size)
    jotaro.display(screen)
    pygame.display.flip()
    time.sleep(1)
    time_stop = jotaro.next_step()
    jotaro.display(screen)
    pygame.display.flip()
    while time_stop:
        screen.fill((0, 0, 0))
        time.sleep(1)
        time_stop = jotaro.next_step()
        jotaro.display(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()