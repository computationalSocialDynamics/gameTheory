from src.Node import Node
from random import random
from pprint import pprint

def getFile():
    file = open('edgelists/Random_Network_Distributed.txt', 'r')
    return file

def comfortFile():
    file = open("ComfortValues.csv",'r')
    return file

def getComfortValues():
    comfortfile = comfortFile()
    comfortValues = [float(line.split()[0]) for line in comfortfile]
    return comfortValues

def getNumberOfNodes():
    file = getFile()
    nodesAsListFirstColumn = [int(line.split()[1]) for line in file]
    file.seek(0)
    nodesAsListSecondColumn = [int(line.split()[0]) for line in file]
    numberOfNodes = max(max(nodesAsListFirstColumn), max(nodesAsListSecondColumn))
    return numberOfNodes

def createNodes():
    numberOfNodes = getNumberOfNodes()
    '''numberOfNodes + 2 to take care of indexing purposes, we just want nodes from index 1 to number of nodes'''
    nodeObjectsAsList = [Node(i-1) for i in range(1,numberOfNodes+2)]
    return nodeObjectsAsList

def getNodes():
    file = getFile()
    players = createNodes()
    dummyPlayer = True

    for line in file:
        vertex1 = int(line.split()[0])
        vertex2 = int(line.split()[1])
        try:
            players[vertex1].neighbors.append(vertex2)
            players[vertex2].neighbors.append(vertex1)
            players[vertex1].degree += 1
            players[vertex2].degree += 1
        except IndexError:
            continue
    comfortValues = getComfortValues()
    iter = 0
    for player in players:
        if(dummyPlayer):
            dummyPlayer = False
            continue

        '''if player.label >= 1 and player.label <= 7:
            player.comfort = 0.5
        if player.label >= 8 and player.label <= 14:
            player.comfort = 0.25
        if player.label >= 15 and player.label <=21:
            player.comfort = 1
        if player.label >= 22 and player.label <=28  :
            player.comfort = 0.75
        if player.label >=29:
            player.comfort = 0'''
        player.stubbornness = round(random(), 5)
        player.comfort = comfortValues[iter]
        #player.comfort = round(random(), 5)
        #player.stubbornness = round(random(), 5)

        #player.comfort = round(random(),5)
        #round to nearest 0.25
        comfort = player.comfort
        player.comfort = round(comfort*4)/4

        #appending twice as indexing starts from 0, which will be ignored
        [player.offeror_value.append(player.comfort) for _ in range(2)]
        [player.acceptor_value.append(player.comfort) for _ in range(2)]

        #general_loss = comfort - player.comfort

        '''if general_loss > 0:
            player.offeror_positive_loss_count = player.acceptor_positive_loss_count = 1
            player.offeror_positive_loss = player.acceptor_positive_loss = abs(general_loss)
        else:
            player.offeror_negative_loss_count = player.acceptor_negative_loss_count = 1
            player.offeror_negative_loss = player.acceptor_negative_loss = abs(general_loss)'''

        player.offerer_steps.append(player.comfort)
        player.acceptor_steps.append(player.comfort)
        iter+=1

    '''the first node is a dummy node not used anywhere (has to be here because indexing starts from 0'''
    players[0].label = 'dummy'
    return players

'''uncomment the below lines and only run this file to view a node's structure. Note that we have a node with label 0 
because indexing starts from 0. It will be ignored throughout the system'''

#players = getNodes()
#pprint(vars(players[1]))



