# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 17:41:13 2018

@author: gaoyu
"""
from __future__ import division
from scipy import *
from pylab import *
from scipy.integrate import odeint      # Module de résolution des équations différentielles
from random import gauss
import numpy as np
import xlrd
import os
import scipy.optimize
from scipy import misc

import pyodbc
#############################

#######################
#connection = pyodbc.connect(r'Driver={SQL Server};Server=localhost;Database=equation;Trusted_Connection=yes;')
connection=pyodbc.connect(r'Driver={SQL Server};SERVER=exactcurefirstdb.cb9zgxqtumuv.eu-west-1.rds.amazonaws.com;DATABASE=RCPequation;UID=mbexactcure;PWD=ExactCurePower42')
cursor = connection.cursor()
cursor2=cursor.execute('SELECT  * FROM dbo.substance')
lst2=[]
for row in cursor2:
    lst2.append(row)

drugsname=lst2[0][0]

F =lst2[0][1]
t12 =lst2[0][2]
tmax =lst2[0][3] 
Vd =lst2[0][4]  
Cmax=lst2[0][5]
CL =lst2[0][6] 
kel=np.log(2)/t12

def f(x): #funtion to calculate ka
    y = (np.log(x)-np.log(kel))/(x-kel)-tmax
    return y

ka = scipy.optimize.fsolve(f, 2)[0]
#################################
connection = pyodbc.connect(r'Driver={SQL Server};Server=localhost;Database=equation;Trusted_Connection=yes;')
cursor = connection.cursor()
cursor1=cursor.execute('SELECT  intake,dose FROM dbo.intake_record')

lst1=[]
for row in cursor1:
    lst1.append(row)


d = []
intake = []

for i in range(len(lst1)):
    d.append(lst1[i][1])
    intake.append(lst1[i][0])

# Solving  
def deriv(syst, t):
    S = syst[0]                      
    Sc = syst[1]                                       
    dSdt= -ka*S
    dScdt= ka*S-kel*Sc
    return [dSdt, dScdt] # Derivatives

start = 0
end = int(48)
intake.append(end)
numsteps = 5*(end-start)
t = linspace(start,end,numsteps)

for i in range(len(lst1)):  
    if (i==0):
        S0 = d[0]*F
        Sc0=0
        syst_CI=array([S0,Sc0])         # Tableau des CI
        Sols=odeint(deriv,syst_CI,t[5*int(intake[i]):5*int(intake[i+1])])    # Résolution numérique des équations différentielles
    
        # Solutions' recovery
        S = Sols[:, 0]
        Sc = Sols[:, 1]
        
        #first maximum
        first_max = max(Sc)
 
    else:
        S0 = d[i]*F+S[-1]
        Sc0= Sc[-1]
        syst_CI=array([S0,Sc0])         # Tableau des CI
        Sols=odeint(deriv,syst_CI,t[5*int(intake[i]):5*int(intake[i+1])])    # Résolution numérique des équations différentielles

        # Solutions' recovery
        S = np.append(S, Sols[:,0], axis = None)
        Sc = np.append(Sc, Sols[:,1], axis = None) 
# Graph

if (Vd ==0 and CL==0 and Cmax==0):
    plot(t, Sc, color = 'green',label= drugsname)
    
    xlabel('time (h)')     # Label de l'axe des abscisses
    ylabel('quantite (mg)') # Label de l'axe des ordonnées
    legend()                                                # Appel de la légende
    show()

elif (Vd==0 and CL !=0):
    Vd = CL/kel
    plot(t, Sc/Vd, color = 'green',label= drugsname)
    
    xlabel('time (h)')     # Label de l'axe des abscisses
    ylabel('concentration (mg/L)') # Label de l'axe des ordonnées
    legend()                                                # Appel de la légende
    show()
    
elif (Vd==0 and Cmax !=0):
    Vd = first_max/Cmax
    plot(t, Sc/Vd, color = 'green',label= drugsname)
    
    xlabel('time (h)')     # Label de l'axe des abscisses
    ylabel('concentration (mg/L)') # Label de l'axe des ordonnées
    legend()                                                # Appel de la légende
    show()
    
elif (Vd!=0):
    plot(t, Sc/Vd, color = 'green',label= drugsname)
    
    xlabel('time (h)')     # Label de l'axe des abscisses
    ylabel('concentration (mg/L)') # Label de l'axe des ordonnées
    legend()                                                # Appel de la légende
    show()
    
    AUC = np.trapz

print('substance:',lst2[0],'    ','intake record(end:48)',lst1)


     
