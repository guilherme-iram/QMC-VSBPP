from Instance import *
from copy import deepcopy
import sys

epsilon = sys.float_info.epsilon

'''
Breve expçicação:
A ideia aqui é que esses 4 vetores de tamanho n em cada bin permitam fazer as operações da busca local de forma eficiente.
Perceba que a busca só minimiza jointCost e é, de fato, a coisa mais trabalhosa de lidar no código.

Conceitualmente, os vetores de Active e Inactive Joint Cost são os custos conjuntos totais do item i 
associados à solução. Pense que cada item é adicionado no bin com seu custo conjunto total "no máximo" (active joint cost == totalJointCost do item)
sempre que esse custo é diminuído, ele é adicionado no vetor de inactive joint cost. 

Somando os dois para cada item, voltaríamos ao custo conjunto total do item i.

Para a solução só conta o activeCost.

No entanto, é válido fazer a observação de que esse dado, simplesmente, não permite que a gente faça as avaliações em O(1).

Além de saber o quanto a presença de outros items no bin j interferem no custo conjunto do item i, 
é necessário saber o quanto a presença do item i interfere no custo conjunto dos outros itens.

Para isso, temos os vetores de increaseAssociated e decreaseAssociated.

No caso, increaseAssociated mede o custo de NÃO ter o item i no bin j, enquanto decreaseAssociated 
mede a melhoria no custo de ter o item i no bin j.

Digamos que queremos mover um item i pertencente ao bin j para o bin j'.

A sacada aqui é que atualizar o custo conjunto da solução movendo um item de um bin para outro consiste em:

1)  Somar decreaseAssociated[i] do bin j que  no custo conjunto da solução; (somar o custo dele não estar mais no bin j)
2)  Subtrair increaseAssociated[i] do bin j' no custo conjunto da solução; (subtrair o custo dele não estar no bin j')
3)  Somar o inactiveJointCost[i] do item i no bin j no custo conjunto da solução; (somar de volta o que o bin j tirava dele)
4)  Subtrair o activeJointCost[i] do item i no bin j no custo conjunto da solução; (subtrair o que o bin j tirava dele)

'''

class Bin:
    def __init__(self) -> None:
        self.type = -1
        self.items = []
        self.dimensions = [0 for _ in range(Instance.d)] # capacidade utilizada em cada dimensão
        self.activeJointCost = [0 for _ in range(Instance.n)]
        self.inactiveJointCost = [0 for _ in range(Instance.n)]
        self.increaseAssociated = [0 for _ in range(Instance.n)]
        self.decreaseAssociated = [0 for _ in range(Instance.n)]
        self.totalJointCost = 0

    def __str__(self) -> str:
        a_str = f"Bin type: {self.type}\n"
        a_str += f"Bin Cost: {Instance.binsData[self.type].cost}\n"
        a_str += f"Total Joint Cost: {self.totalJointCost}\n"
        a_str += f"Items: {self.items}\n"
        a_str += f"Dimensions: {self.dimensions}\n"
        a_str += f'Active joint cost: {self.activeJointCost}\n' # custo conjunto total do item i que não foi subtraído
        a_str += f'Inactive joint cost: {self.inactiveJointCost}\n' # custo conjunto total do item i que foi subtraído
        a_str += f"Associated Increase: {self.increaseAssociated}\n" # custo que i adicionou em outros itens
        a_str += f"Associated Decrease: {self.decreaseAssociated}\n\n" # custo que i subrtraiu de outros itens
        a_str += f"Total Increase: {sum(self.increaseAssociated)}\n"
        a_str += f"Total Decrease: {sum(self.decreaseAssociated)}\n"


        return a_str

    def __repr__(self) -> str:
        return self.__str__()
    
    def __getitem__(self, index):
        return self.items[index]

    def addItem(self, item:int):
        self.items.append(item)
        #self.totalJointCost -= self.increaseAssociated[item]
        #self.increaseAssociated[item] = 0
        for dim in range(Instance.d):
            self.dimensions[dim] += Instance.itemsData[item].dimensions[dim]
    
    def removeItem(self, item:int):
        self.items.remove(item)
        #self.totalJointCost += self.decreaseAssociated[item]
        for dim in range(Instance.d):
            self.dimensions[dim] -= Instance.itemsData[item].dimensions[dim]

    def canAddItem(self, item:int):
        for dim in range(Instance.d):
            if self.dimensions[dim] + Instance.itemsData[item].dimensions[dim] > Instance.binsData[self.type].dimensions[dim]:
                return False
        return True
    def canSwapItems(self, item:int, other:int):
        for dim in range(Instance.d):
            if self.dimensions[dim] + Instance.itemsData[other].dimensions[dim] - Instance.itemsData[item].dimensions[dim] > Instance.binsData[self.type].dimensions[dim]:
                return False
        return True
    def __len__(self):
        return len(self.items)
    
    def resetCost(self):
        self.totalJointCost = 0
        self.increaseAssociated = [0 for _ in range(Instance.n)]
        self.decreaseAssociated = [0 for _ in range(Instance.n)]
        self.activeJointCost = [0 for _ in range(Instance.n)]
        self.inactiveJointCost = [0 for _ in range(Instance.n)]



        
class Solution:
    def __init__(self) -> None:
        self.itemsBin = [-1 for _ in range(Instance.n)] # relaciona em qual bin o item está
        self.cost = 0
        self.bins = []
    
    def __str__(self) -> str:
        a_str = f"Solution cost: {self.cost}\n"
        a_str += f"Items bin: {self.itemsBin}\n"
        a_str += f"Bins:\n"
        for bin in self.bins:
            a_str += f"{bin}\n"
        return a_str

    def __repr__(self) -> str:
        return self.__str__()
    



    def copy(self, other) -> None:
        self.itemsBin = deepcopy(other.itemsBin)
        self.cost = other.cost
        self.bins = deepcopy(other.bins)
    
    def mergeBins(self, j1:int, j2:int, best_k:int, merge_joint_cost:int)-> None:
            #self.bins[j1].decreaseAssociated[item] = self.bins[j1].increaseAssociated[item]
            #self.bins[j1].increaseAssociated[item] = 0
        
        for i in range(len(Instance.itemsData)):
            if self.itemsBin[i] != j1:
                self.bins[j1].increaseAssociated[i] += self.bins[j2].increaseAssociated[i]
            else:
                #self.bins[j1].increaseAssociated[i] += self.bins[j2].increaseAssociated[i]
                self.bins[j1].increaseAssociated[i] = 0
                self.bins[j1].decreaseAssociated[i] += self.bins[j2].increaseAssociated[i]

        
        for item in self.bins[j2].items:
            self.itemsBin[item] = j1
            self.bins[j1].addItem(item)
        
    
            

                

        self.cost -= self.bins[j1].totalJointCost
        self.cost -= Instance.binsData[self.bins[j1].type].cost
        self.cost -= self.bins[j2].totalJointCost
        self.cost -= Instance.binsData[self.bins[j2].type].cost

        self.cost += Instance.binsData[best_k].cost
        self.cost += merge_joint_cost
        
        self.bins[j1].type = best_k
        self.bins[j1].totalJointCost = merge_joint_cost
        
        
        self.bins.remove(self.bins[j2])


        for bin in self.bins[j2:]:
            for item in bin.items:
                self.itemsBin[item] -= 1

    def calculateInfo(self):
        self.cost = 0

        for index in range(len(self.bins)):
            self.bins[index].resetCost()

            for it in range(len(self.bins[index])):
                self.itemsBin[self.bins[index][it]] = index
        
        for item in range(len(self.itemsBin)):
            if self.itemsBin[item] == -1:
                raise Exception("Item not in bin")
            
            self.bins[self.itemsBin[item]].activeJointCost[item] += Instance.itemsData[item].totalJointCost
            for dependentIndex in range(len(Instance.itemsData[item].links)):
                
                dependentId = Instance.itemsData[item].links[dependentIndex]
                if self.itemsBin[dependentId] == self.itemsBin[item]:
                    self.bins[self.itemsBin[item]].decreaseAssociated[dependentId] += Instance.linkMatrix[item][dependentId]
                    self.bins[self.itemsBin[item]].activeJointCost[item] -= Instance.linkMatrix[item][dependentId]
                    self.bins[self.itemsBin[item]].inactiveJointCost[item] += Instance.linkMatrix[item][dependentId]
                else:
                    self.bins[self.itemsBin[item]].increaseAssociated[dependentId] += Instance.linkMatrix[item][dependentId]
                    
            
            self.bins[self.itemsBin[item]].totalJointCost += self.bins[self.itemsBin[item]].activeJointCost[item]
        
        for bin in self.bins:
            self.cost += bin.totalJointCost
            self.cost += Instance.binsData[bin.type].cost
        

            
    
    def evaluateMigrateItem(self, i:int, j:int)->float: # sendo i o item a ser migrado e j o bin para onde ele vai (CALCULA O NOVO CUSTO)
        new_cost = self.cost
        
        new_cost += self.bins[self.itemsBin[i]].decreaseAssociated[i]
        new_cost -= self.bins[j].increaseAssociated[i]
        new_cost -= self.bins[self.itemsBin[i]].activeJointCost[i]
        new_cost += self.bins[j].activeJointCost[i]

        if (len(self.bins[self.itemsBin[i]]) == 1):
            new_cost -= Instance.binsData[self.bins[self.itemsBin[i]].type].cost

        test = Solution()
        test.copy(self)
        
        test.bins[test.itemsBin[i]].removeItem(i)
        test.bins[j].addItem(i)
        test.itemsBin[i] = j
        test.calculateInfo()

        if abs(test.cost - new_cost) > epsilon:
            print(f'new_cost: {new_cost}, test.cost: {test.cost}')
            print('current solution: ')
            print(self.bins[self.itemsBin[i]])
            print(self.bins[j])
            print('test solution: ')
            print(test.bins[self.itemsBin[i]])
            print(test.bins[j])
            raise Exception("Error in migrate item evaluation")
        return new_cost
    
    def migrateItem(self, i:int, j:int)-> None: # sendo i o item a ser migrado e j o bin para onde ele vai (ATUALIZA A ESTRUTURA)

        self.cost = self.evaluateMigrateItem(i, j)

        self.bins[j].totalJointCost -= self.bins[j].increaseAssociated[i]

        self.bins[self.itemsBin[i]].totalJointCost += self.bins[self.itemsBin[i]].decreaseAssociated[i]

        self.bins[j].decreaseAssociated[i] = self.bins[j].increaseAssociated[i]
        self.bins[j].increaseAssociated[i] = 0
        self.bins[self.itemsBin[i]].increaseAssociated[i] = self.bins[self.itemsBin[i]].decreaseAssociated[i]
        self.bins[self.itemsBin[i]].decreaseAssociated[i] = 0

        

        if (len(self.bins[self.itemsBin[i]]) == 0):
            for item in self.bins[self.itemsBin[i] + 1:]:
                self.itemsBin[item] -= 1
            self.bins.remove(self.bins[self.itemsBin[i]])
        else:
            self.bins[self.itemsBin[i]].removeItem(i)

        self.bins[j].addItem(i)
        
        
        self.itemsBin[i] = j


    def evaluateSwapItems(self, i:int, j:int)->float: # sendo i e j os itens a serem trocados de caixa (CALCULA O NOVO CUSTO)
        new_cost = self.cost

        new_cost += self.bins[self.itemsBin[i]].decreaseAssociated[i]
        new_cost += self.bins[self.itemsBin[j]].decreaseAssociated[j]

        new_cost -= self.bins[self.itemsBin[i]].increaseAssociated[j]
        new_cost -= self.bins[self.itemsBin[j]].increaseAssociated[i]

        return new_cost

    def swapItems(self, i:int, j:int)-> None: # sendo i e j os itens a serem trocados de caixa (ATUALIZA A ESTRUTURA)
        self.cost = self.evaluateSwapItems(i, j)

        self.bins[self.itemsBin[i]].totalJointCost += self.bins[self.itemsBin[i]].decreaseAssociated[i]
        self.bins[self.itemsBin[j]].totalJointCost += self.bins[self.itemsBin[j]].decreaseAssociated[j]


        self.bins[self.itemsBin[i]].totalJointCost -= self.bins[self.itemsBin[i]].increaseAssociated[j]
        self.bins[self.itemsBin[j]].totalJointCost -= self.bins[self.itemsBin[j]].increaseAssociated[i]


        bin_i = self.itemsBin[i]
        bin_j = self.itemsBin[j]

        
        self.bins[bin_i].increaseAssociated[i] = self.bins[bin_i].decreaseAssociated[i]
        self.bins[bin_j].increaseAssociated[j] = self.bins[bin_j].decreaseAssociated[j]

        self.bins[bin_i].decreaseAssociated[i] = 0
        self.bins[bin_j].decreaseAssociated[j] = 0


        self.bins[bin_i].decreaseAssociated[j] = self.bins[bin_i].increaseAssociated[j]
        self.bins[bin_j].decreaseAssociated[i] = self.bins[bin_j].increaseAssociated[i]

        self.bins[bin_i].increaseAssociated[j] = 0
        self.bins[bin_j].increaseAssociated[i] = 0

        self.bins[self.itemsBin[i]].removeItem(i)
        self.bins[self.itemsBin[j]].removeItem(j)

        self.bins[self.itemsBin[i]].addItem(j)
        self.bins[self.itemsBin[j]].addItem(i)

        self.itemsBin[i] = bin_j
        self.itemsBin[j] = bin_i
    

