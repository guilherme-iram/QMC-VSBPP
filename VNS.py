from Construction import *
from Neighborhood import *

def VND():
    pass

def VNS():
    
    best = construction()
    best.calculateInfo()
    
    print(best)
    print("-" * 80) 
    best = swap_bins(best)
    best.calculateInfo()
    print("SWAP BINS\n")
    print(best)

    return best

