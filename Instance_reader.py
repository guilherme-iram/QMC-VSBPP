from Instance import *

def instance_reader(path):

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
    my_instance = Instance(InstanceN, n, m, d, _type)
    print(my_instance, '\n')

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

        bin_type = Bin(type_bin, cost_bin, values)
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
    
    bin_type = Bin(type_bin, cost_bin, values)
    bins_type_list.append(bin_type)


    my_instance.bins = bins_type_list

    for bin_ in my_instance.bins:
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
        
        item_type = Item(id_item, values)
        items_type_list.append(item_type)
        # print(item_type)
                
    my_instance.items = items_type_list

    for item in my_instance.items:
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
    
    my_instance.linked_items = links

    for i, link in enumerate(my_instance.linked_items):
        print(f"Link {i+1}: {link}")

    return my_instance


