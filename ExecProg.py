# IMPORTS
import sys
import time
import os
import ctypes as ct

import os.path
from os import path

chemin = "/home/nathan/TAL/Routage/Sources/NOISY_PAES/"
cheminMeteo = "/home/nathan/TAL/grib/"
cheminPolar = "/home/nathan/TAL/polar/"

def polar(polar) :

    os.chdir(cheminPolar)
    print(polar)
    print(cheminPolar+polar+".dat")
    isExist = path.exists(cheminPolar+polar+".dat")
    print(isExist)
    if not isExist : 
        #si non : on converti le .xml en .dat
        #on lance la librairie partagée en passant le fichier voulu en parametre 
        _lib = ct.cdll.LoadLibrary(cheminPolar+"xmlToDat.so")
        main_func = _lib.lib_main
        main_func.argtypes = [ct.c_char_p]
        main_func.restype = ct.c_int
        # https://docs.python.org/3/library/ctypes.html#calling-functions
        param = "{}.xml".format(polar)
        result = main_func(str.encode(param))
    
    
    
def grib(weather) :   
    
    os.chdir(cheminMeteo)
    print(weather)
    print(cheminMeteo+weather+".isoc")
    isExist = path.exists(cheminMeteo+weather+".isoc")
    print(isExist)
    if not isExist : 
        #si non : on converti le .grib en .isoc
        print("./gribfile/{}.grb".format(weather))
        #on lance la librairie partagée en passant le fichier voulu en parametre 
        _lib = ct.cdll.LoadLibrary(cheminMeteo+"grib2isoc2.so")
        main_func = _lib.lib_main
        main_func.argtypes = [ct.c_char_p]
        main_func.restype = ct.c_int
        # https://docs.python.org/3/library/ctypes.html#calling-functions
        param = "./gribfile/{}.grb".format(Weather)
        result = main_func(str.encode(param))
        
        
        
def calculRoutes():
    os.chdir(chemin)
    
    print()
    print("lancement programme de calcul des routes : ")
    print()
     
    #on lance le programme C comme librairie partagée en passant le fichier "paramsRoute" en parametre 
    _lib = ct.cdll.LoadLibrary(chemin+"noisypaes.so")
    main_func = _lib.lib_main
    main_func.argtypes = [ct.c_char_p]
    main_func.restype = ct.c_int
    # https://docs.python.org/3/library/ctypes.html#calling-functions
    result = main_func(b"paramsRoute")
    
    print()
    print("fin programme de calcul des routes.")
    print()