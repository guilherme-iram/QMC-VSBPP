from Instance import *
from Solution import *



def trivial_solution():
    sol = Solution()
    j = 0
    for item in Instance.itemsData:
        lowest_cost = float('inf')
        best_type = -1
        for type in Instance.binsData:
            if type.cost < lowest_cost:
                available_capacity = True
                for dim in range(Instance.d):

                        if item.dimensions[dim] > type.dimensions[dim]:
                             available_capacity = False
                             break
                
                if available_capacity:
                    lowest_cost = type.cost
                    best_type = type.id
                    break # considerando que os tipos estão ordenados por custo, o primeiro que couber é o melhor
        
        
        
        bin = Bin()

        bin.type = best_type

        bin.addItem(item.id)
        bin.totalJointCost += item.totalJointCost
        sol.bins.append(bin)
        sol.itemsBin[item.id] = j
        sol.cost += lowest_cost
        sol.cost += item.totalJointCost


        j += 1
    
    return sol

def calculate_distance(sol:Solution, j1:int, j2:int):
            
    best_k = -1
    best_cost = float('inf')
    # o cálculo abaixo é pra recuperar a soma das dimensões dos itens dos bins j1 e j2
    sum_dim = [sol.bins[j1].dimensions[dim] + sol.bins[j2].dimensions[dim] for dim in range(Instance.d)]
    

    c_j1 = sol.bins[j1].totalJointCost + Instance.binsData[sol.bins[j1].type].cost
    c_j2 = sol.bins[j2].totalJointCost + Instance.binsData[sol.bins[j2].type].cost

    for type in Instance.binsData:
        if type.cost < best_cost:
            available_capacity = True
            for dim in range(Instance.d):
                if sum_dim[dim] > type.dimensions[dim]:
                    available_capacity = False
                    break
                
            if available_capacity:
                best_cost = type.cost
                best_k = type.id
                break # considerando que os tipos estão ordenados por custo, o primeiro que couber é o melhor
    
    j_line_items = sol.bins[j1].items + sol.bins[j2].items

    jointCost = sol.bins[j1].totalJointCost + sol.bins[j2].totalJointCost

    for itemId in j_line_items:
        item = Instance.itemsData[itemId]
        for dependentIndex in range(len(item.links)):
            if item.links[dependentIndex] == 1:
                dependentId = Instance.itemsData[itemId].links[dependentIndex]
                if dependentId in j_line_items:
                    jointCost -= Instance.linkMatrix[item.id][dependentId]
    

    distance = c_j1 + c_j2 - (jointCost + best_cost) # c(j1) + c(j2) - c(j') 

    
    

    return best_k, distance

def construction():
     
    sol = trivial_solution()
    
    
    while True:
        best_k = -1
        #best_cost = float('inf')
        best_distance = 0
        best_j1 = -1
        best_j2 = -1
        

        for j1 in range(len(sol.bins)-1):
            for j2 in range(j1+1, len(sol.bins)):
                k, distance = calculate_distance(sol, j1, j2)
                if distance > best_distance:
                    best_distance = distance
                    best_k = k
                    best_j1 = j1
                    best_j2 = j2
                    
        

        if best_distance < epsilon:
            print(f'best_distance: {best_distance}')
            return sol
        
        sol.mergeBins(best_j1, best_j2, best_k)
        