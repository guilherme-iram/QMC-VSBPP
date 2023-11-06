from Instance_reader import *
from VNS import *

import numpy as np

def main():
    instance_name = "instance=10_n=25_m=10_d=5_type=B2"
    print("Instance: ", instance_name)
    path = 'instances/' + instance_name + '.txt'
    instance_reader(path)
    
    sol = VNS()

    print(sol)

if __name__ == "__main__":
    main()




