
from Neighborhood import *

def VND(solution:Solution)->None:
    current = Solution()
    current.copy(solution)

    while True:

        bestImprovementMigrateItem(current)
        if solution.cost - current.cost > epsilon:
            solution.copy(current)
            #print(solution.cost)
            continue


        break

def bestImprovementMigrateItem(solution:Solution)-> None:
    best_i = -1 # index do melhor item
    best_j = -1 # index do melhor bin

    improved = False

    best_cost = solution.cost
    new_cost = 0.0


    for i in range(Instance.n):
        for j in range(len(solution.bins)):

            if solution.itemsBin[i] == j:
                continue

            new_cost = solution.evaluateMigrateItem(i, j)

            if (best_cost - new_cost > epsilon): # se houver melhoria no custo
                # checa se o item i cabe no bin j

                if solution.bins[j].canAddItem(i): 
                    #print(f'best_cost: {best_cost} new_cost: {new_cost}')
                    improved = True
                    best_cost = new_cost
                    best_i = i
                    best_j = j
    
    if improved == True:
        #print(f'best_cost: {best_cost}, best_i: {best_i}, best_j: {best_j}')
        solution.migrateItem(best_i, best_j)
        


def bestImprovementSwapItems(solution:Solution)->None:
    best_i = -1 # index do melhor item i
    best_j = -1 # index do melhor item j

    can_i = False
    can_j = False

    improved = False

    best_cost = solution.cost
    new_cost = 0.0

    for i in range(Instance.n - 1):
        for j in range(i + 1,  Instance.n):

            new_cost = solution.evaluateSwapItems(i, j)

            if (best_cost - new_cost > epsilon): # se houver melhoria no custo
                
                bin_i = solution.itemsBin[i]

                can_i = solution.bins[bin_i].canSwapItems(i, j)

                bin_j = solution.itemsBin[j]

                can_j =  solution.bins[bin_j].canSwapItems(j, i)

                if can_i and can_j:
                    improved = True
                    best_cost = new_cost
                    best_i = i
                    best_j = j
    
    if improved == True:
        solution.swapItems(best_i, best_j)

def VNS():
    best = construction()
    best.calculateInfo()
    #VND(best)

    #best.evaluateMigrateItem(0, 2)

    return best


