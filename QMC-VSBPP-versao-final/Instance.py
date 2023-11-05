from collections import defaultdict

def default_factory():
    return 0


class ItemData:
    def __init__(self, id:int = -1, totalJointCost:int = 0, associatedJointCost:int = 0) -> None:
        self.id = id
        self.dimensions = [0 for i in range(Instance.d)]
        self.links = []
        self.totalJointCost = totalJointCost
        self.associatedJointCost = associatedJointCost

    def __str__(self) -> str:
        return f"Item {self.id},\ntotalJointCost = {self.totalJointCost}, \nassociatedJointCost = {self.associatedJointCost}, \ndimensions={self.dimensions}, \nlinks={self.links}\n"
    
    def __repr__(self) -> str:
        return self.__str__()
    
class BinData:

    def __init__(self, id:int = -1, cost:int = -1) -> None:
        self.id = id
        self.dimensions = [0 for i in range(Instance.d)]
        self.cost = cost

    def __str__(self) -> str:
        return f"Bin id={self.id}, cost = {self.cost} , dimensions={self.dimensions}\n"
    
    def __repr__(self) -> str:
        return self.__str__()


class Instance:

    itemsData = []
    binsData = []
    linkMatrix = {}
    id = -1
    n = -1
    m = -1
    d = -1
    type = 'Not set'

    def __str__(self) -> str:
        a_str = f"Instance: {Instance.id}, n = {Instance.n}, m = {Instance.m}, d = {Instance.d}, type = {Instance.type}"
        a_str += "\n\nBins Data:\n"
        for bin in Instance.binsData:
            a_str += f"{bin}\n"
        
        a_str += "\nItems Data:\n"
        for item in Instance.itemsData:
            a_str += f"{item}\n"
        
        return a_str
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def readInstance(path:str)->None:
        
        file = open(path, 'r').readlines()
        firstLine = file[0].split(',')
        
        Instance.id = int(firstLine[0].split('=')[-1])
        Instance.n = int(firstLine[1].split('=')[-1])
        Instance.m = int(firstLine[2].split('=')[-1])
        Instance.d = int(firstLine[3].split('=')[-1])
        Instance.type = firstLine[4].split('=')[-1].strip()

        line_count = 1                                      # linha atual do arquivo
        all_bins_full = False                               # não tiver preenchido as informações de todos os bins
        while (all_bins_full == False):
            d = 0                                # não tiver preenchido as informações de um bin
            bin_data = BinData()
            bin_basic_data = file[line_count].split(' ')    # dados básicos do bin

            bin_data.id = int(bin_basic_data[0].split(':')[-1]) - 1     # tipo do bin -1 para ficar no intervalo da lista

            bin_data.cost = int(bin_basic_data[1].split('=')[-1])         # custo do bin
            
            while (d!= Instance.d):                             # enquanto não tiver preenchido as informações de um bin
                line_count += 1
                bin_item_data = file[line_count].split(', ')
                bin_data.dimensions[d] = int(bin_item_data[-1].split('=')[-1])

                d += 1
            
            Instance.binsData.append(bin_data)

            all_bins_full = (len(Instance.binsData) == Instance.m) # se tiver preenchido as informações de todos os bins

            line_count += 1

        
        all_items_full = False

        while (all_items_full == False):
            d = 0
            item_data = ItemData()
            item_basic_data = file[line_count].split('=')

            item_data.id = int(item_basic_data[-1]) - 1

            while (d!= Instance.d):
                line_count += 1
                item_bin_data = file[line_count].split(', ')
                item_data.dimensions[d] = int(item_bin_data[-1].split('=')[-1])

                d += 1
            
            Instance.itemsData.append(item_data)

            all_items_full = (len(Instance.itemsData) == Instance.n)

            line_count += 1
        
        
        line_count += 1 # pula a linha escrito "Link between items"

        Instance.linkMatrix = {i:defaultdict(default_factory) for i in range(Instance.n)}

        for line in file[line_count:]:
            line_data = line.split(',')
            item1 = int(line_data[0].split('=')[-1]) - 1
            item2 = int(line_data[1].split('=')[-1]) - 1
            cost = int(line_data[2].split('=')[-1])


            Instance.itemsData[item1].links.append(item2)

            Instance.itemsData[item1].totalJointCost += cost
            Instance.itemsData[item2].associatedJointCost += cost
            Instance.linkMatrix[item1][item2] = cost
        
        



