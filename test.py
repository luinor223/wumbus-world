from kb import KnowledgeBase
from program import Program
from agent import Agent

ZaWorld = Program()
ZaWorld.create_world('test_cases/test6_poisoned.txt')
ZaWorld.print_world()
dio = Agent(ZaWorld, 1, 1)
dio.explore()
print(dio.action_log)