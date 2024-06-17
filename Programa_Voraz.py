#-------------------------------------------------This is the main program for the Greedy Algorithm-------------------------------------------
#---------------------------Based on Excel data, it generates an Excel file with the solution----------------------------
#------------------------------------------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import Lectura_de_datos as lect
import Algoritmo_Voraz as Al
import Pasar_excel as Ex
import Puntuacion as Pu
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side

# Fetch student groups from the database
grupos_alumnos1, grupos_alumnos2 = lect.leer("Datos EHU.csv")

# Get the solution
solucion_semana1 = Al.algoritmo(grupos_alumnos1)

# Get the score
puntuacion1 = Pu.Puntuacion(solucion_semana1)

print(puntuacion1)

#---------------------------Pass data to Excel---------------------------------------
Ex.excel(solucion_semana1, "prueba")


