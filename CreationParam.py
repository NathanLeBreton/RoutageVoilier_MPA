# IMPORTS
import sys
import time
import os

chemin = "/home/nathan/TAL/Routage/Sources/NOISY_PAES/"

def creationParam(Seed,start,finish,Date,Stime,Polar,Weather,Noise,Gens,Alpha,Depth,outputfile):

    #on les écrit dans le fichier param qui sera lu par le programme C
    f = open(chemin+"paramsRoute", "w")
    
    lines = [Seed,start,finish,Date,Stime,Polar,Weather,Noise,Gens,Alpha,Depth,outputfile]
    f.writelines("%s\n" % l for l in lines)
    f.close()
    
    