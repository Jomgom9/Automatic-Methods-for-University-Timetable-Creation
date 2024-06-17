#-------------------------------------------------Program that obtains the result of Simulated Annealing and exports it to Excel-------------
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
import math

grupos_alumnos1,grupos_alumnos2 = lect.leer("Datos EHU.csv")

solucion_semana1 = Al.algoritmo(grupos_alumnos1)
puntuacion_max = Pu.Puntuacion(solucion_semana1)
print(puntuacion_max)
solucion = solucion_semana1.copy()
# Define the initial temperature
T=2
# Define the number of iterations
for k in range(4999):
    # Define the temperature change for each iteration
    T-=0.0004
    dia = random.randint(0, len(solucion)-1) # Local changes are made within a day; otherwise, it doesn't make sense
    # Define four random numbers (2 hours, 2 classrooms) to obtain the local solution
    solucion_aux = copy.deepcopy(solucion)
    solucion_aux2 = copy.deepcopy(solucion)
    hora1 = random.randint(0, len(solucion[0])-1)
    clase1 = random.randint(0, len(solucion[0][0])-1)
    hora2 = random.randint(0, len(solucion[0])-1)
    clase2 = random.randint(0, len(solucion[0][0])-1)
    # Perform the swap
    cambio1 = solucion_aux2[dia][hora1][clase1]
    cambio2 = solucion_aux2[dia][hora2][clase2]
    # If the swap is made between two slots where there is no class, skip it
    if type(solucion_aux2[dia][hora1][clase1][6]) == int and type(solucion_aux2[dia][hora2][clase2][6]) == int:                
        continue

    solucion_aux[dia][hora1][clase1] = cambio2
    solucion_aux[dia][hora2][clase2] = cambio1
    puntuacion_aux = Pu.Puntuacion(solucion_aux)
    # If the score is better, it is always accepted
    if puntuacion_aux > puntuacion_max:
        solucion = copy.deepcopy(solucion_aux)
        puntuacion_max = puntuacion_aux

    # If it is worse, it will depend on the exponential of the temperature and the difference between the current and new score
    else:
        # Generate a random number and compare it with the exponential
        num_random = random.random() 
        DeltaE = puntuacion_max - puntuacion_aux
        num_com = math.exp(-DeltaE/T)
        # Compare the exponential with a random number
        if num_com >= num_random:
            puntuacion_max = puntuacion_aux
            solucion = copy.deepcopy(solucion_aux)

print("end")
print(puntuacion_max)
Ex.excel(solucion,"annealing prueba")

	