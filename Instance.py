from collections import UserList
from typing import Iterator
import sys

epsilon = sys.float_info.epsilon

class CustomListIterator:
    def __init__(self, custom_list):
        self.custom_list = custom_list
        self.index = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.custom_list) + 1:
            result = self.custom_list[self.index]
            self.index += 1
            return result
        raise StopIteration

class InstanceList(UserList):
    def __getitem__(self, key):
        return super().__getitem__(key - 1) # resolve o problema de começar a contagem em 1
    def __setitem__(self, key, value):
        super().__setitem__(key - 1, value)
    def __iter__(self) -> Iterator:
        # this should be like getitem, geting from 1 to n
        return CustomListIterator(self)


class Instance:
    id = -1
    n = -1
    m = -1
    d = -1
    type = -1

    _items = []
    _bins = []
    _linked_items = []

    items_Data = InstanceList()
    bins_Data = InstanceList()

    linked_items_Matrix = InstanceList()
    def __init__(self):
        pass
        
    def __str__(self):
        return f"instance={Instance.id}_n={Instance.n}_m={Instance.m}_d={Instance.d}_type={Instance._type}"

class BinTypeData:

    def __init__(self, id, cost, values):
            self.id = id
            self.cost = cost
            self.capacity = [value for value in values if value > 0]

    def __str__(self):
        return f"Bin {self.id} with cost {self.cost} and capacity {self.capacity}"
    


class ItemData:

    def __init__(self, id, values):
        self.id = id
        self.weight = [value for value in values if value > 0] 
        self.linked_Ids = []
        self.linked_items = []

    def __str__(self):
        a_str =  f"Item {self.id} with weight {self.weight}\n"

        for item in self.linked_items:
            a_str += f" joinCost to item {item.id} is {item.cost}\n"
        
        return a_str



