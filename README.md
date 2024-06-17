# Automatic-Methods-for-University-Timetable-Creation


This repository contains the programs used in my Bachelor's thesis in Electronic Engineering, focusing on the study and implementation of automatic methods for creating university timetables. Throughout this project, various techniques and algorithms were explored to optimize the allocation of classes, rooms, and resources, aiming to improve the efficiency and organization of academic schedules. Four methods have been used: Tabu search, Greedy Algorithm, Linear Programming, and Simulated Annealing.

## Repository Contents

In the repository you will find different algorithms created for automating these schedules. All of them utilize data from the file 'Datos EHu.csv', which includes data from the Physics and Electronic Engineering degrees at the Faculty of Science and Technology of UPV/EHU. 

Each folder contains programs corresponding to its name.To run the different algorithms, you need to run the programs found in the folders with the same name. In the case of the greedy algorithm, you need to run the program called 'Programa_Voraz.py', since 'Algoritmo_Voraz.py' is a module that obtains the greedy solution but is also used by other programs. The four algorithms create an Excel file as output with the weekly schedule.

The programs 'Tabu.py', 'Simulated_Anneling.py', and 'Programa_Voraz.py' use the module 'Pasar_excel.py' to convert results to Excel format. These three programs and 'Programacion_Lineal.py' utilize the module 'Lectura_de_datos.py' to read files from 'Datos EHU.csv'.

Additionally, 'Tabu.py', 'Simulated_Anneling.py', and 'Programa_Voraz.py' utilize 'Algoritmo_Voraz.py', which creates the greedy solution that serves as the basis for both Simulated Annealing and Tabu Search.

## Libraries required


To run the programs, you need to install the following Python libraries: Pandas, Pulp, Openpyxl, Random, and Numpy.



## Author

This work was carried out by Jon Gómez Manchola as part of the requirements for obtaining a degree in Electronic Engineering at UPV/EHU.

