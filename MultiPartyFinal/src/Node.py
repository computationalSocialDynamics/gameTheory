'''the Node class which represents each of our network's vertex'''
class Node:
    def __init__(self, label):
        self.label = label
        self.neighbors = []
        self.degree = 0
        self.comfort = 0
        self.stubbornness = 0
        self.offeror_value = []
        self.acceptor_value = []
        self.offeror_count = 0
        self.acceptor_count = 0
        self.offeror_success_count = 0
        self.offeror_failure_count = 0
        self.acceptor_success_count = 0
        self.acceptor_failure_count = 0
        self.number_of_iterations = 0
        self.offerer_steps = []
        self.acceptor_steps = []
        self.acceptor_positive_loss = 0
        self.acceptor_negative_loss = 0
        self.offeror_positive_loss = 0
        self.offeror_negative_loss = 0
        self.acceptor_positive_loss_count = 0
        self.acceptor_negative_loss_count = 0
        self.offeror_positive_loss_count = 0
        self.offeror_negative_loss_count = 0
