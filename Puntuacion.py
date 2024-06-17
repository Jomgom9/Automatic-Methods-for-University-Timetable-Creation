#-------------------------------------------------This function provides the score for a solution-------------------------------------------
#-------------------------------------------------Inputs: Solution as a list----------------------------------------------------
#-------------------------------------------------Output: Objective function value of the solution-------------

import pandas as pd
import numpy as np
import Lectura_de_datos as lect
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side

def Puntuacion(solucion_semana):

    aulas = 8 # Number of classrooms
    franjas = 10 # Number of time slots
    horas_max = 4  # Maximum number of class hours in a day
    horas_max_opt = 7 # Maximum number of elective hours in a day
    dias_semna = 5 # Days of the week when classes can be held
    ga = []

    #----------------------Start of scoring---------------------------
    # First, let's make a list of GAs with which no comparisons need to be made
    for dia in range(len(solucion_semana)):
        solucion_dia = solucion_semana[dia]
        for hora in range(len(solucion_dia)): # Loop for each hour
            for clase in range(len(solucion_dia[hora])): # Loop within each classroom
                if type(solucion_dia[hora][clase][6]) == int: # If the slot is empty, skip it
                    continue
                if solucion_dia[hora][clase][6][2][-3:-1] == "GA":
                    if int(solucion_dia[hora][clase][6][2][-1]) > 1:
                        nombre = solucion_dia[hora][clase][6][11]
                        if nombre != "No":
                            ga.append(solucion_dia[hora][clase][6][2])

    puntos = 0
    for dia in range(len(solucion_semana)):
        solucion_dia = solucion_semana[dia]
        # Analyze for each subject what score it receives based on subjects at its hour and one hour before and after, in different classes
        for hora in range(len(solucion_dia)): # Loop for each hour
            for clase in range(len(solucion_dia[hora])): # Loop within each classroom
                if type(solucion_dia[hora][clase][6]) == int: # If the slot is empty, skip it
                    continue
                puntos_asignatura = 0

                # Let's first consider cases where they are GA, as these do not need to be compared with groups

                if solucion_dia[hora][clase][6][2] in ga:
                    cumplir = 0
                    nombre = solucion_dia[hora][clase][6][11]
                    for clase2 in range(len(solucion_dia[hora])):

                        if type(solucion_dia[hora][clase2][6]) == int: 
                            continue
                        if clase == clase2:
                            continue
                        if solucion_dia[hora][clase2][6][3] == solucion_dia[hora][clase][6][3]:
                            puntos = puntos - 10000
                        if nombre == solucion_dia[hora][clase2][6][2]:
                            cumplir = 1
                    if cumplir == 0:
                        puntos = puntos - 100000
                    continue

                # Now, we look at general cases
                for i in range(2): # Check teachers and subjects
                    # Loop to ensure students or subjects do not coincide at the same hour in different classes and to check for consecutive hours in different classes
                    for clase2 in range(len(solucion_dia[hora])): 
                        if type(solucion_dia[hora][clase2][6]) == int:
                            continue

                        if clase != clase2:
                            # If compared with a GA, no need to check groups or anything else
                            if solucion_dia[hora][clase2][6][2] in ga or solucion_dia[hora][clase][6][2] in ga:
                                if int(solucion_dia[hora][clase][0]) == int(solucion_dia[hora][clase2][0]):
                                    puntos = puntos - 10000
                                continue
                            elif int(solucion_dia[hora][clase][i]) == int(solucion_dia[hora][clase2][i]):
                                if i == 0: # If it is the same teacher, it can't be
                                    puntos_asignatura = puntos_asignatura - 10000
                                else: # If it is the same course, it can't either unless they are electives of different mention
                                    if solucion_dia[hora][clase][6][1] != "Optativa" or solucion_dia[hora][clase2][6][5] == solucion_dia[hora][clase][6][5]:
                                        puntos_asignatura = puntos_asignatura - 10000
                            # Now check if it coincides with a subject common to another degree
                            elif type(solucion_dia[hora][clase][5]) != int:
                                if round((solucion_dia[hora][clase2][1] % 1) * 1000) in solucion_dia[hora][clase][5]: 
                                    puntos_asignatura = puntos_asignatura - 10000

                            # Now enforce that electives cannot coincide with 4th year subjects
                            if type(solucion_dia[hora][clase][6]) != int and type(solucion_dia[hora][clase2][6]) != int: 
                                if i == 1 and str(solucion_dia[hora][clase][6][1]) == "Optativa" and str(solucion_dia[hora][clase2][6][1]) != "Optativa":
                                    if str(solucion_dia[hora][clase2][6][1]) == "4" and solucion_dia[hora][clase2][6][0] == solucion_dia[hora][clase][6][0]:
                                        puntos_asignatura = puntos_asignatura - 10000

                        # Next, check preferences for hours       
                        if hora == 0:
                            if int(solucion_dia[hora][clase][i]) == int(solucion_dia[hora + 1][clase2][i]):
                                if clase == clase2:
                                    # Give more points to students in consecutive slots than to teachers (teachers i=0, students/subjects i=1)
                                    puntos_asignatura = puntos_asignatura + 4 + 2*i     
                                else:
                                    # If they are in different classrooms, the score also increases
                                    puntos_asignatura = puntos_asignatura + 1 + 2*i 

                                if str(solucion_dia[hora][clase][6][1]) != "Optativa":
                                    puntos_asignatura = puntos_asignatura + 1 # It's better to have non-electives consecutive than electives

                        elif hora == franjas - 1:
                            if int(solucion_dia[hora][clase][i]) == int(solucion_dia[hora - 1][clase2][i]):
                                if clase == clase2:
                                    # Give more points to students in consecutive slots than to teachers (teachers i=0, students/subjects i=1)
                                    puntos_asignatura = puntos_asignatura + 4 + 2*i   
                                else:
                                    # If they are in different classrooms, the score also increases
                                    puntos_asignatura = puntos_asignatura + 1 + 2*i 
                                if str(solucion_dia[hora][clase][6][1]) != "Optativa":
                                    puntos_asignatura = puntos_asignatura + 1 # It's better to have non-electives consecutive than electives

                        else:        
                            if int(solucion_dia[hora][clase][i]) == int(solucion_dia[hora + 1][clase2][i]):
                                if clase == clase2:
                                    # Give more points to students in consecutive slots than to teachers (teachers i=0, students/subjects i=1)
                                    puntos_asignatura = puntos_asignatura + 4 + 2*i    
                                else:
                                     # If they are in different classrooms, the score also increases
                                    puntos_asignatura = puntos_asignatura + 1 + 2*i 
                                if str(solucion_dia[hora][clase][6][1]) != "Optativa":
                                    puntos_asignatura = puntos_asignatura + 1 # It's better to have non-electives consecutive than electives
                            if int(solucion_dia[hora][clase][i]) == int(solucion_dia[hora - 1][clase2][i]):
                                if clase == clase2:
                                    # Give more points to students in consecutive slots than to teachers (teachers i=0, students/subjects i=1)
                                    puntos_asignatura = puntos_asignatura + 4 + 2*i    
                                else:
                                    # If they are in different classrooms, the score also increases
                                    puntos_asignatura = puntos_asignatura + 1 + 2*i 
                                if str(solucion_dia[hora][clase][6][1]) != "Optativa":
                                    puntos_asignatura = puntos_asignatura + 1 # It's better to have non-electives consecutive than electives

                # Next, analyze subject preferences according to time slots
                if hora < 4: 
                    puntos_asignatura += 2
                    # Subjects in the morning will score a lot
                    if solucion_dia[hora][clase][2] != "Si": # Students prefer the morning
                        puntos_asignatura += 9 

                elif hora == 4:
                    # In the first lunch hour, if the subject is in the morning, it also scores
                    if solucion_dia[hora][clase][2] != "Si": # Students prefer the morning
                        puntos_asignatura += 3

                elif hora > 5:
                    puntos_asignatura += 1/hora # In the afternoon, the sooner the class is held, the better 
                    if solucion_dia[hora][clase][2] == "Si": # Students prefer the afternoon
                        puntos_asignatura += 9 

                elif hora == 5:
                    puntos_asignatura += 1/hora
                    if solucion_dia[hora][clase][2] == "Si": # Students prefer the afternoon
                        puntos_asignatura += 2 

                if dia == 2 and 2 < hora and solucion_dia[hora][clase][2] != "Si": # No classes after 11:30 on Wednesdays
                    puntos_asignatura = puntos_asignatura - 1000
                # Prefer GAs to be at the first or last hour.
                if hora == 0 or hora == 3:
                    if solucion_dia[hora][clase][6][2][-3:-1] == "GA" and solucion_dia[hora][clase][2] != "Si":
                        puntos_asignatura += 3
                elif hora == 9 or hora == 6:
                    if solucion_dia[hora][clase][6][2][-3:-1] == "GA" and solucion_dia[hora][clase][2] == "Si":
                        puntos_asignatura += 3

                # Now analyze teacher preferences for hours
                horas_pre = solucion_dia[hora][clase][6][9].split(" ")
                # If the teacher wants to teach in a specific time slot, try to schedule the class in those hours
                if len(horas_pre) > 0:
                    lista = list
                    for i in horas_pre:
                        if hora + 1 == int(i):
                            puntos_asignatura += 2

                # Now analyze preferences for days 
                dias_pre = solucion_dia[hora][clase][6][10].split(" ")
                # If the teacher wants to teach on specific day(s), try to schedule the class on those days
                if len(dias_pre) > 0:
                    for i in dias_pre:
                        if dia + 1 == int(i):
                            puntos_asignatura += 2

                # Finally, add the subject's points to the total
                puntos += puntos_asignatura

    return puntos

