import agent
import program
def main():
    ZaWorld = program.Program()
    ZaWorld.create_world('input1.txt')
    Wumpus = agent.Agent(ZaWorld, 1, 1)
    Wumpus.program.print_world()
    #Wumpus.printAgentMap()
    while True:
        if Wumpus.decide_next_move() == False:
            break  
    print(Wumpus.finalPath)
    
main()