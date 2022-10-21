#si vous arrivez pas à dl PIL/Pillow dans les settings entrez dans le terminal les commandes suivantes :
#pip install --upgrade pip
#pip install --upgrade Pillow
from PIL import Image, ImageDraw


f = open("data/metro.txt", "r",encoding='utf-8')
f2 = open("data/metro.txt", "r",encoding='utf-8')
f3 = open("data/pospoints.txt","r",encoding='utf-8')
x = open("data/pospoints.txt")
s=x.read().replace("@", " " )
x.close()

x=open("data/pospoints.txt","w")
x.write(s)
x.close


#input f3
#output return a matrix with the coordinates of each station
def matrixééééé(f):
    d=[]
    for line in f:
        line = line.rstrip('\n') #delete the \n at the end of each line
        x = line.split(";")#create a tuple without ;
        d.append(x)
    return d

matrix_point= matrixééééé(f3)


# Read a line and return an array with the info given in the line
# V 0000 Abbesses ;12 ;False 0 -> ["Abbesses","12","False","0"]

def key_name_value_int(dico):
    dico1= {}
    for line in dico.items():
        dico1.update({line[1][0]:line[0]})

    return dico1


def read_v(line):
    number = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    arr = [""] * 4
    i = 7
    j = 0
    trigger = True
    if line[0] == "V":
        while j != 3:   # j is the index of the array we are filling with our information
            if line[i] in number and trigger:   # Whenever we go from words to a number and vice-versa
                trigger = False                 # we increment the index
                j += 1
                arr += []
            if line[i] not in number and not trigger:
                trigger = True
                j += 1
                arr += []
            arr[j] += line[i]
            i += 1
        arr[0] = arr[0][:-2]    # We delete unwanted characters like ";" or spaces
        arr[2] = arr[2][2:-1]
        return arr


# Read a line and return an array with the info given in the line
# E 0 238 41 -> [0,238,41]
def read_e(line):
    j = 0
    arr = [""] * 3
    for i in range(len(line))[2:]:
        if line[i] == " " and j <= 1:
            arr[j] = int(arr[j])
            j += 1
            arr += []
        else:
            arr[j] += line[i]
    arr[j] = int(arr[j])
    return arr

# Take a file in parameter and ant return a dico
# {item = index of the station:
#  value = station infos in an array}
# V 0185 Maisons-Alfort les Juilliottes ;8 ;False 0
# {185 : {['Maisons-Alfort les Juilliottes', '8', 'False', '0']}, 186 : {['Maison Alfort, Stade', ...] ...}
def init_station(f):
    i = 0
    dico = {}
    for line in f:
        if line[0] == "E": break
        dico[i] = read_v(line)
        i += 1
    return dico

# Take a file in parameter and ant return a dico of dico
# {item = index of the station :
#  value = a dico {item  = index of the destination :
#                 value = time to go to the destination}}
# E 189 367 49
# [189, 367, 49]
# {189 : {367: 49}, 190 : {...}, ...}
#
# where we come from == 189
# where we can go    == 367
# how long it takes  == 49

def init_map(f):
    dico = {}
    for i in range(376):    # initialize the dico dico
        dico[i] = {}
    for line in f:
        if line[0] == "E":
            leg = read_e(line)
            dico[int(leg[0])][int(leg[1])] = int(leg[2])    # the graph is non oriented so we give it add the path two times
            dico[int(leg[1])][int(leg[0])] = int(leg[2])
    return dico


# dico = (init_station(f))
dico = init_map(f)

def dicoDjikstra(dico,s,fin):

    infini = sum(sum(dico[s1][s2] for s2 in dico[s1]) for s1 in dico) + 1
    s_connu = {s:[0,[s]]}
    s_inconnu = {k:[infini,''] for k in dico if k!=s}
    for suivant in dico[s]:
        s_inconnu[suivant] = [dico[s][suivant],s]

    while s_inconnu and any(s_inconnu[k][0] < infini for k in s_inconnu):
        u=min(s_inconnu, key=s_inconnu.get)
        longueur_u,precedent_u=s_inconnu[u]

        for v in dico[u]:
            if v in s_inconnu:
                d= longueur_u + dico[u][v]
                if d<s_inconnu[v][0]:
                    s_inconnu[v]=[d,u]


        s_connu[u]=[longueur_u, s_connu[precedent_u][1]+[u]]

        del s_inconnu[u]
    for key in s_connu.keys():
        if key == fin:
            return s_connu[key]


dico2 = init_station(f2)
#input dico : dico with station's name from init_station, line : line of a station,path from dicoDjikostra,station's number
#output : return the name of the terminus of line


def direction_of(dico_w_name,line,path,stations_number):
    for i in range(len(dico_w_name)):
        if line==int(dico_w_name[i][1]) and  dico_w_name[i][2]=='True': #check if it's a terminus or not
            path1 = dicoDjikstra(dico,stations_number,i) #get the path from the starting point (stations_number) to the terminus
            new_path1 = path1[1][1:]
            new_path = path[1][1:]
            print(new_path)
            print(new_path1)
            print("ligne =", line)
            for line1 in new_path: #check if it's the right terminus by comparing the 2 paths
                for line2 in new_path1:
                    if line1 ==line2:
                        return dico_w_name[i][0]


#input : dico : dico with station's name from init_station, dico1 from init_map, path from dicoDjkstra, example on how to call the function :
#               read_itinary(dico2,dicoDjikstra(dico,3,5))
#output : print the whole itinary from summit A to summit B
def read_itinary(dico_w_name,path):
    print("Temps estimé :",path[0],"secondes")
    depart_ligne = int(dico_w_name[path[1][0]][1])
    print("Vous prenez la station ",dico_w_name[path[1][0]][0],"ligne",depart_ligne,"direction",direction_of(dico_w_name,depart_ligne,path,path[1][0]))
    for i in range(len(path[1])):
        depart_apres = int(dico_w_name[path[1][i]][1])
        if depart_ligne!=depart_apres:
            depart_ligne = depart_apres
            print("Vous devez descendre à la station",dico_w_name[path[1][i]][0],"puis prendre la ligne",depart_apres,"direction",direction_of(dico_w_name,depart_ligne,path,path[1][i]))
    print("Vous êtes arrivé à la station",dico_w_name[path[1][len(path[1])-1]][0],"ligne",depart_ligne)


#input path from point a to point b
#output drawing of the path

def drawing_path(path):
    im = Image.open("data/metrof_r.png")
    img1 = ImageDraw.Draw(im)
    for i in range(len(path[1])-1):
        a = get_coordinate(path[1][i])
        b= get_coordinate(path[1][i+1])
        shape = [(int(a[0]),int(a[1])),(int(b[0]),int(b[1]))]
        img1.line(shape,fill = "black",width=3)
    im.show()


#input number of the station
#output coordinates of the station
def get_coordinate(a):
    for i in range(len(matrix_point)): #
        if matrix_point[i][2]==dico2[a][0]:
            return matrix_point[i][:2]


dico_key_name = key_name_value_int(dico2)
already_processed = []
weighted_edges = []

# creating edges (u, v, w) with the dico data structure
for key, value in dico.items():
    for inner_key, inner_value in value.items():
        edge_A_to_B = (key, inner_key)
        edge_B_to_A = (inner_key, key)
        if edge_A_to_B not in already_processed and edge_B_to_A not in already_processed:
            # add in list
            already_processed.append(edge_A_to_B)
            already_processed.append(edge_B_to_A)

            # add weight to edges
            weighted_edges.append((edge_A_to_B[0], edge_A_to_B[1], inner_value))

# sort edges
weighted_edges.sort(key=lambda y: y[2])


def kruskal(weighted_edges):
    ACPM_nodes = []
    ACPM_edges = []
    ACPM_weight: int = 0

    # initialise data structures
    ACPM_nodes.append(weighted_edges[0][0])
    ACPM_nodes.append(weighted_edges[0][1])
    ACPM_edges.append(weighted_edges[0])
    ACPM_weight = weighted_edges[0][2]

    # complete data structures
    for edge in weighted_edges:
        new_node_nbr_A: int = edge[1]
        new_node_nbr_B: int = edge[0]
        new_edge_weight: int = edge[2]

        # trivial case :
        if new_node_nbr_A not in ACPM_nodes:
            ACPM_nodes.append(new_node_nbr_A)
            ACPM_edges.append(edge)
            ACPM_weight = ACPM_weight + new_edge_weight
        elif new_node_nbr_B not in ACPM_nodes:
            ACPM_nodes.append(new_node_nbr_B)
            ACPM_edges.append(edge)
            ACPM_weight = ACPM_weight + new_edge_weight

        # case where node already in ACPM_nodes :
        if (
                new_node_nbr_A not in ACPM_nodes and
                new_node_nbr_B in ACPM_nodes
        ):
            ACPM_nodes.append(new_node_nbr_A)
            ACPM_edges.append(edge)
            ACPM_weight = ACPM_weight + new_edge_weight
        elif (
                new_node_nbr_B not in ACPM_nodes and
                new_node_nbr_A in ACPM_nodes
        ):
            ACPM_nodes.append(new_node_nbr_B)
            ACPM_edges.append(edge)
            ACPM_weight = ACPM_weight + new_edge_weight

        # when number of edges in ACPM is equal to number of nodes in graph -1
        if len(ACPM_edges) >= (len(dico.keys()) - 1):
            print('Number of edges in the ACPM :', len(ACPM_edges))
            print('Weight of the ACPM :', ACPM_weight)
            break

    # assertion if condition is not complete
    assert (len(ACPM_edges) == (len(dico.keys()) - 1))
    return ACPM_edges

def drawing_ACPM(ACPM):
    im = Image.open("data/metrof_r.png")
    img1 = ImageDraw.Draw(im)

    for i in range(len(ACPM)-1):
        a = get_coordinate(ACPM[i][0])
        b= get_coordinate(ACPM[i][1])
        shape = [(int(a[0]), int(a[1])), (int(b[0]), int(b[1]))]
        img1.line(shape, fill="black", width=3)

    im.show()

#fonction test
def test():
    for i in range(376):
        if get_coordinate(i) is not None:
            print(get_coordinate(i))
        else:
            print(i)
    for i in range(len(matrix_point)):
        print(matrix_point[i],i)
    print(dico2[152])

if __name__ == '__main__':
    print(dicoDjikstra(dico,4,13))
    read_itinary(dico2,dicoDjikstra(dico,4,13))
    drawing_path(dicoDjikstra(dico, 4, 13))



