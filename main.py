# coding=utf-8
from api import API
import random
import sys
from Queue import *

# TODO : Insert your API-key here
_api_key = "bdf45aba-bdf2-49fe-b5a2-0a29e8758f63"
# Specify your API-key number of players per game),
# mapname, and number of waterstreams/elevations/powerups here
_api = API(_api_key, 1, "standardmap", 10, 10, 10)
# MAPS: ", 10, 10, 10)
# MAPS: standardmap , watermap , roadmap , trailmap 


def solution(game_id):
    initial_state = _api.get_game(game_id)
    if initial_state["success"]:
        state = initial_state["gameState"]
        tiles = state["tileInfo"]
        current_player = state["yourPlayer"]
        current_y_pos = current_player["yPos"]
        current_x_pos = current_player["xPos"]
        winPos = findWin(tiles)
        print(winPos)
        route = a_star_search(tiles, (current_x_pos,current_y_pos), winPos)
        print (route)
        #print(tiles[current_y_pos][current_x_pos])
        print (state["yourPlayer"])
        next_step = ()
        # print tiles[5][70]
        # print tiles[7][70]#
        # print tiles[5][80]
        # print tiles[8][70]#
        # print tiles[9][70]#
        # print tiles[4][80]
        # print tiles[3][80]








        
        # !=  {'type': 'forest'} and tiles[x][y] !=  {'type': 'water'} and tiles[x][y] !=  {'type': 'trail'} and tiles[x][y] !=  {'type': 'road'}):
        while not state["gameStatus"] == "finish":#"done":
            #print("Starting turn: " + str(state["turn"]))
            tiles = state["tileInfo"]
            #print(str(state["yourPlayer"]))
            current_player = state["yourPlayer"]
            current_y_pos = current_player["yPos"]
            current_x_pos = current_player["xPos"]
            current_pos = (current_x_pos,current_y_pos)
            #print current_player

            # if (current_pos not in route):
            #     route = a_star_search(tiles, (current_x_pos,current_y_pos), winPos)
            #     print ("whaaaaaaaaaaaat")
            # else:
            #     if next_step in route:
            #         route.remove(next_step)
            
           # if (current_pos not in route or next_step in route):
            route = a_star_search(tiles, (current_x_pos,current_y_pos), winPos)
            print (state["turn"]) #271 standard
            #print (current_pos)
            #print (tiles[current_y_pos][current_x_pos])

            #route = a_star_search(tiles, (current_x_pos,current_y_pos), winPos)

            n = neighbors(tiles, current_pos)

            for i in n:
                if i in route:
                    next_step = i
                    # print ("next {}".format(next_step))
                    # print ("curr {}" .format(current_pos))
           





            #Watertiles decrement 45 movepoints when entered
            #Roadtiles decrement 31 movepoints when entered
            #Trailtiles decrement 40 movepoints when entered
            #Grasstiles decrement 50 movepoints when entered
            
            #If you have more than 20 movepoints left when you try to enter an impassable tile (or go out of bounds) you will get stunned, otherwise you will just stop on your current tile.

            #For each tile the player moves through that contains rain, an additional 7 stamina will be drained.



            #"Fast" -> 210, "Medium" -> 150, "Slow" -> 100. Step always moves 1 tile.

            move = False
            speed = "slow"
            if (next_step[1] == (current_pos[1]-1)):
                step_direction = "n"
                if ((next_step[0],next_step[1]-1) in route and (next_step[0],next_step[1]-2) in route):# and (next_step[0],next_step[1]-3) in route):
                    move = True
                    if (current_player["stamina"] > 75):
                        speed = "medium"
            elif (next_step[1] == (current_pos[1]+1)):
                step_direction = "s"
                if ((next_step[0],next_step[1]+1) in route and (next_step[0],next_step[1]+2) in route):# and (next_step[0],next_step[1]+3) in route):
                    move = True
                    if (current_player["stamina"] > 75):
                        speed = "medium"
            elif ((next_step[0]) == current_pos[0]-1):
                step_direction = "w"
                if ((next_step[0]-1,next_step[1]) in route and (next_step[0]-2,next_step[1]) in route):# and (next_step[0]-3,next_step[1]) in route):
                    move = True
                    if (current_player["stamina"] > 75):
                        speed = "medium"
            elif ((next_step[0]) == current_pos[0]+1):
                step_direction = "e"
                if ((next_step[0]+1,next_step[1]) in route and (next_step[0]+2,next_step[1]) in route):# and (next_step[0]+3,next_step[1]) in route):
                    move = True
                    if (current_player["stamina"] > 75):
                        speed = "medium"
            else:
                step_direction_array = ["w", "e", "n", "s"]
                random_step = random.randint(0, 3)
                step_direction= step_direction_array[random_step]
            if current_pos in route:
                route.remove(current_pos)

            # Funktionslista från _api:
            #     step(self, game_id, direction):
            #     make_move(self, game_id, direction, speed):
            #     rest(self, game_id):
            #     use_powerup(self, game_id, powerup_name):
            #     drop_powerup(self, game_id, powerup_name):
            #current_player:   {u'status': u'swimming', u'playedTurns': 48, u'xPos': 9, u'apiKey': u'bdf45aba-bdf2-49fe-b5a2-0a29e8758f63', u'statusDuration': 0, u'name': u'Sm\xe5l\xe4nska Gubbarna', u'powerupInventory': [u'Cyklop', u'StaminaSale', u'Shoes'], u'lastTurnPlayed': 48, u'yPos': 79, u'stamina': 100, u'activePowerups': [], u'lastTimeActive': u'2018-10-20T10:41:40.0280966+02:00'}

            #print("Stepped: " + str(step_direction_array[random_step]))
            #if (current_player["stamina"] < 40):
            #    _api.rest(game_id)
            #    print (tiles[current_y_pos][current_x_pos])
            if (move or ("weather" in tiles[current_y_pos][current_x_pos]) ):
                response = _api.make_move(game_id, step_direction, speed)
            else:
                response = _api.step(game_id, step_direction)
            if response:
                state = response["gameState"]
                if (state == "Game has finished"):
                    return
        print("Finished!")
    else:
        print (initial_state["message"])
        return


# for x in range(0,100):
#             for y in range(0,100):
#                 if (tiles[x][y]['type'] != 'forest' and tiles[x][y]['type'] != 'road' and tiles[x][y]['type'] != 'water' and tiles[x][y]['type'] != 'trail' and tiles[x][y]['type'] != 'grass' and ):
#                     print(x,y)
#                     print(tiles[x][y])

def main():
    game_id = "9fdefed0-aa5f-4856-87f9-9e17d1cc082c"
    # If no gameID is specified as parameter to the script,
    # Initiate a game with 1 player on the standard map
    if len(sys.argv) == 1:
        _api.end_previous_games_if_any()  # Can only have 2 active games at once. This will end any previous ones.
        game_id = _api.init_game()
        joined_game = _api.join_game(game_id)
        readied_game = _api.try_ready_for_game(game_id)
        if readied_game is not None:
            print("Joined and readied! Solving...")
            solution(game_id)
            #print (_api.get_game(game_id)["gameState"]["tileInfo"])#[0][5])

    else:
        game_id = sys.argv[1]

def findWin(graph):
    for x in range(0,100):
            for y in range(0,100):
                if(graph[y][x]['type'] == 'win'):
                    return (x,y)


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    path = []
    booli = True
    while not (frontier.empty() and booli):
        current = frontier.get()
        
        if current == goal:
            break
        
        for next in neighbors(graph, current):
            if((graph[next[1]][next[0]]['type'] == 'water') or (graph[next[1]][next[0]]['type'] == 'road') or (graph[next[1]][next[0]]['type'] == 'trail') or (graph[next[1]][next[0]]['type'] == 'grass') or (graph[next[1]][next[0]]['type'] == 'win')):
                #print ("{} on {}" .format((graph[next[0]][next[1]]),(next[0],next[1])))
                new_cost = (cost_so_far[current] + int(cost(graph, current, next)))
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current
                #print ("{} in {}" .format(next, neighbors(graph, current)))
            

    temp2 = 1
    temp = current
    while (temp in came_from):
        temp2 += 1
        path.append(temp)
        temp = came_from[temp]
    #print (temp2) #Gives the steps left
    return path

# Calculates the additional cost for A* based on what type of tile and conditions 
def cost(graph, current, next):
    if (graph[next[1]][next[0]]['type'] == 'water'):
        if "waterstream" in graph[next[1]][next[0]]:
            if (graph[next[1]][next[0]]["waterstream"]["speed"] > 40):
                if not sameDir(current, next, graph[next[1]][next[0]]["waterstream"]["direction"]):
                    return int(6)
                else: 
                    return int(4)
            else:
                return int(5)
    
    elif (graph[next[1]][next[0]]['type'] == 'road' or graph[next[1]][next[0]]['type'] == 'trail'):
        if "elevation" in graph[next[1]][next[0]]:
            if (graph[next[1]][next[0]]["elevation"]["amount"] > 30):
                if sameDir(current, next, graph[next[1]][next[0]]["elevation"]["direction"]):
                    return int(6)
                else: 
                    return int(4)
            else:
                return int(5)
    #else:
    return int(4)


    

    #{"type": "water",   NOTE same direction === GOOOD
    #"waterstream": {
	#"direction": "s",
    #"speed": 15
    #}}

    #{"type": "road",   same when type == trail  NOTE same direction ==== BAAAAD
    #"elevation": {
        #"direction": "e",
	#"amount": 28
    #}
    # "weather": "rain"} 



# Calculates the cost of movementpoints to enter a tile (based on type and conditions)
#def movementCost(graph, (x, y)): 


#Direction is "s", "e", "w" or "n"
def sameDir(current, next, direction):
    if (next[1] == (current[1]-1)):
        if (direction == "n"):
            return True
        else:
            return False    
    elif (next[1] == (current[1]+1)):
        if (direction == "s"):
            return True
        else:
            return False
        
    elif ((next[0]) == current[0]-1):
        if (direction == "w"):
            return True
        else:
            return False
        
    elif ((next[0]) == current[0]+1):
        if (direction == "e"):
            return True
        else:
            return False


def neighbors(graph, current): 
    templist = []
    if ((0 <= (current[0]+1) < 100) and (0 <= (current[1]) < 100)):
        templist.append(((current[0]+1),(current[1])))
    if ((0 <= (current[0]-1) < 100) and (0 <= (current[1]) < 100)):
        templist.append(((current[0]-1),(current[1])))
    if ((0 <= (current[0]) < 100) and (0 <= (current[1]+1) < 100)):
        templist.append(((current[0]),(current[1]+1)))
    if ((0 <= (current[0]) < 100) and (0 <= (current[1]-1) < 100)):
        templist.append(((current[0]),(current[1]-1)))
    return templist#[((current[0]+1),(current[1])), ((current[0]-1),(current[1])), ((current[0]),(current[1]-1)), ((current[0]),(current[1]+1))]


main()
