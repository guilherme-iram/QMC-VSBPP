from Instance_reader import *
from VNS import *
import numpy as np
import os
import sys
import re


def main():

    n = 25

    diretorio = "instances" 

    if os.path.exists(diretorio):

        arquivos = os.listdir(diretorio)

        for instance in arquivos[:4]:
            match = re.search(r'n=(\d+)', instance)
            if match:
                numero = match.group(1)
                numero = int(numero)

                if numero == n:

                        instance_name = instance
                        print("Instance: ", instance_name)
                        path = 'instances/' + instance_name 
                        instance_reader(path)
                    
                        sol = VNS()
                        print(sol)
                        print('-' * 100)
                        print('\n\n')

    else:
        print(f"O diretório {diretorio} não foi encontrado.")


if __name__ == "__main__":
    main()