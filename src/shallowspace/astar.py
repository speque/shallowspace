'''
Created on Dec 9, 2010

@author: pekka
'''

import math

def a_star(start, goal, map):
    closedset = set()                               # The set of nodes already evaluated.     
    openset =  set()                                # The set of tentative nodes to be evaluated.
    openset.add(start)
    came_from = {}
    g_score = {}                                    #The map of navigated nodes.
    h_score = {}
    f_score = {}
    g_score[start.id] = 0                           # Distance from start along optimal path.
    h_score[start.id] = heuristic_estimate_of_distance(map, start, goal)
    f_score[start.id] = h_score[start.id]           # Estimated total distance from start to goal through y.
    
    while not len(openset) == 0:
        lowest_f_score = 1000
        x = None
        for sector in openset:
            if f_score[sector.id] < lowest_f_score:
                x = sector
                lowest_f_score = f_score[sector.id]
        if x == goal:
            if len(came_from) == 0:
                return []
            else:
                return reconstruct_path(came_from, came_from[goal.id])
        
        openset.remove(x)
        closedset.add(x)
        
        for y in x.neighbors:
            if y == None or y in closedset:
                continue
            tentative_g_score = g_score[x.id] + 1      # 1 = distance between x and y
 
            if y not in openset:
                openset.add(y)
                tentative_is_better = True
            elif tentative_g_score < g_score[y.id]:
                tentative_is_better = True
            else:
                tentative_is_better = False
                
            if tentative_is_better:
                came_from[y.id] = x
                g_score[y.id] = tentative_g_score
                h_score[y.id] = heuristic_estimate_of_distance(map, y, goal)
                f_score[y.id] = g_score[y.id] + h_score[y.id]
    return None
 

 
def reconstruct_path(came_from, current_node):
    if current_node.id in came_from:
        p = reconstruct_path(came_from, came_from[current_node.id])
        p.append(current_node)
        return p
    else:
        return [current_node]

def heuristic_estimate_of_distance(map, start, goal):
    start_x = map.sector_x(start)
    start_y = map.sector_y(start)
    goal_x = map.sector_x(goal)
    goal_y = map.sector_y(goal)
    return math.sqrt(math.pow(start_x - goal_x, 2) + math.pow(start_y - goal_y, 2)) 
