from Instance_reader import *
from VNS import *
import numpy as np
import os
import sys
import re
import time


def main():

    n = 25 # 25, 50, 100, 200

    diretorio = "instances" 

    if os.path.exists(diretorio):

        arquivos = os.listdir(diretorio)
        cont = 0
        for instance in arquivos:
            cont += 1
            print(f"Instância {cont} de {len(arquivos)}\n")
            match = re.search(r'n=(25|50|100|200)', instance)
            if match:
                
                numero = match.group(1)
                numero = int(numero)

                if numero == n:
                    print(instance)

                    costs = []
                    times = []

                    for i in range(1, 5 + 1):
                        
                        print(f"Instância: {instance} - Execução: {i}")
                        print(f"Execução {i} ({i / 5 * 100:.2f}%)\n")

                        instance_name = instance
                        # print("Instance: ", instance_name)
                        path = 'instances/' + instance_name 
                        instance_reader(path)                        

                        time_start = time.time()
                        sol = VNS()
                        str_solution = str(sol)
                        time_end = time.time()

                        str_solution += f"Tempo: {time_end - time_start} (s)."

                        costs.append(sol.cost)
                        times.append(time_end - time_start)

                        print(str_solution)

                        with open(f"resultados/n{numero}/{instance_name.split('.')[0]}/VNS_solucao_{i}.txt", "w") as f:
                            f.write(str_solution)
                            f.close()

                    str_relaorio = f"Instância: {instance}\n"
                    str_relaorio += f'Melhor custo: {np.min(costs):.4f}\n'
                    str_relaorio += f'Custo médio : {np.mean(costs):.4f}\n'
                    str_relaorio += f'Tempo médio : {np.mean(times):.4f}\n'
                    str_relaorio += f'Desvio padrão do custo: {np.std(costs):.4f}\n'
                    str_relaorio += f'Desvio padrão do tempo: {np.std(times):.4f}\n'
                    

                    print(str_relaorio)

                    with open(f"resultados/n{numero}/{instance_name.split('.')[0]}/VNS_relatorio.txt", "w") as f:
                        f.write(str_relaorio)
                        f.close()
    else:
        print(f"O diretório {diretorio} não foi encontrado.")


if __name__ == "__main__":
    main()