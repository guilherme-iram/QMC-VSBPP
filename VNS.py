from Instance import *
from Solution import *

def VND():
    pass

def VNS():
    best = Solution.from_Instance()
    
    # best = ConstructionHeuristic(Instance) Abaixo segue um exemplo de solução criada usando as primeiras cinco caixas
    # A ideia aqui era apenas gerar uma solução arbitrária para testar a função calculateInfo()
    for i in range(1, 6):
        best.bins.add(i)
        
        for j in range( (5 * (i - 1)), (5 * i)): # gerando pares (1, 6), (6, 11), (11, 16), (16, 21), (21, 26)
            best.items[j].setBinBeforeCalc(i)
    
    best.calculateInfo()
    
    return best

