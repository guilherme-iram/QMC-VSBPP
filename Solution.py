from Instance import *
from copy import deepcopy

class Item:
    def __init__(self, id = -1, nOfDependentItems = 0, jointCost = 0) -> None:
        self.id = id
        self.nOfDependentItems = nOfDependentItems
        self.binId = -1 # id do bin que o item está
        self.dependentItems = [-1 for _ in range(nOfDependentItems)] # lista de itens dependentes. O valor é 1 se o item dependente 
                                                                    # está em um bin diferente do item principal, e 0 caso contrário
        self.jointCost = 0 # soma do custo conjunto de todos os itens dependentes

    def __str__(self) -> str:
        a_str =  f"Item {self.id}: weight {self.getWeight()}, in bin {self.binId}, jointCost {self.jointCost}\n"
        a_str += f"Dependent items: {self.dependentItems}\n"
        return a_str

    def __repr__(self) -> str:
        return self.__str__()
    
    def getData(self): # retorna o objeto ItemData correspondente ao item
        return Instance.items_Data[self.id]
    
    def getWeight(self):
        return Instance.items_Data[self.id].weight
    
    def linkedIds(self): # retorna a lista de itens dependentes
        return Instance.items_Data[self.id].linked_Ids

    def setBinBeforeCalc(self, binId):
        self.binId = binId                  # a razão desta função existir é que, ao criar uma primeira solução, é necessário definir o bin de cada item
                                            # para poder calcular o custo conjunto de cada item. Considerando que este é um VNS, é interessante que apenas
                                            # a solução inicial seja criada com esta função, e que as demais soluções sejam criadas com esta função e as demais 
                                            # sejam atualizadas por setBin da classe Solution. (cabe revisão e melhrorias naquela função)
    
    def updateJointCost(self):
        self.jointCost = 0
        for i in range(self.nOfDependentItems):
            dependentId = Instance.items_Data[self.id].linked_Ids[i]
            self.jointCost += self.dependentItems[i] * Instance.linked_items_Matrix[self.id][dependentId]


class Bin:
    
    static_id = 0

    def __init__(self, type:int = -1) -> None:

        Bin.static_id += 1
        self.id = Bin.static_id

        self.type = type
        if type == -1:
            self.cost = 0
        else:
            self.cost = Instance.bins_Data[type].cost
        self.jointCost = 0
        self.items = []
        self.weight = [0 for _ in range(Instance.d)]
    
    def __str__(self) -> str:
        a_str =  f"Bin Type {self.type}, cost {self.cost}, jointCost {self.jointCost} "
        a_str += f"Items: {self.items}\n"
        return a_str
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __getitem__(self, key):     # retorna o id do item na posição na posição key do bin
        return self.items[key]
    
    def __len__(self):          # retorna o número de itens no bin len(bin)
        return len(self.items)
    
    def __iter__(self):
        return iter(self.items) # para fazer for item in bin:
    
    def copy(self):
        return deepcopy(self)
    
    def resetCost(self):
        self.cost = Instance.bins_Data[self.type].cost
        self.jointCost = 0

    def changeType(self, newType):
        self.type = newType
        self.cost = Instance.bins_Data[self.type].cost
    
    def addItem(self, item):

        self.items.append(item.id)
        
        for d in range(Instance.d):
            self.weight[d] += Instance.items_Data[item.id].weight[d]

    def removeItem(self, item):
        self.items.remove(item.id)
        
        for d in range(Instance.d):
            self.weight[d] -= Instance.items_Data[item.id].weight[d]

# Sempre se altera o jointCost a partir da classe solution e vai atribuindo para as classes menores
class Solution:
    def __init__(self) -> None:
        self.bins = [Bin() for _ in range(Instance.n)]
        self.bins = InstanceList(self.bins)
        self.items = [Item(itemData.id, len(itemData.linked_Ids)) for itemData in Instance.items_Data]
        self.items = InstanceList(self.items)
        self.cost = 0
        
    
    def __str__(self) -> str:
        a_str =  f"Solution: cost {self.cost}\n"
        for bin in self.bins:
            a_str += f"{bin}"

        return a_str
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __getitem__(self, key):     # retorna o bin na posição key da solução
        return self.bins[key]
    
    def calculateInfo(self):

        self.cost = 0

        for bin in self.bins:
            bin.resetCost()

        for item in self.items:
            if item.binId == -1:
                raise Exception("Item not in bin")
            
            item.jointCost = 0

            for dependentIndex in range(item.nOfDependentItems):
                
                dependentId = Instance.items_Data[item.id].linked_Ids[dependentIndex]
                item.dependentItems[dependentIndex] = 1 if self.items[dependentId].binId != item.binId else 0
                item.jointCost += item.dependentItems[dependentIndex] * Instance.linked_items_Matrix[item.id][dependentId]
            
            self.bins[item.binId].jointCost += item.jointCost
        
        self.cost = sum([bin.cost for bin in self.bins]) + sum([bin.jointCost for bin in self.bins])


    def copy(self, other):
        self = deepcopy(other)


    def merge(self, j1:int, j2:int, best_k:int):

        for item in self.bins[j2]:
            self.items[item].binId = j1
            self.bins[j1].addItem(self.items[item])

        self.bins[j1].type = best_k
        self.bins.remove(self.bins[j2])

        for i in (range(j2, len(self.bins) + 1)):
            for iter in range(len(self.bins[i])):
                self.items[self.bins[i][iter]].binId -= 1
        
        self.calculateInfo()
        


    

        
            

    


        



    



