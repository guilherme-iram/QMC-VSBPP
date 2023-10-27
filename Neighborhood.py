from Solution import *
from Instance import *
import random
from Construction import * 

from collections import namedtuple

class Node:

    def __init__(self, items:list, cost:float = float('inf'), bin_type = -1) -> None:
        self.items = items
        self.cost = cost
        self.bin_type = bin_type
    
    def __str__(self) -> str:
        return f"Items: {self.items} Cost: {self.cost} BinType: {self.bin_type}"
    
    def __repr__(self) -> str:
        return f"Items: {self.items} Cost: {self.cost} BinType: {self.bin_type}"
        
# random.seed(42)

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
    
    # print("Totla de itens removidos: ", len(itens_removed_from_bins))
    for item in itens_removed_from_bins:

        lowest_cost = float('inf')
        best_type = -1
        
        for type in Instance.bins_Data:

            if type.cost < lowest_cost:
                available_capacity = True
                for dim in range(Instance.d):
                        if Instance.items_Data[item].weight[dim] > type.capacity[dim]:
                             available_capacity = False
                             break
                
                if available_capacity:
                    lowest_cost = type.cost
                    best_type = type.id
        

        new_bin = Bin(best_type)
        new_bin.addItem(Instance.items_Data[item])
        solution.bins.append(new_bin)

        solution.items[Instance.items_Data[item].id].setBinBeforeCalc(len(solution.bins))

    construction(solution)
    solution.calculateInfo()

    return solution


def delete_bins(solution, betha=0.5):

    random_bins = random.sample(solution.bins, int(len(solution.bins) * betha))

    if len(random_bins) == 1:
        return solution
    
    itens_removed_from_bins = []

    for i in range(len(random_bins)):

        for item in random_bins[i].items:
            itens_removed_from_bins.append(item)
        
        solution.bins.remove(random_bins[i])

    # rint("Totla de itens removidos: ", len(itens_removed_from_bins))
    
    for item in itens_removed_from_bins:

        lowest_cost = float('inf')
        best_type = -1
        
        for type in Instance.bins_Data:

            if type.cost < lowest_cost:
                available_capacity = True
                for dim in range(Instance.d):
                        if Instance.items_Data[item].weight[dim] > type.capacity[dim]:
                             available_capacity = False
                             break
                
                if available_capacity:
                    lowest_cost = type.cost
                    best_type = type.id
        

        new_bin = Bin(best_type)
        new_bin.addItem(Instance.items_Data[item])
        solution.bins.append(new_bin)

        solution.items[Instance.items_Data[item].id].setBinBeforeCalc(len(solution.bins))

    construction(solution)
    solution.calculateInfo()

    return solution


def buildAcyclicGraph(solution:Solution):
    
    sequenced_items = []

    for bin in solution.bins:
        for item in bin:
            sequenced_items.append(item)


    acyclic_digraph = []
    
    for i in range(len(sequenced_items)):
        set_of_items = []
        line = []
        jointCost = Instance.items_Data[sequenced_items[i]].totalJointCost # começa o jointCost com o custo total do item i
        
        dimensions = [weight for weight in Instance.items_Data[sequenced_items[i]].weight] # começa as dimensões com as dimensões do item i

        for j in range(len(sequenced_items)):
            if j == i:
                set_of_items.append(sequenced_items[j])
                node = Node(items=deepcopy(set_of_items))
                
                lowest_cost = float('inf')
                available_capacity = False
                best_type = -1                                      # infere o tipo mais barato que cabe o item i
                for type in Instance.bins_Data:
                    if type.cost < lowest_cost:
                        available_capacity = True
                        for dim in range(Instance.d):
                                if dimensions[dim] > type.capacity[dim]:
                                    available_capacity = False
                                    break
                        
                        if available_capacity:
                            lowest_cost = type.cost
                            best_type = type.id
                
                node.cost = jointCost + lowest_cost
                node.bin_type = best_type

                line.append(node)




            elif j > i:
                jointCost += Instance.items_Data[sequenced_items[j]].totalJointCost # soma o jointCost total do item j ao jointCost

                for (it, item) in enumerate(set_of_items):
                    jointCost -= Instance.linked_items_Matrix[sequenced_items[j]][item] # subtrai o jointCost do item j com todos os itens que já estão no conjunto

                for (it, item) in enumerate(set_of_items):
                    jointCost -= Instance.linked_items_Matrix[item][sequenced_items[j]] # subtrai o jointCost de todos os itens que já estão no conjunto com o item j

                set_of_items.append(sequenced_items[j])
                
                node = Node(items=deepcopy(set_of_items))
                
                for dim in range(Instance.d):
                    dimensions[dim] += Instance.items_Data[sequenced_items[j]].weight[dim] # soma as dimensões do item j com as dimensões do conjunto
                
                lowest_cost = float('inf')
                available_capacity = False
                best_type = -1
                for type in Instance.bins_Data:
                    if type.cost < lowest_cost:
                        available_capacity = True
                        for dim in range(Instance.d):
                                if dimensions[dim] > type.capacity[dim]:
                                    available_capacity = False
                                    break
                        
                        if available_capacity:
                            lowest_cost = type.cost
                            best_type = type.id
                
                if best_type == -1:
                    for k in range(j, len(sequenced_items)):
                        node = Node(items=[-1])                 # se não for mais possível achar um bin que comporte os itens
                        line.append(node)                       # invalida todos os nós restantes da linha
                    
                    break
                
                node.cost = jointCost + lowest_cost
                node.bin_type = best_type

                line.append(node)

            else:
                line.append(Node(items=[-1])) # transforma o itens atrás do item i em um nó inválido de custo infinito
        
        set_of_items.append(0)                              # faz uma cópia do nó anterior e adiciona o nó 0 (nó final)

        node = Node(items=deepcopy(set_of_items))

        node.cost = line[len(sequenced_items) - 1].cost  

        node.bin_type = line[len(sequenced_items) - 1].bin_type



        line.append(node)                   # linha completa (lista de nós)

        acyclic_digraph.append(line)        # grafo acíclico completo (lista de linhas)
    

    return acyclic_digraph

