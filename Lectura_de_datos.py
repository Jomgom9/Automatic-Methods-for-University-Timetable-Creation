#-------------------------------------------------This function reads data from the .csv file-------------------------------------------
#-------------------------------------------------Inputs: CSV file name----------------------------------------------------
#-------------------------------------------------Output: List with different student groups and their characteristics-------------


import csv
import numpy as np
	# Open the CSV file in read mode
def leer(nombre):
	with open(nombre, newline='') as csvfile:

	    n = 0
	    asignaturas = dict()
	    carrera = {}
	    numero_carreras = {}
	    optativas = []
	    no_optativas = []
	    contador_carrera = 0
	    contador_curso = 0
	    contador_profesor = 0
	    profesores = {}
	    codificacion2 = []
	    agrupacion_cursos1=[]
	    codificacion1 = []
	    agrupacion_cursos2=[]
	    numero_asignatura = 0
	    indice_asignatura_repetida = None
	    asignaturas_repetidas = []
	    num=0

	    # Create a CSV reader object
	    reader = csv.reader(csvfile)
	    # Read each line of the file
	    for row in reader: # `row` is a list containing the values of the current row
	        if n == 0:
	            n = 1
	            continue
	        cadena = row[0]
	        valores = cadena.split(';')

	        if valores[1] == "Optativa":
	        	optativas.append(valores)
	        else:
	        	no_optativas.append(valores)
	    if len(optativas)>1:    	
	    	opt_y_noopt = np.concatenate((no_optativas,optativas),axis=0)
	    else:
	    	opt_y_noopt = np.array(no_optativas)

	    for datos in opt_y_noopt:
	        if datos[2]+str(datos[4]) in asignaturas:
	        	if indice_asignatura_repetida == None or indice_asignatura_repetida == str(datos[0]) + str(datos[1]):
	        		indice_asignatura_repetida = str(datos[0]) + str(datos[1])
	        		asignaturas_repetidas.append(asignaturas[datos[2]+str(datos[4])])
	        		
	        	else:
	        		indice_asignatura_repetida = str(datos[0]) + str(datos[1])
	        		asignaturas_repetidas = []
	        		asignaturas_repetidas.append(asignaturas[datos[2]+str(datos[4]) ])
	        		
	        	#Save course data in case the next subject is from another course
	        	datos_index = np.where(np.all(opt_y_noopt == datos, axis=1))[0][0]
	        	if datos_index + 1 < len(opt_y_noopt):
	        		if datos[1] != opt_y_noopt[datos_index+1][1] or datos[0] != opt_y_noopt[datos_index+1][0]:
	        			if len(agrupacion_cursos1)>0 or len(agrupacion_cursos2)>0:
	        				codificacion1.append(np.array(agrupacion_cursos1))
	        				codificacion2.append(np.array(agrupacion_cursos2))
	        				agrupacion_cursos1=[]
	        				agrupacion_cursos2=[]
	        				asignaturas_repetidas=[]
	        	continue
	       	
	       	else:	
	       		if indice_asignatura_repetida != str(datos[0]) + str(datos[1]):
	       			indice_asignatura_repetida = None
	       			asignaturas_repetidas = []
	       		numero_asignatura += 1
	       		asignaturas[datos[2]+str(datos[4]) ] = numero_asignatura


	        if datos[3] in profesores:
	        		numero_profesor = profesores[datos[3]] #Check if it's a new professor or not
	       	else:
	       		contador_profesor +=1
	       		profesores[datos[3]] = contador_profesor
	       		numero_profesor = profesores[datos[3]]

	       	if datos[0] in carrera:	

	            if datos[1] in carrera[datos[0]]:
	                numero_Car_Cur = carrera[datos[0]][datos[1]]
	          
	                if (datos[4]=="1"):
	                	agrupacion_cursos1.append(np.array([numero_profesor,numero_Car_Cur+numero_asignatura/1000,datos[6],int(datos[7]),int(datos[8]),asignaturas_repetidas, datos]))
	                	
	                elif (datos[4]=="2"):
	                	agrupacion_cursos2.append(np.array([numero_profesor,numero_Car_Cur+numero_asignatura/1000,datos[6],int(datos[7]), int(datos[8]),asignaturas_repetidas,datos]))
	                	
	                else:
	                	agrupacion_cursos1.append(np.array([numero_profesor,numero_Car_Cur+numero_asignatura/1000,datos[6],int(datos[7]),int(datos[8]),asignaturas_repetidas,datos]))
	                	agrupacion_cursos2.append(np.array([numero_profesor,numero_Car_Cur+numero_asignatura/1000, datos[6],int(datos[7]),int(datos[8]),asignaturas_repetidas,datos]))
	                
	                #Save course data in case the next subject is from another course.
	                datos_index = np.where(np.all(opt_y_noopt == datos, axis=1))[0][0]
	                if datos_index + 1 < len(opt_y_noopt):
	                	if datos[1] != opt_y_noopt[datos_index+1][1] or datos[0] != opt_y_noopt[datos_index+1][0]:
	                		if len(agrupacion_cursos1)>0 or len(agrupacion_cursos2)>0:
	                			codificacion1.append(np.array(agrupacion_cursos1))
	                			codificacion2.append(np.array(agrupacion_cursos2))
	                			agrupacion_cursos1=[]
	                			agrupacion_cursos2=[]
	                			asignaturas_repetidas=[]

	            else:
	                contador_curso = len(carrera[datos[0]]) + 1
	                contador_carrera = numero_carreras[datos[0]]
	                carrera[datos[0]][datos[1]] = contador_curso + contador_carrera
	                numero_Car_Cur = carrera[datos[0]][datos[1]]

	                if (datos[4]=="1"):
	                	agrupacion_cursos1.append(np.array([numero_profesor,numero_Car_Cur+numero_asignatura/1000,datos[6],int(datos[7]), int(datos[8]),asignaturas_repetidas,datos]))
	                
	                elif (datos[4]=="2"):
	                	agrupacion_cursos2.append(np.array([numero_profesor,numero_Car_Cur+numero_asignatura/1000,datos[6],int(datos[7]), int(datos[8]),asignaturas_repetidas,datos]))
	               		
	                else:
	                	agrupacion_cursos1.append(np.array([numero_profesor,numero_Car_Cur+numero_asignatura/1000,datos[6], int(datos[7]),int(datos[8]),asignaturas_repetidas,datos]))
	                	agrupacion_cursos2.append(np.array([numero_profesor,numero_Car_Cur+numero_asignatura/1000,datos[6],int(datos[7]), int(datos[8]),asignaturas_repetidas,datos]))
	                datos_index = np.where(np.all(opt_y_noopt == datos, axis=1))[0][0]

	                #Save course data in case the next subject is from another course.
	                if datos_index + 1 < len(opt_y_noopt):
	                	if datos[1] != opt_y_noopt[datos_index+1][1] or datos[0] != opt_y_noopt[datos_index+1][0] :
	                		if len(agrupacion_cursos1)>0 or len(agrupacion_cursos2)>0:
	                			codificacion1.append(np.array(agrupacion_cursos1))
	                			codificacion2.append(np.array(agrupacion_cursos2))
	                			agrupacion_cursos1=[]
	                			agrupacion_cursos2=[]
	                			asignaturas_repetidas=[]

	        else:
	            contador_curso = 1
	            contador_carrera = len(carrera)*10 +10
	            numero_carreras[datos[0]] = contador_carrera
	            carrera[datos[0]] = {datos[1]: contador_carrera + contador_curso} # associate each course with its coefficient
	            numero_Car_Cur = carrera[datos[0]][datos[1]]

	            if (datos[4]=="1"):
	                agrupacion_cursos1.append(np.array([numero_profesor,numero_Car_Cur+numero_asignatura/1000, datos[6],int(datos[7]),int(datos[8]),asignaturas_repetidas,datos]))
	            
	            elif (datos[4]=="2"):
	            	agrupacion_cursos2.append(np.array([numero_profesor,numero_Car_Cur+numero_asignatura/1000,datos[6],int(datos[7]), int(datos[8]),asignaturas_repetidas,datos]))
	               	
	            else:
	                agrupacion_cursos1.append(np.array([numero_profesor,numero_Car_Cur+numero_asignatura/1000,datos[6], int(datos[7]),int(datos[8]),asignaturas_repetidas,datos]))
	                agrupacion_cursos2.append(np.array([numero_profesor,numero_Car_Cur+numero_asignatura/1000,datos[6],int(datos[7]), int(datos[8]), asignaturas_repetidas,datos]))
	            
	            
	            datos_index = np.where(np.all(opt_y_noopt == datos, axis=1))[0][0] #axis=1
	            
	            #Save course data in case the next subject is from another course.
	            if datos_index + 1 < len(opt_y_noopt):
	                	if datos[1] != opt_y_noopt[datos_index+1][1] or datos[0] != opt_y_noopt[datos_index+1][0] :
	                		if len(agrupacion_cursos1)>0 or len(agrupacion_cursos2)>0:
	                			codificacion1.append(np.array(agrupacion_cursos1))
	                			codificacion2.append(np.array(agrupacion_cursos2))
	                			agrupacion_cursos1=[]
	                			agrupacion_cursos2=[]
	                			asignaturas_repetidas=[]

	    if len(agrupacion_cursos1 )>0 or len(agrupacion_cursos2)>0:
	        codificacion1.append(np.array(agrupacion_cursos1))
	        codificacion2.append(np.array(agrupacion_cursos2))
	        agrupacion_cursos2 = []
	        agrupacion_cursos1 = []
	        asignaturas_repetidas=[]
	                   
	       	

	return np.array(codificacion1),np.array(codificacion2)
