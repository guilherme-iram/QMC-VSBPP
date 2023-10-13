from Instance import *
from copy import deepcopy

class Item:
    def __init__(self, id = -1, weight = None, nOfDependentItems = 0, jointCost = 0) -> None:
        self.id = id
        self.weight = weight # dimensões do item
        self.nOfDependentItems = nOfDependentItems
        self.binId = -1 # id do bin que o item está
        self.dependentItems = [-1 for _ in range(nOfDependentItems)] # lista de itens dependetes. O valor é 1 se o item dependente 
                                                                    # está em um bin diferente do item principal, e 0 caso contrário
        self.jointCost = 0 # soma do custo conjunto de todos os itens dependentes

    def __str__(self) -> str:
        a_str =  f"Item {self.id}: weight {self.weight}, in bin {self.binId}, jointCost {self.jointCost}\n"
        a_str += f"Dependent items: {self.dependentItems}\n"
        return a_str

    def __repr__(self) -> str:
        return self.__str__()
    
    def setBinBeforeCalc(self, binId):
        self.binId = binId                  # a razão desta função existir é que, ao criar uma primeira solução, é necessário definir o bin de cada item
                                            # para poder calcular o custo conjunto de cada item. Considerando que este é um VNS, é interessante que apenas
                                            # a solução inicial seja criada com esta função, e que as demais soluções sejam criadas com esta função e as demais 
                                            # sejam atualizadas por setBin da classe Solution. (cabe revisão e melhrorias naquela função)
    
    def updateJointCost(self):
        self.jointCost = 0
        for i in range(self.nOfDependentItems):
            self.jointCost += self.dependentItems[i] * Instance.items[self.id - 1].linked_items[i].cost

class B1:
    # Uma lista implementada como vetor.
    def __init__(self, nOfItems = 0) -> None:
        self.used = [-1 for _ in range(nOfItems)]
        self.nextIndex = 0
        self.cost = 0
    
    def add(self, type):
        self.used[self.nextIndex] = type
        self.cost += Instance.bins[type - 1].cost
        self.nextIndex += 1
    
    def remove(self):
        self.nextIndex -= 1
        self.cost -= Instance.bins[self.used[self.nextIndex] - 1].cost
        self.used[self.nextIndex] = -1
    
    def updateCost(self):
        self.cost = 0
        index = 0

        while self.used[index] != -1:
            self.cost += Instance.bins[self.used[index] - 1].cost
            index += 1
            if index >= len(self) :
                break
        
    def __str__(self) -> str:
        return str(self.used)
    
    def __repr__(self) -> str:
        return self.__str__()
    


    def __len__(self):
        return self.nextIndex
    

class Solution:
    def __init__(self) -> None:
        self.bins = B1(0) # define a lista de bins. Caso o bin esteja vazio, o valor é -1. Do contrário, o valor é o tipo do bin
        self.items = None # define a lista de items. 
        #self.jointCostSum = 0 # soma do custo conjunto de todos os itens
        self.cost = 0
    
    def __repr__(self) -> str:
        a_str = f"Solution with cost {self.cost}\n"
        a_str += f"Bins: {self.bins}\n"
        a_str += f"Items: \n{self.items}\n"
        return a_str

    def __str__(self) -> str:
        return self.__repr__()

    def copy(self, other):
        self = deepcopy(other)

    
    def calculateInfo(self):        # função estável
        self.cost = 0
        jointCostSum = 0
        for item in self.items:
            if item.binId == -1:
                raise Exception("Item not in bin")
            
            item.jointCost = 0
            for dependentIndex in range(item.nOfDependentItems):
                item.dependentItems[dependentIndex] = 1 if self.items[Instance.items[item.id - 1].linked_items[dependentIndex].id - 1].binId != item.binId else 0
            
            for dependentIndex in range(item.nOfDependentItems):
                item.jointCost += item.dependentItems[dependentIndex] * Instance.items[item.id - 1].linked_items[dependentIndex].cost
        
            jointCostSum += item.jointCost

        self.bins.updateCost()

        self.cost = self.bins.cost + jointCostSum       


    def updateCost(self):
        self.cost = 0

        for item in self.items:
            self.cost += item.jointCost
        
        self.cost += self.bins.cost

    def setBin(self, itemId, binId): # cabe revisão mantive aqui apenas para ficar a "ideia" mas precisa alterar também quem tinha itemId nos seus itens dependentes
        self.items[itemId - 1].binId = binId
        self.cost -= self.items[itemId - 1].jointCost

        self.items[itemId -1 ].jointCost = 0

        item = self.items[itemId - 1]
        for dependentIndex in range(self.items[itemId - 1].nOfDependentItems):
            self.items[itemId - 1 ].dependentItems[dependentIndex] = 1 if self.items[Instance.items[itemId - 1].linked_items[dependentIndex].id - 1].binId != item.binId else 0
            self.items[itemId - 1].jointCost += self.items[itemId - 1 ].dependentItems[dependentIndex] * Instance.items[itemId - 1].linked_items[dependentIndex].cost


    def __len__(self):
        return len(self.items)


    @classmethod
    def from_Instance(cls):
        cls = Solution()
        cls.bins = B1(len(Instance.items))
        cls.items = [Item(itemData.id, itemData.weight, len(itemData.linked_items)) for itemData in Instance.items]
        cls.cost = 0
        return cls

