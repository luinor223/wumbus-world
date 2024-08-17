from agent import Agent
from program import Program
def main():
    ZaWorld = Program()
    ZaWorld.create_world('input2.txt')
    ZaWorld.print_world()
    dio = Agent(ZaWorld, 1, 1)
    dio.explore()
    print(dio.action_log)
    print(dio.points)
    print(dio.HP)
if __name__ == "__main__":
    main()