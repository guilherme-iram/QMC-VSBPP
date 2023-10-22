from Instance import *
from collections import namedtuple, defaultdict

jointCost = namedtuple('jointCost', ['id', 'cost'])

def default_factory():
    return 0

def instance_reader(path, verbose=False):

    with open(path, 'r') as f:
        inst = f.read()

    InstanceN = None
    n = None
    m = None
    d = None
    _type = None
    
    first_line = inst.split('\n')[0]

    for j, element in enumerate(first_line.split(',')):
        if j == 0:
            InstanceN = int(element.split('=')[1])
        if 'n=' in element:
            n = int(element.split('=')[1])
        elif 'm=' in element:
            m = int(element.split('=')[1])
        elif 'd=' in element:
            d = int(element.split('=')[1])
        elif 'type=' in element:
            _type = element.split('=')[1]

    # print(InstanceN, n, m, d, _type)
    Instance.id = InstanceN
    Instance.n = n
    Instance.m = m
    Instance.d = d
    Instance._type = _type
    if verbose:
        print(Instance, '\n')

    # ------------------- BINS -------------------

    bins_type_list = []

    bins = inst.split('BinType:')
    bins = bins[1:]

    for bin_ in bins[:-1]: 

        bin_lines = bin_.split('\n')
        type_bin, cost_bin = bin_lines[0].split(' ')

        type_bin = int(type_bin)
        cost_bin = int(cost_bin.split('=')[1])

        values = []

        for line in bin_lines:
            if "value" in line:
                values.append(int(line.split('=')[-1]))

        bin_type = BinTypeData(type_bin, cost_bin, values)
        bins_type_list.append(bin_type)

    # OBS: O último bin não tem o 'Item:' no final
    bin_lines = bins[-1].split('Item:')[0].split('\n')

    values = []

    for j, line in enumerate(bin_lines[:-1]):
        if j == 0:
            type_bin, cost_bin = line.split(' ')
            type_bin = int(type_bin)
            cost_bin = int(cost_bin.split('=')[1])
        else:
            values.append(int(line.split('=')[-1]))
    
    bin_type = BinTypeData(type_bin, cost_bin, values)
    bins_type_list.append(bin_type)


    Instance._bins = bins_type_list
    if verbose:
        for bin_ in Instance._bins:
            print(bin_)
        print()

    # ------------------- ITEMS ------------------- 

    items_type_list = []

    items = inst.split('Item: no=')
    items[-1] = items[-1].split('Links between items')[0]
    
    for j, item in enumerate(items[1:]):
        # print(item)
        item_lines = item.split('\n')

        if j == len(items[1:])-1:
            item_lines = item_lines[:-1]

            

        id_item = int(item_lines[0].split(' ')[0])
        values = []

        for line in item_lines[1:]:
            if "=" in line:
                values.append(int(line.split('=')[-1]))
        
        item_type = ItemData(id_item, values)
        items_type_list.append(item_type)
        if verbose:
            print(item_type)
                
    Instance._items = items_type_list

    if verbose:
        for item in Instance._items:
            print(item)
        print()

    # ------------------- LINKS -------------------

    linked_items = inst.split("Links between items")
    linked_items = linked_items[1:]
    links = []

    for linked in linked_items[0].split('\n')[1:-1]:

        linked_line = linked.split(' ')
        for i, element in enumerate(linked_line):
            if 'itemNo1' in element:
                itemNo1 = int(element.split('=')[1].strip(','))
            
            elif 'itemNo2' in element:
                itemNo2 = int(element.split('=')[1].strip(','))

            elif 'cost' in element:
                cost = int(element.split('=')[1])
        
        links.append((itemNo1, itemNo2, cost))

        Instance._items[itemNo1-1].linked_Ids.append(itemNo2)

        Instance._items[itemNo1-1].linked_items.append(jointCost(itemNo2, cost))

    
    Instance._linked_items = links

    if verbose:
        for i, link in enumerate(Instance._linked_items):
            print(f"Link {i+1}: {link}")
    
    
    Instance.items_Data = InstanceList(Instance._items)
    Instance.bins_Data = InstanceList(Instance._bins)

    Instance.linked_items_Matrix = InstanceList()
    

    for i in range(1, Instance.n + 1):
        j_costs = defaultdict(default_factory)
        for link in Instance._linked_items:
            if link[0] == i:
                j_costs[link[1]] = link[2]
        
        Instance.linked_items_Matrix.append(j_costs)
                



