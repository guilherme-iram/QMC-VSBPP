from Instance_reader import *
from VNS import *

def main():
    instance_name = "instance=1_n=25_m=10_d=3_type=B1"
    path = 'instances/' + instance_name + '.txt'
    instance_reader(path)

    # for item in Instance.items_Data:
        # print(item)
    
    sol = VNS()
    # print(sol)

if __name__ == "__main__":
    main()