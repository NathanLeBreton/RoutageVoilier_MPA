# IMPORTS
import sys
import time
import os

#from progress.bar import IncrementalBar
from haversine import haversine

"""
Genere la carte du monde avec une certaine precision

prune : precision
src_file : fichier source au format geojson genere par QGIS
output_file : fichier de sortie
nb_lines : nombre de lignes dans le fichier source. Uniquement pour l'affichage de la barre de progression
"""
def generate_map(prune, src_file, output_file):
    print("LAUNCHING MAP GENERATION ...")

    output_file = open(output_file, "w+")

    with open(src_file) as file:
        #A cause de la taille du fichier, on doit operer ligne par ligne
        line = file.readline()

        while line:
            #Liste des coordonnees d'une ligne
            coords_list = []
            #Liste des coordonnes que l'ont va ecrire
            to_write = []

            content_line = line.split()
            len_line = len(content_line)

            if len_line > 15:
                # Les donnees qui nous interresses commencent a l'index 15
                for x in range (15, len_line):
                    if content_line[x] not in ('[', '],', ']', '}', '},'):
                        #On ajoute les coordonnees a notre liste
                        coords_list.append(content_line[x].replace(',', ''))
                #On cree le premier point
                last_longitude = float(coords_list[0])
                last_latitude = float(coords_list[1])
                last_point = (last_latitude, last_longitude)

                #On recupere chaque coordonnees. Les données d'un point vont par paire
                for i in range(0, len(coords_list), 2):
                    #Donnes d'un point
                    longitude = float(coords_list[i])
                    latitude = float(coords_list[i + 1])
                    this_point = (latitude, longitude)

                    if haversine(last_point, this_point) > prune:
                        to_write.append(last_point)
                        #On met a jour le dernier point valide
                        last_longitude = longitude
                        last_latitude = latitude
                        last_point = this_point

                #On ajoute le dernier point de la ligne
                last_longitude = float(coords_list[len(coords_list)-2])
                last_latitude = float(coords_list[len(coords_list)-1])
                last_point = this_point
                to_write.append(last_point)

                #Si la liste des points a ecrire comporte plus qu'un seul point, alors on ecrit la ligne dans le fichier
                if len(to_write) >= 2:
                    for lat,lon in to_write:
                        data = str(lon) + ' ' + str(lat) + '\n'
                        output_file.write(data)
                    #On passe une ligne a la fin pour separer les formes entre elles
                    output_file.write('\n')
                else:
                    first_lon = float(coords_list[0])
                    first_lat = float(coords_list[1])
                    A = (first_lat, first_lon)
                    last_lon = float(coords_list[len(coords_list)-2])
                    last_lat = float(coords_list[len(coords_list)-1])
                    B = (last_lat, last_lon)
                    # Si les points ne sont pas trop proche l'un de l'autre on les ecrit
                    if haversine(A,B)>0.005:
                        #On ecrit les deux points de la liste
                        data = str(first_lon) + ' ' + str(first_lat) + '\n' + str(last_lon) + ' ' + str(last_lat) + '\n\n'
                        output_file.write(data)
                        output_file.write('\n')

            #On passe a la ligne suivante
            line = file.readline()
            #bar.next()
        #bar.finish()

"""
Verifie que les coordonnees sont comprises dans les bornes

data : les coordonnees d'un point
lonmax : longitude maximale
lonmin : longitude minimale
latmax : latitude maximale
latmin : latitude minimale
"""
def check(data, lonmax, lonmin, latmax, latmin):
    # lonmin < lon < lonmax latmin < lat < latmax
    if float(lonmin) < float(data[0]) and float(data[0]) < float(lonmax) and float(latmin) < float(data[1]) and float(data[1]) < float(latmax):
        return True
    return False

"""
Genere une carte bornee

world_map : carte du monde generee au prealable
lonmax : longitude maximale
lonmin : longitude minimale
latmax : latitude maximale
latmin : latitude minimale
output_file : fichier de resultat
nb_lines : nombre de lignes dans le fichier source. Uniquement pour l'affichage de la barre de progression
"""
def generate_borned_map(lonmax, lonmin, latmax, latmin):
    
    '''
    print(lonmax)
    print(lonmin)
    print(latmax)
    print(latmin)
    '''

    lonmax = float(lonmax)
    lonmin = float(lonmin)

    latmax = float(latmax)
    latmin = float(latmin)

    output_file = open("background.dat", "w+")


    with open("world_map.dat") as f:

        line = f.readline()

        last_check = False

        while line:
            
            data = line.split()


            if len(data) > 1 and check(data, lonmax, lonmin, latmax, latmin):
                    print("ok")	
                    output_file.write(line)
                    last_check = True
            else:
                if last_check == True:
                    output_file.write("\n")
                last_check = False

            line = f.readline()
            #bar.next()
        #bar.finish()
        print("generetation fond carte OK")

"""
Recupere les parametres de la route

param_file : fichier de parametre de la route
"""
def read_params(param_file):
    print("LOADING PARAMETERS FROM FILE ...")
    with open(param_file) as f_params:

        #Premiere ligne
        f_params.readline()
        #Ligne contenant les coordonnees du point de depart
        start = f_params.readline()
        #Ligne contenant les coordonnees du point d'arrivee
        end = f_params.readline()

        content_start = start.split()
        content_end = end.split()

        lat_start = float(content_start[1])
        lon_start = float(content_start[2])

        lat_end = float(content_end[1])
        lon_end = float(content_end[2])

        if lat_start > lat_end:
            latmax = lat_start
            latmin = lat_end
        else :
            latmax = lat_end
            latmin = lat_start

        if lon_start > lon_end:
            lonmax = lon_start
            lonmin = lon_end
        else:
            lonmax = lon_end
            lonmin = lon_start
        
    print("DONE")
    return float(lonmax), float(lonmin), float(latmax), float(latmin)

"""
genere la route a partir du fichier de la route

route_file : fichier de la route
output : fichier de resultat
"""
def generate_route(route_file, output):
    print("GENERATING ROUTE ...")
    with open(route_file) as rf:
        # premiere ligne du fichier
        line = rf.readline()

        # On lit le fichier ligne par ligne
        while line:
            content = line.split()
            if len(content) > 8:
                # Du au format du fichier de parametres de la route
                if content[0] != "##":
                    lat = content[8]
                    lon = content[9]
                    data = str(lon) + " " + str(lat) + "\n"
                    output.write(data)
                else:
                    # On separe les formes
                    output.write('\n')
            # On change de ligne
            line = rf.readline()
    print("DONE ...")

"""
Fusionne le fichier de la carte bornee et celui de la route
"""
def merge(result_map, route):
    command = "gnuplot -e \'set size ratio -1; plot \""+str(result_map)+"\" w l, \""+str(route)+"\" with line linecolor rgb \"red\"\' -persist"
    os.system(command)

        

def main(lonmax, lonmin, latmax, latmin, prune, src_file, route_file, dest_dir):

    print("LANCEMENT PROGRAMME ROUTAGE")     

    src_file = src_file.replace(" ", "").replace("\'", "")
    route_file = route_file.replace(" ", "").replace("\'", "")
    dest_dir = dest_dir.replace(" ", "").replace("\'", "")

    # Creation des fichiers de sortie
    world_map = open(dest_dir + "/world_map.dat", "w+")
    result_map = open(dest_dir + "/background.dat", "w+")
    route = open(dest_dir + "/route.dat", "w+")

    #Uniquement necessaire pour l'affichage de la progression du programme
    nb_lines = 0
    with open(src_file) as of:
        line = of.readline()
        while line:
            nb_lines += 1
            line = of.readline()

    generate_map(prune, src_file, world_map)

    gen_world = dest_dir + "/world_map.dat"
    #Uniquement necessaire pour l'affichage de la progression du programme
    nb_lines = 0
    with open(gen_world) as of:
        line = of.readline()
        while line:
            nb_lines += 1
            line = of.readline()

    start_time = time.time()
    generate_borned_map(gen_world, lonmax, lonmin, latmax, latmin, result_map)

    generate_route(route_file, route)
    
    gen_route = dest_dir + "/route.dat"
    gen_map = dest_dir + "/background.dat"
    merge(gen_map, gen_route)

    print("FIN PROGRAMME ROUTAGE")  


'''
def main(args):
#lonmax, lonmin, latmax, latmin, prune, src_file, route_file, dest_dir
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-lonmax", "--lonmax", type=float, default= 2, required=False)
    parser.add_argument("-lonmin", "--lonmin", type=float, default= 4, required=False)
    parser.add_argument("-latmax", "--latmax", type=float, default= 4, required=False)
    parser.add_argument("-latmin", "--latmin", type=float, default= 4, required=False)
    parser.add_argument("-prune", "--prune", type=str, default= 4, required=False)
    parser.add_argument("-src_file", "--src_file", type=str, default= 4, required=False)
    parser.add_argument("-route_file", "--route_file", type=str, default= 4, required=False)
    parser.add_argument("-dest_dir", "--dest_dir", type=str, default= 4, required=False)

    args = parser.parse_args(args)

    longmax = args.lonmax
    lonmin = args.lonmin
    latmax = args.latmax
    prune = args.prune
    
    src_file = args.src_file.replace(" ", "").replace("\'", "")
    route_file = args.route_file.replace(" ", "").replace("\'", "")
    dest_dir = args.dest_dir.replace(" ", "").replace("\'", "")

    # Creation des fichiers de sortie
    world_map = open(dest_dir + "/world_map.dat", "w+")
    result_map = open(dest_dir + "/background.dat", "w+")
    route = open(dest_dir + "/route.dat", "w+")

    #Uniquement necessaire pour l'affichage de la progression du programme
    nb_lines = 0
    with open(src_file) as of:
        line = of.readline()
        while line:
            nb_lines += 1
            line = of.readline()

    generate_map(prune, src_file, world_map, nb_lines)

    gen_world = dest_dir + "/world_map.dat"
    #Uniquement necessaire pour l'affichage de la progression du programme
    nb_lines = 0
    with open(gen_world) as of:
        line = of.readline()
        while line:
            nb_lines += 1
            line = of.readline()

    start_time = time.time()
    generate_borned_map(gen_world, lonmax, lonmin, latmax, latmin, result_map, nb_lines)

    generate_route(route_file, route)
    
    gen_route = dest_dir + "/route.dat"
    gen_map = dest_dir + "/background.dat"
    merge(gen_map, gen_route)

'''

if __name__ == '__main__':
    main(sys.argv[1:])