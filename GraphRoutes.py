# IMPORTS
import sys
import time
import os

def routePrincipale():
    #le meilleur chemin :         
    tailleList = 0         
    with open("noisy_iso.dat", "r") as ins:
        arrayLat = []
        arrayLong = []
        arrayDist = []
        arrayTime = []
        for line in ins:
            cdc = line
            maListe = cdc.split(" ")
            tailleList = tailleList+1
            #on lit seulement les lignes qui contiennent des données
            if maListe[0] == '\n':
                break
            elif maListe[0] != '##':
                for j in range(len(maListe)):
                    #print("value : " + maListe[j])
                    maListe[j] = float(maListe[j]) 
                arrayLat.append(maListe[8])
                arrayLong.append(maListe[9])
                arrayDist.append(maListe[5])
                arrayTime.append(maListe[7])         
      
    with open("noisy_isofront.dat", "r") as ins:
        arrayStress = []
        for line in ins:
            cdc = line
            maListe = cdc.split(" ")       
            for i in range(len(maListe)):
                try:
                    maListe[i] = float(maListe[i])
                except: 
                    pass
            for i in range (1,tailleList-2):
                arrayStress.append(maListe[1])   

                
    '''
    #if premiere exec : création source, puis création de la ligne 
    if val < 1 :
        sourceMeilleurCheminLigne = ColumnDataSource(data=dict(x=arrayLong, y=arrayLat, dist=arrayDist, 
                                         time=arrayTime, stress=arrayStress)) 

        #on creer la ligne du meilleur chemin
        fig.line('x','y',source=sourceMeilleurCheminLigne, 
                 color='blue', line_width=3,
                 legend='Meilleur chemin')
    
    #sinon : on met juste a jour la source
    else:
        sourceMeilleurCheminLigne.data = dict(x=arrayLong, y=arrayLat, 
                                              dist=arrayDist, time=arrayTime, stress=arrayStress) 
      
    '''
    
def autreRoutes():
    #autres chemins 
    tabStress = []
    with open("noisy_front.dat", "r") as ins:
        num = 1
        for line in ins:
            cdc = line
            maListe = cdc.split(" ")
            for j in range(len(maListe)):
                try:
                    maListe[j] = float(maListe[j])
                except:
                    pass
                tabStress.append(maListe[1])  
    
    
    tabChemin = []
    val = 0
    with open("noisy_ps.dat", "r") as ins:
        arrayDist = []
        arrayTime = []
        arrayLat = []
        arrayLong = []
        arrayStress = []
        
        #Je reset toutes les sources pour effacer les anciens chemins 
        for i in range(len(tabChemin)):           
            tabChemin[i].data = dict(x=arrayLong, y=arrayLat, dist=arrayDist,time=arrayTime) 
        
        
        for line in ins:
            cdc = line
            maListe = cdc.split(" ")
            #if maListe est vide : ligne blanche
            if maListe[0] == '\n':
                #si array deja vide on fait rien
                #sinon on affiche la ligne et on reset les 2 array
                if len(arrayLat)!=0 and len(arrayLong)!=0 :                        
                    
                    for i in range(len(arrayLat)):                    
                        arrayStress.append(tabStress[val])
                        
                    val = val+1
                    
                           
                    s = ColumnDataSource(data=dict(x=arrayLong, y=arrayLat, dist=arrayDist,
                                               time=arrayTime, stress=arrayStress))  
                    tabChemin.append(s)
                    
                         
                    arrayDist = []
                    arrayTime = []
                    arrayLat = []
                    arrayLong = []
                    arrayStress = []  
                    
            #on lit seulement les lignes qui contiennent des données
            if maListe[0] != '##' and maListe[0] != '\n':          
                for j in range(len(maListe)):
                    maListe[j] = float(maListe[j]) 
                #on extrait les x et y 
                arrayLat.append(maListe[8])
                arrayLong.append(maListe[9])
                arrayDist.append(maListe[5])
                arrayTime.append(maListe[7])
                
    
    #on trace les chemins en parcourant le tableau             
    for i in range(len(tabChemin)):
        nom = 'line'+str(i)
        fig.line('x', 'y', source=tabChemin[i], color='black', line_width=0.5, name=nom)            
                
