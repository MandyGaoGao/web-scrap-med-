# -*- coding: utf-8 -*-

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

##############################
#####     PK DATA      #######
##############################

path = os.getcwd()+"\\pkParam\\name.xlsx"

# Opening
classeur = xlrd.open_workbook(path)

# All the sheets
sheets = classeur.sheet_names()

# First sheet
pkDrugInfo = classeur.sheet_by_name(sheets[0])

#Drug's name
'''
drugsname = pkDrugInfo.cell_value(3, 0)

# PK Parameters
pkParameters = classeur.sheet_by_name(sheets[1])
F = float(pkParameters.cell_value(3, 2))
t12 = float(pkParameters.cell_value(4, 2))
tmax = float(pkParameters.cell_value(5, 2))
Vd = float(pkParameters.cell_value(6, 2)) 
Cmax=float(pkParameters.cell_value(7, 2)) 
CL = float(pkParameters.cell_value(8, 2)) 

# Calibration 

kel=np.log(2)/t12
'''
def f(x): #funtion to calculate ka
    y = (np.log(x)-np.log(kel))/(x-kel)-tmax
    return y

ka = scipy.optimize.fsolve(f, 2)[0] ## the solver takes in argument a value which has to be close to the real value of ka


##############################
#####     SOLVING      #######
##############################

path = os.getcwd()+"\\contextual\\name_date.xlsx"

# Opening
classeur = xlrd.open_workbook(path)

# All the sheets
sheets = classeur.sheet_names()

# First sheet
contextFeatures = classeur.sheet_by_name(sheets[0])

# Dosage
d = []
intake = []
nrows = contextFeatures.nrows
for i in range(13, nrows):
    d.append(float(contextFeatures.cell_value(i, 2)))
    intake.append(float(contextFeatures.cell_value(i, 1)))

# Solving  
def deriv(syst, t):
    S = syst[0]                      
    Sc = syst[1]                                       
    dSdt= -ka*S
    dScdt= ka*S-kel*Sc
    return [dSdt, dScdt] # Derivatives

start = 0
end = int(contextFeatures.cell_value(8, 0))
intake.append(end)
numsteps = 5*(end-start)
t = linspace(start,end,numsteps)

for i in range(nrows-13):  
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
    
#        
    
# Graph

if (Vd ==0 and CL==0 and Cmax==0):
    plot(t, Sc, color = 'green',label= drugsname)
    
    xlabel('time (h)')     # Label de l'axe des abscisses
    ylabel('quantite (mg)') # Label de l'axe des ordonnées
    legend()                                                # Appel de la légende
    show()

elif (Vd==0 and CL !=0):
    Vd = CL/ke
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

