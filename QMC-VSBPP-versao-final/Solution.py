from Instance import *
from copy import deepcopy
import sys

epsilon = sys.float_info.epsilon



class Bin:
    def __init__(self) -> None:
        self.type = -1
        self.items = []
        self.dimensions = [0 for _ in range(Instance.d)] # capacidade utilizada em cada dimensão
       
        self.totalJointCost = 0

    def __str__(self) -> str:
        a_str = f"Bin type: {self.type}\n"
        a_str += f"Bin Cost: {Instance.binsData[self.type].cost}\n"
        a_str += f"Total Joint Cost: {self.totalJointCost}\n"
        a_str += f"Items: {self.items}\n"
        a_str += f"Dimensions: {self.dimensions}\n"
        


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
    
    def calculateInfo(self):
        self.cost = 0

        for index in range(len(self.bins)):
            self.bins[index].resetCost()

            for it in range(len(self.bins[index])):
                self.itemsBin[self.bins[index][it]] = index
            
            

        for item in range(Instance.n):
            if self.itemsBin[item] == -1:
                raise Exception("Item not in bin")
            

            for dependentIndex in range(len(Instance.itemsData[item].links)):
                
                dependentId = Instance.itemsData[item].links[dependentIndex]
                
                if self.itemsBin[dependentId] != self.itemsBin[item]:
                    self.bins[self.itemsBin[item]].totalJointCost += Instance.linkMatrix[item][dependentId]
            
        
        for bin in self.bins:
            self.cost += Instance.binsData[bin.type].cost + bin.totalJointCost
        

    
    def mergeBins(self, j1:int, j2:int, best_k:int):
        for item in self.bins[j2]:
            self.itemsBin[item] = j1
            self.bins[j1].addItem(item)
        

        self.bins[j1].type = best_k
        self.bins.remove(self.bins[j2])

        for bin in self.bins[j2:]:
            for item in bin.items:
                self.itemsBin[item] -=1
        
        

        self.calculateInfo()