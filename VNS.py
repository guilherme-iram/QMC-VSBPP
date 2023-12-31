from Construction import *
from Neighborhood import *
import time

#neighborhood = [swap_bins, delete_bins]

def VND(best_solution):

    current = deepcopy(best_solution)

    while True:
        current = bestImprovementMigrateItems(current)
        current = bestImprovementSwapItems(current)

        if best_solution.cost - current.cost > epsilon:
            best_solution = deepcopy(current)
            continue
        
        return best_solution


def bestImprovementMigrateItems(solution:Solution):
    best_i = -1 # index do melhor item
    best_j = -1 # index do melhor bin

    improved = False

    best_cost = solution.cost
    new_cost = 0.0


    for i in range(1, Instance.n+1):
        for j in range(1, len(solution.bins)+1):

            if solution.items[i].binId == j:
                continue

            new_cost = solution.evaluateMigrateItem(i, j)

            if (best_cost - new_cost > epsilon): # se houver melhoria no custo
                # checa se o item i cabe no bin j

            
                #print(f'best_cost: {best_cost} new_cost: {new_cost}')
                improved = True
                best_cost = new_cost
                best_i = i
                best_j = j
    
    if improved == True:
        
        #print(f'best_cost: {best_cost}, best_i: {best_i}, best_j: {best_j}')
        solution.migrateItem(best_i, best_j)
    
    return solution
    

def bestImprovementSwapItems(solution:Solution):
    best_i = -1 # index do melhor item i
    best_j = -1 # index do melhor item j

    improved = False

    best_cost = solution.cost

    for i in range(1, Instance.n):
        for j in range(i+1, Instance.n + 1):
            
            if solution.items[i].binId == solution.items[j].binId:
                continue
            
            new_cost = solution.evaluateSwapItems(i, j)
            
            if (best_cost - new_cost > epsilon):
                improved = True
                best_cost = new_cost
                best_i = i
                best_j = j
    
    if improved == True:
        #print(f'best_cost: {best_cost}, best_i: {best_i}, best_j: {best_j}')
        solution.swapItems(best_i, best_j)
    
    return solution



def VNS(max_iter = 2000, time_limit = 600.0):
    
    best = construction()
    best.calculateInfo()

    k = 1
    start = time.time()
    # for i in range(max_iter):
    iter = 0
    while True:
        k = 1

        while(k <= 3):
           
            if k == 1:
                current = swap_bins(best)
                #print('Swap bins')
            elif k == 2:
                current = delete_bins(best)
                #print('Delete bins')
            elif k == 3:
                current = permutation_shortest_path(best)
                #print('Permutation shortest path')
            
            current = VND(current)

            if best.cost - current.cost > epsilon:
                print(f"Melhora: {best.cost} -> {current.cost} (delta: {best.cost - current.cost})")
                best = deepcopy(current)
                
                k = 1
                iter = 0
            else:
                k += 0
                iter += 1
        
            if time.time() - start > time_limit:
                #print('Retorno por tempo')
                return best    
            
            if iter > max_iter:
                #print('Retorno por maxIter')
                return best


        if time.time() - start > time_limit:
                #print('Retorno por tempo')
                return best
