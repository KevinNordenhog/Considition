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


# A "solution" that takes a step in a random direction every turn
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
        print route
        #print(tiles[current_y_pos][current_x_pos])
        
        # !=  {'type': 'forest'} and tiles[x][y] !=  {'type': 'water'} and tiles[x][y] !=  {'type': 'trail'} and tiles[x][y] !=  {'type': 'road'}):
        while not state["gameStatus"] == "done":
            #print("Starting turn: " + str(state["turn"]))
            tiles = state["tileInfo"]
            #print(str(state["yourPlayer"]))
            current_player = state["yourPlayer"]
            current_y_pos = current_player["yPos"]
            current_x_pos = current_player["xPos"]
            current_pos = (current_x_pos,current_y_pos)

            if (current_pos not in route):
                route = a_star_search(tiles, (current_x_pos,current_y_pos), winPos)
                print "whaaaaaaaaaaaat"
            
            

            n = neighbors(tiles, current_pos)

            for i in n:
                if i in route:
                    next_step = i
                    print "next {}".format(next_step)
                    print "curr {}" .format(current_pos)
            if (next_step[1] == (current_pos[1]-1)):
                step_direction = "n"
            elif (next_step[1] == (current_pos[1]+1)):
                step_direction = "s"
            elif ((next_step[0]) == current_pos[0]-1):
                step_direction = "w"
            elif ((next_step[0]) == current_pos[0]+1):
                step_direction = "e"
            else:
                step_direction_array = ["w", "e", "n", "s"]
                random_step = random.randint(0, 3)
                step_direction= step_direction_array[random_step]
            route.remove(current_pos)


            # # Take a step in a random direction
            # step_direction_array = ["w", "e", "n", "s"]
            # random_step = random.randint(0, 3)


            #print("Stepped: " + str(step_direction_array[random_step]))
            response = _api.step(game_id, step_direction)
            if response:
                state = response["gameState"]
        print("Finished!")
    else:
        print(initial_state["message"])


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
                new_cost = cost_so_far[current] + 1#cost(graph, current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost #+ heuristic(goal, next) ska denhär vara med ? ? ? ? har ingen aning
                    frontier.put(next, priority)
                    came_from[next] = current
                #print ("{} in {}" .format(next, neighbors(graph, current)))
            

    temp2 = 1
    temp = current
    while (temp in came_from):
        temp2 += 1
        path.append(temp)
        temp = came_from[temp]
    print temp2
    return path


def neighbors(graph, current): 
    templist = []
    # if ((0 <= (current[0]+1) < 100) and (0 <= (current[1]) < 100)):
    #     templist.append(((current[0]),(current[1]+1)))
    # if ((0 <= (current[0]-1) < 100) and (0 <= (current[1]) < 100)):
    #     templist.append(((current[0]),(current[1]-1)))
    # if ((0 <= (current[0]) < 100) and (0 <= (current[1]+1) < 100)):
    #     templist.append(((current[0]+1),(current[1])))    
    # if ((0 <= (current[0]) < 100) and (0 <= (current[1]-1) < 100)):
    #     templist.append(((current[0]-1),(current[1])))
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