from Instance_reader import *

def main():
    instance_name = "instance=1_n=25_m=10_d=3_type=B1"
    path = 'instances/' + instance_name + '.txt'
    instance = instance_reader(path)
    print("\nResultado final:", instance)

if __name__ == "__main__":
    main()