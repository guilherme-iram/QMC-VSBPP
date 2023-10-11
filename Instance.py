class Instance:

    def __init__(self, id, n, m, d, _type):
        self.id = id
        self.n = n
        self.m = m
        self.d = d
        self._type = _type

        self.items = []
        self.bins = []
        self.linked_items = []

    def __str__(self):
        return f"instance={self.id}_n={self.n}_m={self.m}_d={self.d}_type={self._type}"

class Bin:

    def __init__(self, id, cost, values):
            self.id = id
            self.cost = cost
            self.capacity = [value for value in values if value > 0]

    def __str__(self):
        return f"Bin {self.id} with cost {self.cost} and capacity {self.capacity}"

class Item:

    def __init__(self, id, values):
        self.id = id
        self.weight = [value for value in values if value > 0] 

    def __str__(self):
        return f"Item {self.id} with weight {self.weight}"


