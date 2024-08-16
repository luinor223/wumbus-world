from agent import Agent
from program import Program
def main():
    ZaWorld = Program()
    ZaWorld.create_world('input1.txt')
    ZaWorld.print_world()
    dio = Agent(ZaWorld, 1, 1)
    dio.explore()
    print(dio.action_log)
main()