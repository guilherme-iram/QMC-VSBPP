from Instance import *
from Solution import *

def trivial_solution():
    sol = Solution()
    j = 1
    for item in Instance.items_Data:
        lowest_cost = float('inf')
        best_type = -1
        for type in Instance.bins_Data:
            if type.cost < lowest_cost:
                available_capacity = True
                for dim in range(Instance.d):

                        if item.weight[dim] > type.capacity[dim]:
                             available_capacity = False
                             break
                
                if available_capacity:
                    lowest_cost = type.cost
                    best_type = type.id
        
        
        
        sol.bins[j] = Bin(best_type)
        sol.bins[j].addItem(item)
        sol.items[item.id].setBinBeforeCalc(j)

        j += 1
    
    return sol
        
def calculate_distance(sol:Solution, j1:int, j2:int):

    best_k = -1
    best_cost = float('inf')

    sum_dim = [sol.bins[j1].weight[dim] + sol.bins[j2].weight[dim] for dim in range(Instance.d)]    
    
    j_line_items = sol.bins[j1].items + sol.bins[j2].items

    #jointCost = 0

    c_j1 = sol.bins[j1].jointCost + sol.bins[j1].cost
    c_j2 = sol.bins[j2].jointCost + sol.bins[j2].cost
    # o cálculo do jointCost é feito no loop abaixo. Ele não importa muito para essa escolha
    # tendo em vista que queremos, simplesmente, o bin mais barato se encaixa com os dois itens
    for type in Instance.bins_Data:
        if type.cost < best_cost:
            available_capacity = True
            for dim in range(Instance.d):
                if sum_dim[dim] > type.capacity[dim]:
                    available_capacity = False
                    break
            
            if available_capacity:
                best_cost = type.cost
                best_k = type.id
    
    jointCost = sol.bins[j1].jointCost + sol.bins[j2].jointCost

    for itemId in j_line_items:
        item = sol.items[itemId]
        for dependentIndex in range(item.nOfDependentItems):
            if item.dependentItems[dependentIndex] == 1:
                dependentId = Instance.items_Data[item.id].linked_Ids[dependentIndex]
                if dependentId in j_line_items:
                    jointCost -= Instance.linked_items_Matrix[item.id][dependentId]
    

    distance = c_j1 + c_j2 - (jointCost + best_cost) # c(j1) + c(j2) - c(j') 

    return best_k, distance

        

def construction(sol = None):
    if sol is None:
        sol = trivial_solution()
    else:
        sol.calculateInfo()
    
    while True:
        best_k = -1
        #best_cost = float('inf')
        best_distance = 0
        best_j1 = -1
        best_j2 = -1

        for j1 in range(1, len(sol.bins)):
            for j2 in range(j1+1, len(sol.bins) + 1):
                k,  distance = calculate_distance(sol, j1, j2)

                if distance > best_distance:
                    best_distance = distance
                    best_k = k
                    #best_cost = cost
                    best_j1 = j1
                    best_j2 = j2 
        
        if best_distance <= epsilon:
            return sol


        sol.merge(best_j1, best_j2, best_k)
        
        
                        

    