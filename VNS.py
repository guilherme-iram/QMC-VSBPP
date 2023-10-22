from Instance import *
from Solution import *
from Construction import *

def VND():
    pass

def VNS():
    best = Solution.from_Instance()
    
    # best = ConstructionHeuristic(Instance) Abaixo segue um exemplo de solução criada usando as primeiras cinco caixas
    # A ideia aqui era apenas gerar uma solução arbitrária para testar a função calculateInfo()
    best = construction()
    
    best.calculateInfo()
    
    return best

