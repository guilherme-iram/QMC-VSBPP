class Instance:
    id = -1
    n = -1
    m = -1
    d = -1
    type = -1

    items = []
    bins = []
    linked_items = []
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
        self.linked_items = []

    def __str__(self):
        a_str =  f"Item {self.id} with weight {self.weight}\n"

        for item in self.linked_items:
            a_str += f" joinCost to item {item.id} is {item.cost}\n"
        
        return a_str


