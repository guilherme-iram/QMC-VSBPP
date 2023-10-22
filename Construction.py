from Instance import *
from Solution import *

def trivial_solution():
    sol = Solution.from_Instance()
    for j in range(len(Instance.items)):
        item = Instance.items[j]
        lowest_cost = float('inf')
        best_type = -1
        for type in Instance.bins:
            if type.cost < lowest_cost:
                available_capacity = True
                for dim in range(Instance.d):

                        if item.weight[dim] > type.capacity[dim]:
                             available_capacity = False
                             break
                
                if available_capacity:
                    lowest_cost = type.cost
                    best_type = type.id
        
        sol.bins.add(best_type)
        sol.items[item.id - 1].setBinBeforeCalc(j)
    
    return sol
        

def calculate_distance(sol, j1, j2):
    best_k = -1
    best_cost = float('inf')



    sum_weight = [0 for _ in range(Instance.d)]

    for dim in range(Instance.d):
        pass
    
    
    for type in Instance.bins:
        

        pass

    return best_k, best_cost

        

def construction():
    sol = trivial_solution()

    while True:
        largestDist = 0
        for j1 in range(sol.bins.nextIndex - 1):
            for j2 in range(j1 + 1, sol.bins.nextIndex):
                
                pass

        
        if largestDist == 0:
            break

    return sol
                    
                        

    