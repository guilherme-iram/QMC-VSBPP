from Instance_reader import *
from VNS import *

def main():
    instance_name = "instance=2_n=25_m=20_d=3_type=B1"
    print("Instance: ", instance_name)
    path = 'instances/' + instance_name + '.txt'
    instance_reader(path)

    # for item in Instance.items_Data:
        # print(item)
    
    sol = VNS()
    # print(sol)

if __name__ == "__main__":
    main()