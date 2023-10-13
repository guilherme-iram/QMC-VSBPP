from Instance import *

all_datasets = [
    "dataset1(n=25)",
    "dataset2(n=50)",
    "dataset3(n=100)",
    "dataset4(n=200)",
]

for name_dataset in all_datasets:

    all_instances = []

    with open (f'datasets/{name_dataset}.txt') as f:
        txt = f.read()

    instances = txt.split('instance=')
    instances = instances[1:]

    for i, inst in enumerate(instances):
        
        bins_type_list = []

        InstanceN = None
        n = None
        m = None
        d = None
        _type = None
        
        first_line = inst.split('\n')[0]
        
        for j, element in enumerate(first_line.split(',')):
            if j == 0:
                InstanceN = int(element)
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
        print(my_instance)

        # Bins do 0 até m-1
        bins = inst.split('BinType:')
        bins = bins[1:]

        for bin_ in bins[:-1]: 

            bin_lines = bin_.split('\n')
            type_bin, cost_bin = bin_lines[0].split(' ')
            type_bin = int(type_bin[:-1])
            cost_bin = int(cost_bin.split('=')[1])

            values = []
    
            for line in bin_lines:
                if "value" in line:
                    values.append(int(line.split('=')[-1]))

            bin_type = BinTypeData(type_bin, cost_bin, values)
            bins_type_list.append(bin_type)

        # Ultimo bin
        bin_lines = bins[-1].split('Item:')[0].split('\n')
        
        values = []

        for j, line in enumerate(bin_lines[:-1]):
            if j == 0:
                type_bin, cost_bin = line.split(', ')
                type_bin = int(type_bin)
                cost_bin = int(cost_bin.split('=')[1])
            else:
                values.append(int(line.split('=')[-1]))
        
        bin_type = BinTypeData(type_bin, cost_bin, values)
        bins_type_list.append(bin_type)


        my_instance.bins = bins_type_list

        # items 

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

            for line in item_lines[1:-1]:
                if "=" in line:
                    values.append(int(line.split('=')[-1]))
            
            item_type = ItemData(id_item, values)
            items_type_list.append(item_type)
            # print(item_type)
                
        my_instance.items = items_type_list

        all_instances.append(my_instance)


    linked_items = txt.split("Links between items")
    linked_items = linked_items[1:]
    links = []

    for linked in linked_items[0].split('\n')[1:]:

        linked_line = linked.split(' ')
        for i, element in enumerate(linked_line):
            if 'itemNo1' in element:
                itemNo1 = int(element.split('=')[1].strip(','))
            
            elif 'itemNo2' in element:
                itemNo2 = int(element.split('=')[1].strip(','))

            elif 'cost' in element:
                cost = int(element.split('=')[1])
        
        links.append((itemNo1, itemNo2, cost))


    for i, instance in enumerate(all_instances):
        instance.linked_items = links


    def instance_to_txt(instance):

        string = f"instance={instance.id},n={instance.n},m={instance.m},d={instance.d},type={instance._type}\n"
        # instance=1,n=25,m=10,d=3,type=B1
        print(len(instance.bins))
        for bin_ in instance.bins:
            string += f"BinType:{bin_.id} cost={bin_.cost}\n"
            for i, value in enumerate(bin_.capacity):
                string += f"\tno={i+1}, value={value}\n"
        
        for item in instance.items:
            string += f"Item: no={item.id}\n"
            for i, value in enumerate(item.weight):
                string += f"\tno={i+1}, value={value}\n"

        string += "Links between items\n"
        for i, link in enumerate(instance.linked_items):
            string += f"Link{i + 1}: itemNo1={link[0]}, itemNo2={link[1]}, cost={link[2]}\n"
        return string


    # save txt for each instance in instances
    for instance in all_instances:
        with open(f"instances/{instance}.txt", 'w') as f:
            f.write(instance_to_txt(instance))
            print(f"Instance {instance.id} saved")

