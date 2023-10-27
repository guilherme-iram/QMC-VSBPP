from Construction import *
from Neighborhood import *

neighborhood = [swap_bins, delete_bins]

def VND_test(best_solution):

    solution = Solution()
    solution = deepcopy(best_solution)

    for i in range(0, len(neighborhood)):

        solution = neighborhood[i](solution)

        if solution.cost < best_solution.cost:
            best_solution = deepcopy(solution)
            i = 0

    return best_solution        


def VND():
    pass

def VNS(maxIter = 5):
    
    best = construction()
    best.calculateInfo()
    aux_solution = deepcopy(best)
    print(best)

    for i in range(maxIter):
        aux_solution = neighborhood[i % 2](aux_solution)
        aux_solution.calculateInfo()
        aux_solution = VND_test(aux_solution)
        aux_solution.calculateInfo()

        if aux_solution.cost < best.cost:
            
            print("Melhorou: ", aux_solution.cost, best.cost)
            best = deepcopy(aux_solution)
            i = 0
        if i % 10 == 0:
            print("-" * 15)
            print("Iteracao: ", i)
            print("-" * 15)

    print(best)

    return best

