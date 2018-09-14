from NodesProvider import getNodes
from NodesProvider import getNumberOfNodes
from WriteToFile import writeToFile
from random import randint
from random import random
import time
import math
from pprint import pprint

start_time = time.time()

'''initialize members for the game'''
window = 1
players = getNodes()
number_of_players = getNumberOfNodes()
offerer_list = [0]
acceptor_list = [0]
success_by_iter = []
failure_by_iter = []
sensitivity_list = []

'''set the weight or the strength between edges'''
link_strength = [[0.5 for y in range(number_of_players+1)] for x in range(number_of_players+1)]


'''Start game'''
def playGame(total_number_of_iterations):
    iterVal = 1
    iteration = 1
    global players
    '''setting all successess and failures by iteration as false initially'''
    global success_by_iter
    global failure_by_iter
    success_by_iter = [False for i in range(total_number_of_iterations+1)]
    failure_by_iter = [False for i in range(total_number_of_iterations+1)]

    while iteration <= total_number_of_iterations:
        offeror = randint(1,number_of_players)
        acceptor = randint(1,number_of_players)
        sensitivity = 0.5
        sensitivity_list.append(sensitivity)
        if(acceptor in players[offeror].neighbors):
            offerer_list.append(offeror+1)
            acceptor_list.append(acceptor+1)
            players[offeror].offeror_count += 1
            players[acceptor].acceptor_count += 1

            '''Update previous offeror values to nearest discretized value based on sensitivity; also update losses with direction'''
            updateValuesAndLosses(acceptor, iterVal, offeror, sensitivity)

            '''Check if success or failure'''
            checkConditionAndPerformActions(acceptor, iterVal, offeror, sensitivity)
            iterVal += 1
            iteration += 1
            
            if iterVal == 10000:
                players = refreshPlayersAndStoreSteps(players)
                iterVal = 1

    return players


def checkConditionAndPerformActions(acceptor, iterVal, offeror, sensitivity):

    '''Underlying model equation'''
    if (abs(players[offeror].offeror_value[iterVal] - players[acceptor].acceptor_value[iterVal])) < (
            window * link_strength[offeror][acceptor] * sensitivity):
        onSuccess(acceptor, iterVal, offeror)
    else:
        onFailure(acceptor, iterVal, offeror, sensitivity)
    updateOthers(acceptor, iterVal, offeror)


def updateValuesAndLosses(acceptor, iterVal, offeror, sensitivity):

    cur_offeror_val = players[offeror].offeror_value[iterVal]
    if cur_offeror_val >= sensitivity:
        players[offeror].offeror_value[iterVal] = math.ceil(cur_offeror_val * 4) / 4
    else:
        players[offeror].offeror_value[iterVal] = math.floor(cur_offeror_val * 4) / 4

    cur_offeror_loss = cur_offeror_val - players[offeror].offeror_value[iterVal]
    if cur_offeror_loss > 0:
        players[offeror].offeror_positive_loss_count += 1
        players[offeror].offeror_positive_loss = (((players[offeror].offeror_positive_loss_count - 1) *
                                                   players[offeror].offeror_positive_loss) + (
                                                  abs(cur_offeror_loss))) / (
                                                 players[offeror].offeror_positive_loss_count)
    else:
        players[offeror].offeror_negative_loss_count += 1
        players[offeror].offeror_negative_loss = (((players[offeror].offeror_negative_loss_count - 1) *
                                                   players[offeror].offeror_negative_loss) + (
                                                  abs(cur_offeror_loss))) / (
                                                 players[offeror].offeror_negative_loss_count)

    cur_acceptor_val = players[acceptor].acceptor_value[iterVal]
    if (cur_acceptor_val >= sensitivity):
        players[acceptor].acceptor_value[iterVal] = math.ceil(cur_acceptor_val * 4) / 4
    else:
        players[acceptor].acceptor_value[iterVal] = math.floor(cur_acceptor_val * 4) / 4

    cur_acceptor_loss = cur_acceptor_val - players[acceptor].acceptor_value[iterVal]
    if cur_acceptor_loss > 0:
        players[acceptor].acceptor_positive_loss_count += 1
        players[acceptor].acceptor_positive_loss = (((players[acceptor].acceptor_positive_loss_count - 1) *
                                                     players[acceptor].acceptor_positive_loss) + (
                                                    abs(cur_acceptor_loss))) / (
                                                   players[acceptor].acceptor_positive_loss_count)
    else:
        players[acceptor].acceptor_negative_loss_count += 1
        players[acceptor].acceptor_negative_loss = (((players[acceptor].acceptor_negative_loss_count - 1) *
                                                    players[acceptor].acceptor_negative_loss) + (
                                                   abs(cur_acceptor_loss))) / (
                                                  players[acceptor].acceptor_negative_loss_count)


'''update accordingly on successful negotiation'''
def onSuccess(acceptor, iterVal, offeror):
    success_by_iter[iterVal] = True
    players[offeror].offeror_success_count += 1
    players[acceptor].acceptor_success_count += 1
    players[offeror].offeror_value.append(players[offeror].offeror_value[iterVal])  # No motion
    players[acceptor].offeror_value.append(players[acceptor].offeror_value[iterVal])  # No motion
    players[offeror].acceptor_value.append(players[offeror].acceptor_value[iterVal])  # No motion
    players[acceptor].acceptor_value.append(players[acceptor].acceptor_value[iterVal])  # No motion

'''update accordingly on failed negotiation'''
def onFailure(acceptor, iterVal, offeror, sensitivity):
    failure_by_iter[iterVal] = True
    players[offeror].offeror_failure_count += 1
    players[acceptor].acceptor_failure_count += 1
    players[offeror].acceptor_value.append(players[offeror].acceptor_value[iterVal])
    players[acceptor].offeror_value.append(players[acceptor].offeror_value[iterVal])

    offeror_val = ((players[offeror].offeror_value[iterVal]) * players[offeror].stubbornness) + (
                (players[offeror].offeror_value[iterVal] + players[acceptor].acceptor_value[iterVal]) / 2) * (
                1 - players[offeror].stubbornness)
    players[offeror].offeror_value.append(offeror_val)

    acceptor_val = ((players[acceptor].acceptor_value[iterVal]) * players[acceptor].stubbornness) + (
                    (players[acceptor].acceptor_value[iterVal] + players[offeror].offeror_value[iterVal]) / 2) * (
                    1 - players[acceptor].stubbornness)
    players[acceptor].acceptor_value.append(acceptor_val)


'''update other nodes each iteration'''
def updateOthers(acceptor, iterVal, offeror):
    for i in range(1, number_of_players + 1):
        if (i != offeror and i != acceptor):
            players[i].offeror_value.append(players[i].offeror_value[iterVal])
            players[i].acceptor_value.append(players[i].acceptor_value[iterVal])


'''this utility function helps prevent memory overuse by clearing objects every 10,000 iteration and storing
the intermediate 10,000th value for later use. Note that I'm using 10,000 as a benchmark because we have 
~4000 nodes in the graph. A system with 16GB of memory can actually perform upto 75,000 iterations of 4000 nodes, but 
since we also need to store intermediate 10,000 steps for visualization purposes, I kept it as 10,000 for simplicity.
If the number of nodes in your graph increases substantially, you'll have to adjust the number of *refresh steps*'''
def refreshPlayersAndStoreSteps(players):
    dummyPlayer = True
    for player in players:
        if dummyPlayer:
            dummyPlayer = False
            continue
        topOfferValue = player.offeror_value[-1]
        topAcceptorValue = player.acceptor_value[-1]
        player.offeror_value.clear()
        player.acceptor_value.clear()

        '''appending twice as indexing starts from 0, which will be ignored. We are essentially refreshing our offerer
        and acceptor lists and putting the initial value as the last value obtained from the list. As the list grows 
        for each object, memory error is more likely to happen.'''
        [player.offeror_value.append(topOfferValue) for _ in range(2)]
        [player.acceptor_value.append(topAcceptorValue) for _ in range(2)]

        '''Offerer_steps and acceptor_steps contains values for each 50,000th iteration of our game'''
        player.offerer_steps.append(topOfferValue)
        player.acceptor_steps.append(topAcceptorValue)
    return players

def main():
    global players
    N = int(input("Enter the number of iterations you'd like: "))
    for iter in range(5 ):
        players = getNodes()
        finalPlayers = playGame(N)
        writeToFile(finalPlayers, iter, sensitivity_list, offerer_list, acceptor_list)
    print('\nCongratulations! Your game output has been saved in the file DataFile.csv; note that if you run the game '
          'again the file will be overwritten. Please save your file if you do not wish to lose data.')
    print("\n--- It took just %s seconds for the program to run! Isn't that great? :D ---" % round((time.time() - start_time),2))

if __name__ == "__main__":
    main()

