import networkx as nx
import matplotlib.pyplot as plt
import codecs
import csv
import matplotlib.cm as cm
import matplotlib.colors
from networkx.drawing.layout import spring_layout

def getFile():
    file = open('LargestComponent_SNAP.txt', 'r')
    return file

def initializeFile():
    G = nx.Graph()
    file = getFile()
    for line in file:
        vertex1 = int(line.split()[0])
        vertex2 = int(line.split()[1])
        G.add_edge(vertex1, vertex2)
    return G

def storeAttrs(iter, G, char):
    attFile = codecs.open("SNAPattrs.csv", "r", "ISO-8859-1")
    reader = csv.reader(attFile)
    firstrow = True
    for line in reader:
        G.node[int(line[0])]['degree'] = int(line[1])
        G.node[int(line[0])]['Initial Proposer Values'] = float(line[2])
        G.node[int(line[0])]['stub'] = float(line[3])
        G.node[int(line[0])]['interactions'] = int(line[4])
        G.node[int(line[0])]['Final Proposer Values'] = float(line[5])
    return G

def drawPlot(G, value, iter, char):
    node_colors = []
    node_sizes = []
    i=0
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["green","red"])
    for node in G.nodes(data=True):
        i+=1
        try:
            print(node[1][value], i)
            # if(node[1][value] == 0):
            #     node_colors.append('navy')
            # elif(node[1][value] == 0.25):
            #     node_colors.append('blue')
            # elif(node[1][value] == 0.50):
            #     node_colors.append('green')
            # elif(node[1][value] == 0.75):
            #     node_colors.append('red')
            # elif(node[1][value] == 1):
            #     node_colors.append('darkred')
            # else:
            #     node_colors.append('black')
            node_colors.append(cmap(node[1][value]))
            node_sizes.append(node[1]['degree'])
        except KeyError:
            print(i)
    print(node_sizes)
    pos = spring_layout(G, random_state = 1337)
    #cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red","violet","blue"])
    #norm = plt.Normalize(0,1)
    nx.draw_networkx(G,pos=pos, with_labels=False, node_size = 15, node_color = node_colors)#[v*10 for v in node_sizes] , cmap=cmap, vmin=0, vmax=1)
    #plt.suptitle("Run for " + value + " for iteration: " + str(iter))
    plt.suptitle("SNAP")

    sm = plt.cm.ScalarMappable(cmap=cmap)
    sm._A = []
    plt.colorbar(sm)

    #plt.savefig("Plots/StarFixed" + char  + "/"  + value + str(iter) + ".png", dpi=1000)
    plt.savefig("SNAP" + char + ".png", dpi=1000)
    plt.clf()

def main():
    attrs = ['Final Proposer Values']
    chars = ['Final']
    # attrs = ['Initial Proposer Values']
    # chars = ['Initial']
    G = initializeFile()
    for char in chars:
            for value in attrs:
                G = storeAttrs(0+1, G, char)
                drawPlot(G, value, 0+1, char)

main()