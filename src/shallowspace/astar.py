'''
Created on Dec 9, 2010

@author: pekka
'''

import math

def a_star(start, goal, game_map):
    closedset = set()                               # The set of nodes already evaluated.     
    openset =  set()                                # The set of tentative nodes to be evaluated.
    openset.add(start)
    came_from = {}
    g_score = {}                                    #The game_map of navigated nodes.
    h_score = {}
    f_score = {}
    g_score[start.sector_id] = 0                           # Distance from start along optimal path.
    h_score[start.sector_id] = heuristic_estimate_of_distance(game_map, start, goal)
    f_score[start.sector_id] = h_score[start.sector_id]           # Estimated total distance from start to goal through neighbor.
    
    while not len(openset) == 0:
        lowest_f_score = 1000
        candidate = None
        for sector in openset:
            if f_score[sector.sector_id] < lowest_f_score:
                candidate = sector
                lowest_f_score = f_score[sector.sector_id]
        if candidate == goal:
            if len(came_from) == 0:
                return []
            else:
                return reconstruct_path(came_from, came_from[goal.sector_id])
        
        openset.remove(candidate)
        closedset.add(candidate)
        
        for neighbor in candidate.neighbors:
            if neighbor == None or neighbor in closedset or not game_map.map_state.sector_is_free(neighbor):
                continue
            tentative_g_score = g_score[candidate.sector_id] + 1      # 1 = distance between candidate and neighbor
 
            if neighbor not in openset:
                openset.add(neighbor)
                tentative_is_better = True
            elif tentative_g_score < g_score[neighbor.sector_id]:
                tentative_is_better = True
            else:
                tentative_is_better = False
                
            if tentative_is_better:
                came_from[neighbor.sector_id] = candidate
                g_score[neighbor.sector_id] = tentative_g_score
                h_score[neighbor.sector_id] = heuristic_estimate_of_distance(game_map, neighbor, goal)
                f_score[neighbor.sector_id] = g_score[neighbor.sector_id] + h_score[neighbor.sector_id]
    return None
 

 
def reconstruct_path(came_from, current_node):
    if current_node.sector_id in came_from:
        path = reconstruct_path(came_from, came_from[current_node.sector_id])
        path.append(current_node)
        return path
    else:
        return [current_node]

def heuristic_estimate_of_distance(game_map, start, goal):
    start_x = game_map.sector_x(start)
    start_y = game_map.sector_y(start)
    goal_x = game_map.sector_x(goal)
    goal_y = game_map.sector_y(goal)
    return math.sqrt(math.pow(start_x - goal_x, 2) + math.pow(start_y - goal_y, 2)) 
