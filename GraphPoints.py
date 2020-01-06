# IMPORTS
import sys
import time
import os

def routePrincipale(): 
    #le meilleur chemin :
    with open("noisy_isofront.dat", "r") as ins:
        arrayTime = []
        arrayStress = []
        for line in ins:
            cdc = line
            maListe = cdc.split(" ")       
            for i in range(len(maListe)):
                try:
                    maListe[i] = float(maListe[i]) 
                except : 
                    pass
                arrayTime.append(maListe[0])
                arrayStress.append(maListe[1])
     
    
    if val : 
        sourceMeilleurCheminPoint = ColumnDataSource(data=dict(x=arrayTime, y=arrayStress)) 

        # Draw the coordinates as circles
        fig1.circle('x', 'y',source=sourceMeilleurCheminPoint,
                   color='blue', size=10, alpha=0.5,
                   legend='Meilleur chemin')
    else:
        sourceMeilleurCheminPoint.data = dict(x=arrayTime, y=arrayStress)
        
        
        
def autreRoutes():
    tabPoint = []
    #autres chemins
    num=0
    with open("noisy_front.dat", "r") as ins:
        arrayTime = []
        arrayStress = []
    
        
        #Je reset toutes les sources pour effacer les anciens chemins 
        for i in range(len(tabPoint)):           
            tabPoint[i].data = dict(x=arrayTime, y=arrayStress) 
        
        for line in ins:
            cdc = line
            maListe = cdc.split(" ")
            for j in range(len(maListe)-1):
                    try :
                        maListe[j] = float(maListe[j]) 
                    except:
                        pass
                    arrayTime.append(maListe[0])
                    arrayStress.append(maListe[1])                    
                    
                    s = ColumnDataSource(data=dict(x=arrayTime, y=arrayStress))  
                    tabPoint.append(s)
                    
                    arrayTime = []
                    arrayStress = []
                    
                    
    #on place les points en parcourant le tableau             
    for i in range(len(tabPoint)):
        nom = 'point'+str(i)
        fig1.circle('x', 'y',source=tabPoint[i],
                    color='black', size=5, alpha=0.5, name=nom)    