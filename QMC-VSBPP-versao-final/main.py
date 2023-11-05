from VNS import *

def main():
    
    inst = Instance()

    Instance.readInstance('C:\\Users\\JoãoPereira\\Desktop\\QMC-VSBPP-optimizer\\instances\\instance=1_n=25_m=10_d=3_type=B1.txt')
    #Instance.readInstance('C:\\Users\\JoãoPereira\\Desktop\\QMC-VSBPP-optimizer\\instances\\instance=96_n=200_m=50_d=5_type=B4.txt')
    #print(inst)

    sol = VNS()
    print(sol)

    #sol.calculateInfo()
    #print(permutation_shortest_path(sol))

   


if __name__ == "__main__":
    main()




