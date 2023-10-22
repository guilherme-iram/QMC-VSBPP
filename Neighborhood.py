from Solution import *
from Instance import *
import random
from Construction import * 


random.seed(42)

def swap_all_itens(bin_1, bin_2):
    
    all_items_bin_1 = [item for item in bin_1.items]
    all_items_bin_2 = [item for item in bin_2.items]

    for item in all_items_bin_1:
        bin_1.removeItem(Instance.items_Data[item])

    for item in all_items_bin_2:
        bin_2.removeItem(Instance.items_Data[item])

    for item in all_items_bin_1:
        bin_2.addItem(Instance.items_Data[item])

    for item in all_items_bin_2:
        bin_1.addItem(Instance.items_Data[item])



def swap_bins(solution, alhpa=0.6):

    random_bins = random.sample(solution.bins, int(len(solution.bins) * alhpa))

    if len(random_bins) == 1:
        return solution
    
    itens_removed_from_bins = []

    for i in range(0, len(random_bins) - 1):

        bin_1 = random_bins[i]
        bin_2 = random_bins[i+1]

        swap_all_itens(bin_1, bin_2)

        while True:
            invalid_capacity = False
            
            for j, capacity in enumerate(Instance.bins_Data[bin_1.type].capacity):
                if capacity < bin_1.weight[j]:
                    invalid_capacity = True

            if invalid_capacity:
                item = random.choice(bin_1.items)
                bin_1.removeItem(Instance.items_Data[item])
                itens_removed_from_bins.append(item)
            else:
                break

        while True:
            invalid_capacity = False
            
            for j, capacity in enumerate(Instance.bins_Data[bin_2.type].capacity):
                if capacity < bin_2.weight[j]:
                    invalid_capacity = True

            if invalid_capacity:
                item = random.choice(bin_2.items)
                bin_2.removeItem(Instance.items_Data[item])
                itens_removed_from_bins.append(item)
            else:
                break

    for item in itens_removed_from_bins:

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
        

        new_bin = Bin(best_type)
        new_bin.addItem(item)
        j_to_set = -1

        for j in range(len(solution.bins)):
            if solution.bins[j].id == -1:
                solution.bins[j] = new_bin
                j_to_set = j
                break
        
        solution.items[item.id].setBinBeforeCalc(j_to_set)

    solution = construction(solution)
    solution.calculateInfo()

    return solution

