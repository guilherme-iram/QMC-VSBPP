from Construction import *
from Neighborhood import *

neighborhood = [swap_bins, delete_bins]

def VND(best_solution):

    solution = Solution()
    solution = deepcopy(best_solution)

    for i in range(0, len(neighborhood)):

        solution = neighborhood[i](solution)

        if solution.cost < best_solution.cost:
            best_solution = deepcopy(solution)
            i = 0

    return best_solution        


def VNS():
    
    best = construction()
    best.calculateInfo()

    print("Custo inicial: ", best.cost)

    aux_solution = deepcopy(best)
    
    iter = 0
    
    for k in range(len(neighborhood)):
        
        aux_solution = neighborhood[k](aux_solution)
        aux_solution.calculateInfo()
        aux_solution = VND(aux_solution)
        aux_solution.calculateInfo()

        if aux_solution.cost < best.cost:
            print("Melhorou: ", aux_solution.cost, best.cost)
            best = deepcopy(aux_solution)
            k = 0

        if iter % 10 == 0:
            print("-" * 15)
            print("Iteracao: ", iter)
            print("-" * 15)

        iter += 1 

    return best