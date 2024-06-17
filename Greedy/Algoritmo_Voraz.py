#-------------------------------------------------This function executes the Greedy algorithm-------------------------------------------
#-------------------------------------------------Inputs: List with groups of students-----------------------------------------
#-------------------------------------------------Output: Greedy Solution------------------------------------------------------------
import pandas as pd
import numpy as np
import Lectura_de_datos as lect
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side
import Lectura_de_datos as lect

def algoritmo(grupos_alumnos):
    #1=group1, 2=group2 
    alu = len(grupos_alumnos) #number of student groups
    aulas = 8 #number of classrooms
    franjas = 10 #number of time slots
    horas_max = 4  #maximum number of class hours in a day
    horas_max_opt = 7 #maximum number of elective hours in a day
    dias_semna = 5 #Days of the week classes can be held


    solucion_semana = np.array([None] * dias_semna)
    clases_vacias = 0
    puntos = 0
    horas_max_dia=[]
    coincidencias_ga={}
    for curso in grupos_alumnos:
        mañana=0
        tarde=0
        if len(curso)>0:
            for asig in curso:
                if asig[6][6]=="No":
                    mañana+=int(asig[6][8])*int(asig[6][7])
                else:
                    tarde+=int(asig[6][7])*int(asig[6][8])
            if curso[0][6][1] == "Optativa":
                horas_max_dia.append(horas_max_opt)
            elif tarde>19 or mañana>19:
                horas_max_dia.append(horas_max+1)
            else:
                horas_max_dia.append(horas_max)
        else:
            horas_max_dia.append(horas_max)


    #----------------------Algorithm Start----------------------------
    for dia in range(dias_semna):
        dia_max = np.array(horas_max_dia) #list with maximum hours for each group of students in the day
        solucion_dia = np.zeros((franjas,aulas,7),dtype=object)  # final empty day solution
        #analyze for each group/subject which time slot is optimal
        for grupo in range(alu): #for each group of students
            for asignatura in range(len(grupos_alumnos[grupo])): #for each subject within each group
                

                asignatura = (asignatura + dia ) % len(grupos_alumnos[grupo]) #Start cycle at different index each time, so the algorithm doesn't leave the last indices always at the end, allowing only four subjects per day
                if grupos_alumnos[grupo][asignatura][6][2][-3:-1]=="GA":
                    if int(grupos_alumnos[grupo][asignatura][6][2][-1])>1:
                        nombre=grupos_alumnos[grupo][asignatura][6][11]
                        if nombre != "No":
                            coincidencias_ga[nombre]=grupos_alumnos[grupo][asignatura]
                            continue
                hora_opt,clase_opt,optimo_max,cont = 0, 0, 0, 0
                duracion = grupos_alumnos[grupo][asignatura][3]
                for hora in range(franjas):
                    
                    for clase in range(aulas):

                        optimo = 0
                        for i in range(2): #only check for teacher and group
                            for clase2 in range(aulas): #This loop ensures no overlap in students or subjects at the same time in different classes, and checks for consecutive hours in different classes

                                if int(grupos_alumnos[grupo][asignatura][i]) == int(solucion_dia[hora][clase2][i]) :
                                    if i == 0: #If same teacher, not possible
                                        optimo = optimo - 10000
                                    else: #If same course, unless they are electives from different specialties
                                        if grupos_alumnos[grupo][asignatura][6][1] != "Optativa" or solucion_dia[hora][clase2][6][5]== grupos_alumnos[grupo][asignatura][6][5]:
                                            optimo = optimo - 10000
                                #Check if it coincides with a subject common to another major
                                elif round((solucion_dia[hora][clase2][1] % 1) *1000) in grupos_alumnos[grupo][asignatura][5]: 
                                    optimo = optimo - 10000
                                
                                elif  type(solucion_dia[hora][clase2][6]) != int: #To avoid overlapping electives with those from 4

                                    if i == 1 and str(grupos_alumnos[grupo][asignatura][6][1]) == "Optativa" and  str(solucion_dia[hora][clase2][6][1])!="Optativa":
                                    
                                        if solucion_dia[hora][clase2][6][1] == "4" and solucion_dia[hora][clase2][6][0] == grupos_alumnos[grupo][asignatura][6][0] :
                                                
                                            optimo = optimo -10000

                                
                                if hora == 0:
                                    if int(grupos_alumnos[grupo][asignatura][i]) == int(solucion_dia[hora + 1][clase2][i]):
                                        # if solucion_dia[hora + 1][clase2][6][2][-3]!="_":
                                            if clase == clase2:
                                                optimo = optimo + 2 + 2*i #This gives priority to consecutive students over consecutive teachers    
                                            else:
                                                optimo = optimo + 1 + i 
                                elif hora == franjas - 1:
                                    if int(grupos_alumnos[grupo][asignatura][i]) == int(solucion_dia[(hora - 1)][clase2][i]) :
                                        # if solucion_dia[hora - 1][clase2][6][2][-3]!="_":
                                            if clase == clase2:
                                                optimo = optimo + 2 + 2*i #This gives priority to consecutive students over consecutive subjects    
                                            else:
                                                optimo = optimo + 1 + i 

                                else:        
                                    if int(grupos_alumnos[grupo][asignatura][i]) == int(solucion_dia[hora + 1][clase2][i]):
                                        # if solucion_dia[hora + 1][clase2][6][2][-3]!="_":
                                            if clase == clase2:
                                                optimo = optimo + 2 + 2*i #This gives priority to consecutive students over consecutive subjects    
                                            else:
                                                optimo = optimo + 1 + i 
                                    elif  int(grupos_alumnos[grupo][asignatura][i]) == int(solucion_dia[hora - 1][clase2][i]):
                                        # if solucion_dia[hora - 1][clase2][6][2][-3]!="_":
                                            if clase == clase2:
                                                optimo = optimo + 2 + 2*i #This gives priority to consecutive students over consecutive subjects    
                                            else:
                                                optimo = optimo + 1 + i 

                        if hora < 4: #Prefer morning classes and lunch break
                            optimo += 2
                            if grupos_alumnos[grupo][asignatura][2] != "Si": #Morning students
                                optimo +=5 
                        elif hora == 4:
                            if grupos_alumnos[grupo][asignatura][2] != "Si": #Morning students
                                optimo += 3
                                        
                        elif hora > 5 :
                            optimo += 1/hora #Better right after lunch than last hour
                            if grupos_alumnos[grupo][asignatura][2] == "Si": #Afternoon students
                                optimo += 4
                        elif hora == 5:
                            optimo += 1/hora
                            if grupos_alumnos[grupo][asignatura][2] == "Si": #Afternoon students
                                optimo+=2 
                        if dia == 2 and 2<hora and grupos_alumnos[grupo][asignatura][2] != "Si": #No classes after 11:30 on Wednesdays
                            optimo = optimo -1000

                        if hora == 0 or hora == 3 :
                            if grupos_alumnos[grupo][asignatura][6][2][-3:-1]=="GA" and grupos_alumnos[grupo][asignatura][2] != "Si":
                                optimo += 3
                        elif hora == 9 or hora == 6:
                            if grupos_alumnos[grupo][asignatura][6][2][-3:-1]=="GA" and grupos_alumnos[grupo][asignatura][2] == "Si":
                                optimo += 3

                        #Now analyze teacher preferences for hours
                        horas_pre=grupos_alumnos[grupo][asignatura][6][9].split(" ")
                        if len(horas_pre)>0:
                            lista = list
                            for i in horas_pre:
                                if hora +1 == int(i):
                                    optimo += 2

                        #Now analyze day preferences 
                        dias_pre=grupos_alumnos[grupo][asignatura][6][10].split(" ")
                        if len(dias_pre)>0:
                            for i in dias_pre:
                                if  dia+1 == int(i):
                                    optimo += 2
                        
                        # Now we take into account: 1- that the optimal is better than previous ones. 2- that the time slot is empty.
                        # 3- that the maximum number of subjects per day has not already been reached. 4- that the maximum weekly hours of the subject have not already been reached.

                        valido = "si"
                        if franjas-hora+1<=duracion:
                            valido = "no"
                        elif  hora<4 and hora + duracion > 4:
                            valido ="no"
                        else:
                            for i in range(duracion):
                                if solucion_dia[hora+i][(clase)][0:1].all() != np.zeros(2).all():
                                    valido = "no"

                        if optimo>optimo_max and valido == "si" and dia_max[grupo] > 0 and grupos_alumnos[grupo][asignatura][4] > 0: 
                            optimo_max = optimo
                            cont = 1
                            hora_opt,clase_opt = hora,clase  
                            
                            
                if cont == 1: # The counter is used because if the new group cannot fit into any time slot, it would be negative, overwriting the schedule (0,0).

                    
                    for i in range(duracion):
                        solucion_dia[hora_opt+i][clase_opt] = grupos_alumnos[grupo][asignatura]
                    dia_max[grupo] -= 1
                    grupos_alumnos[grupo][asignatura][4] -= 1
                puntos += optimo_max

        solucion_semana [dia] = solucion_dia
    
    for dia in range(len(solucion_semana)):
        solucion_dia_ga=solucion_semana[dia]
        # Each subject's score is analyzed based on the subjects at its time and one hour before and after, in different classes.
        for hora in range(len(solucion_dia_ga)): 
            for clase in range(len(solucion_dia_ga[hora])): 
                if type(solucion_dia_ga[hora][clase][6]) != int:

                    if solucion_dia_ga[hora][clase][6][2] in coincidencias_ga:
                        for clase2 in range(len(solucion_dia_ga[hora])):
                            if type(solucion_dia_ga[hora][clase2][6])==int:
                                solucion_dia_ga[hora][clase2] = coincidencias_ga[solucion_dia_ga[hora][clase][6][2]]
                                break 
        solucion_semana [dia] = solucion_dia_ga
    return solucion_semana
