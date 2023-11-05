from Construction import *
from copy import deepcopy

class Node:

    def __init__(self, items:list, cost:float = float('inf'), bin_type = -1) -> None:
        self.items = items
        self.cost = cost
        self.bin_type = bin_type
    
    def __str__(self) -> str:
        return f"Items: {self.items} Cost: {self.cost} BinType: {self.bin_type}"
    
    def __repr__(self) -> str:
        return f"Items: {self.items} Cost: {self.cost} BinType: {self.bin_type}"
    


def buildAcyclicGraph(solution:Solution):
    
    sequenced_items = []

    for bin in solution.bins:
        for item in bin:
            sequenced_items.append(item)


    acyclic_digraph = []

    for i in range(len(sequenced_items)):
        set_of_items = []
        line = []
        jointCost = Instance.itemsData[sequenced_items[i]].totalJointCost # começa o jointCost com o custo total do item i
        
        dimensions = [weight for weight in Instance.itemsData[sequenced_items[i]].dimensions] # começa as dimensões com as dimensões do item i

        for j in range(len(sequenced_items)):
                if j == i:
                    set_of_items.append(sequenced_items[j])
                    node = Node(items=deepcopy(set_of_items))
                    
                    lowest_cost = float('inf')
                    available_capacity = False
                    best_type = -1                                      # infere o tipo mais barato que cabe o item i
                    for type in Instance.binsData:
                        if type.cost < lowest_cost:
                            available_capacity = True
                            for dim in range(Instance.d):
                                    if dimensions[dim] > type.dimensions[dim]:
                                        available_capacity = False
                                        break
                            
                            if available_capacity:
                                lowest_cost = type.cost
                                best_type = type.id
                                break # considerando que os tipos estão ordenados por custo, o primeiro que couber é o melhor
                    
                    node.cost = jointCost + lowest_cost
                    node.bin_type = best_type

                    line.append(node)


                elif j > i:
                    jointCost += Instance.itemsData[sequenced_items[j]].totalJointCost # soma o jointCost total do item j ao jointCost

                    for (it, item) in enumerate(set_of_items):
                        jointCost -= Instance.linkMatrix[sequenced_items[j]][item] # subtrai o jointCost do item j com todos os itens que já estão no conjunto

                    for (it, item) in enumerate(set_of_items):
                        jointCost -= Instance.linkMatrix[item][sequenced_items[j]] # subtrai o jointCost de todos os itens que já estão no conjunto com o item j

                    set_of_items.append(sequenced_items[j])
                    
                    node = Node(items=deepcopy(set_of_items))
                    
                    for dim in range(Instance.d):
                        dimensions[dim] += Instance.itemsData[sequenced_items[j]].dimensions[dim] # soma as dimensões do item j com as dimensões do conjunto
                    
                    lowest_cost = float('inf')
                    available_capacity = False
                    best_type = -1
                    for type in Instance.binsData:
                        if type.cost < lowest_cost:
                            available_capacity = True
                            for dim in range(Instance.d):
                                    if dimensions[dim] > type.dimensions[dim]:
                                        available_capacity = False
                                        break
                            
                            if available_capacity:
                                lowest_cost = type.cost
                                best_type = type.id
                                break # considerando que os tipos estão ordenados por custo, o primeiro que couber é o melhor
                    
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
            
            

        line.append(node)                   # linha completa (lista de nós)
        line.append(Node(items=[-1], cost= 0))       # nó inválido de custo infinito

        acyclic_digraph.append(line)        # grafo acíclico completo (lista de linhas)


        

    return acyclic_digraph


def dijkstra(graph):
    
    nodes = [[float(), None, i] for i in range(len(graph))]
    nodes[0][0] = 0 # custo
    nodes[0][1] = 0 # pai

    solution_nodes = []

    while len(nodes) > 0:

        nodes = sorted(nodes)
        current_node = nodes.pop(0)
        solution_nodes.append(current_node)

        for i in range(len(nodes)):
            if graph[current_node[2]][nodes[i][2]].cost + current_node[0] < nodes[i][0]:
                nodes[i][0] = graph[current_node[2]][nodes[i][2]].cost + current_node[0]
                nodes[i][1] = current_node[2]

    final_node = solution_nodes[-1]
    arcs = []

    print(final_node)
    while True:
        arcs.append((final_node[1], final_node[2]))
        if final_node[1] == 0:
            break
        final_node = solution_nodes[final_node[1]]
        print(final_node)

    arcs = sorted(arcs)
    print("\n", arcs)
    return arcs

def permutation_shortest_path(solution: Solution):

    graph = buildAcyclicGraph(solution)
    arcs = dijkstra(graph)

    
    new_solution = Solution()

    print(arcs)
   
    
    return new_solution