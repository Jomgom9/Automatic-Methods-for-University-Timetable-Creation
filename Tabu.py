#-------------------------------------------------Program that obtains the result of Tabu Search and exports it to Excel-------------
#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import Lectura_de_datos as lect
import Algoritmo_Voraz as Al
import Pasar_excel as Ex
import Puntuacion as Pu
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side
import random
import copy

grupos_alumnos1,grupos_alumnos2 = lect.leer("Datos EHU.csv")

solucion_semana1 = Al.algoritmo(grupos_alumnos1)
puntuacion_max = Pu.Puntuacion(solucion_semana1)
print(puntuacion_max)
solucion = solucion_semana1.copy()
tabu={}
n_sin_mejora = 0 
puntuacion_total_max = puntuacion_max
# First, we define the number of cycles to perform
for k in range(100):
    dia = random.randint(0, len(solucion)-1) # Local changes are made within a day; otherwise, it doesn't make sense
    puntuacion_aux_max = 0
    solucion_aux_cambio = []
    # Now we define for each iteration how many local solutions we will calculate
    for i in range(200):

        solucion_aux = copy.deepcopy(solucion)
        solucion_aux2 = copy.deepcopy(solucion)
        # We define four random numbers (2 hours, 2 classrooms) to obtain the local solution
        hora1 = random.randint(0, len(solucion[0])-1)
        clase1 = random.randint(0, len(solucion[0][0])-1)
        hora2 = random.randint(0, len(solucion[0])-1)
        clase2 = random.randint(0, len(solucion[0][0])-1)

        # We make the swap
        cambio1 = solucion_aux2[dia][hora1][clase1]
        cambio2 = solucion_aux2[dia][hora2][clase2]
        
        # If the swap is made between two slots where there is no class, we skip it
        if type(solucion_aux2[dia][hora1][clase1][6]) == int and type(solucion_aux2[dia][hora2][clase2][6]) == int:
            continue

        cambio_tupla1=((hora1,clase1),(hora2,clase2))
        cambio_tupla2=((hora1,clase1),(hora2,clase2))
        # If the swap is in the Tabu list, it is not performed
        if cambio_tupla1 in tabu or cambio_tupla2 in tabu:
            continue

        solucion_aux[dia][hora1][clase1] = cambio2
        solucion_aux[dia][hora2][clase2] = cambio1

        # We calculate the score of the new solution
        puntuacion_aux = Pu.Puntuacion(solucion_aux)
        
        # If the swap is worse but better than what was obtained for this iteration, it is saved
        if puntuacion_aux_max < puntuacion_aux:
            puntuacion_aux_max = puntuacion_aux
            solucion_aux_cambio = copy.deepcopy(solucion_aux)
            cambio_aux = copy.deepcopy(cambio_tupla1)

        # If the new score is better, the swap is made directly
        if puntuacion_aux > puntuacion_max:
            tabu[cambio_tupla1] = 10
            solucion = copy.deepcopy(solucion_aux)
            puntuacion_max = puntuacion_aux
            n_sin_mejora = 0
            break
    
    # If no improvement was obtained, we keep the best "worst" one
    else:
        solucion = copy.deepcopy(solucion_aux_cambio)
        puntuacion_max = puntuacion_aux_max
        n_sin_mejora += 1
        tabu[cambio_aux] = 10
    
    # We update the Tabu list
    for key in list(tabu.keys()):
        tabu[key] -= 1
        if tabu[key] == 0:
            del tabu[key]
    print(puntuacion_max,dia,i,k)
    tabu[cambio_aux] = 10
    if puntuacion_max > puntuacion_total_max:
        puntuacion_total_max = puntuacion_max
        solucion_final = copy.deepcopy(solucion)

    # If more than 500 iterations are made without improvement, we end
    if n_sin_mejora > 500:
        break

print("end")
print(puntuacion_total_max)

# We save the solution to Excel
Ex.excel(solucion_final,"solucion_semana_1Cuatrimestre_tabu_final4")
