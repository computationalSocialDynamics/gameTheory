import codecs
import csv

def writeToFile(finalPlayers, iter, sensitivity_list, offeror_list, acceptor_list):
    del finalPlayers[0] #deleting dummy player
    with codecs.open("RunSensitivityRandomComfort" + str(iter+1) + ".csv", "w", "utf-8-sig") as outputFile:
        writer = csv.writer(outputFile, dialect="excel")
        '''write header row'''
        header_row = ['Label', 'Degree', 'Comfort', 'Stubbornness', 'Number of iterations', 'Offeror Positive Loss', 'Offeror Negative Loss',
                      'Acceptor Positive Loss', 'Acceptor Negative Loss', 'Offerer Count', 'Acceptor Count', 'Offeror Success',
                      'Offeror Failure', 'Acceptor Success', 'Acceptor Failure']
        writer.writerow(header_row)

        '''write player attributes to file'''
        for player in finalPlayers:
            if not player.neighbors:
                continue
            label = player.label
            degree = player.degree
            comfort = player.comfort
            stubbornness = player.stubbornness
            number_of_iterations = player.offeror_count + player.acceptor_count
            offer_positive_loss = player.offeror_positive_loss
            offer_negative_loss = player.offeror_negative_loss
            acceptor_positive_loss = player.acceptor_positive_loss
            acceptor_negative_loss = player.acceptor_negative_loss
            offer_count = player.offeror_count
            accept_count = player.acceptor_count
            offer_success = player.offeror_success_count
            offer_failure = player.offeror_failure_count
            accept_success = player.acceptor_success_count
            accept_failure = player.acceptor_failure_count
            row = [label, degree, comfort, stubbornness, number_of_iterations,offer_positive_loss, offer_negative_loss,
                   acceptor_positive_loss, acceptor_negative_loss, offer_count, accept_count, offer_success, offer_failure,
                   accept_success, accept_failure]
            row.extend(player.offerer_steps)
            row.extend(player.acceptor_steps)
            writer.writerow(row)
        sensitivity_row = ['' for i in range(len(header_row))]
        sensitivity_row.extend(sensitivity_list)
        writer.writerow(sensitivity_row)

        offeror_row = ['' for i in range(len(header_row))]
        offeror_row.extend(offeror_list)
        writer.writerow(offeror_row)

        acceptor_row = ['' for i in range(len(header_row))]
        acceptor_row.extend(acceptor_list)
        writer.writerow(acceptor_row)
