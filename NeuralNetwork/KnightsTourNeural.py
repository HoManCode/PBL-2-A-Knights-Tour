#!/usr/bin/env python
# coding: utf-8
"""
https://github.com/NiloofarShahbaz/knight-tour-neural-network/blob/master/knight_tour.py

Searches for a solution for the Knight's Tour problem on a board of size n x n from a randomly generated
starting point, using DFS. Each legal Knight's move is represented by a neuron. All neurons have a state,
2 vertices (which represent positions on the board), an output, and a maximum of 8 neighbours **neighbours are neurons
that share a vertex with the neuron in question.
If a neuron output is 1 it is the correct solution.
"""
#Imports the necessary libraries
import numpy as np
import time
import random
    
 #Defines legal Knight's moves in chess.
VALID_KNIGHT_MOVES = [(1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2)]
DEBUG = False

class KnightTour:
    def __init__(self, board_size):
        # Initializes necessary arrays & board size
        self.board_size = board_size
        self.board = []
        for i in range(self.board_size[0]):
            temp = []
            for j in range(self.board_size[1]):
                temp.append(set())
            self.board.append(temp)
        self.neuron_vertices = []
        self.neuron_outputs = np.array([])
        self.neuron_states = np.array([])
        self.neuron_neighbours = []
        if DEBUG:
            print('------FIRST-------')
            self.print_board(self.board)

        self.init()
        
    # Method to print the relevant sized board
    def print_board(self, board):
        if len(board) == self.board_size[0]:
            for i in range(self.board_size[0]):
                print(board[i])
        else:
            for i in range(0, len(board), 6):
                print(board[i: i+6])
                
    # Method to find all the possible Knight moves AKA neurons on the board
    # Also sets the neuron_vertices and neuron neighbours
    def init(self):
        neuron_num = 0
        # For loop iterates through the board for both x and y coordinates
        for x_position_1 in range(self.board_size[0]):
            for y_position_1 in range(self.board_size[1]):
                i = x_position_1 * self.board_size[1] + y_position_1

                for (x_position_2, y_position_2) in self.find_neighbours((x_position_1, y_position_1)):
                    j = x_position_2 * self.board_size[1] + y_position_2

                    # each neuron has 2 vertices
                    # this ensures that we add the neuron only once
                    if j > i:
                        self.board[x_position_1][y_position_1].add(neuron_num)
                        self.board[x_position_2][y_position_2].add(neuron_num)
                        self.neuron_vertices.append({(x_position_1, y_position_1), (x_position_2, y_position_2)})
                        neuron_num += 1

        for i in range(len(self.neuron_vertices)):
            vertex1, vertex2 = self.neuron_vertices[i]
            # neighbours of neuron i = neighbours of vertex1 + neighbours of vertex2 - i
            neighbours = self.board[vertex1[0]][vertex1[1]].union(self.board[vertex2[0]][vertex2[1]]) - {i}
            self.neuron_neighbours.append(neighbours)

        if DEBUG:
            print("----init-----")
            print('board')
            self.print_board(self.board)
            print('vertices')
            self.print_board(self.neuron_vertices)
            print('neighbours')
            self.print_board(self.neuron_neighbours)
            
    # Initializes each neuron state to 0 and a random number
    # between 0 and 1 for neuron outputs.
    def initialize_neurons(self):
        self.neuron_outputs = np.random.randint(2, size=(len(self.neuron_vertices)), dtype=np.int16)
        self.neuron_states = np.zeros((len(self.neuron_vertices)), dtype=np.int16)

        if DEBUG:
            print('_________initialize_neurons__________________________')
            print('states:')
            print(self.neuron_states)
            print('outputs')
            print(self.neuron_outputs)
            
    # Updates the state and output of each neuron
    def update_neurons(self):
        sum_of_neighbours = np.zeros((len(self.neuron_states)), dtype=np.int16)
        for i in range(len(self.neuron_neighbours)):
            sum_of_neighbours[i] = self.neuron_outputs[list(self.neuron_neighbours[i])].sum()
        next_state = self.neuron_states + 4 - sum_of_neighbours - self.neuron_outputs
        # counts the number of changes between the next state and the current state.
        number_of_changes = np.count_nonzero(next_state != self.neuron_states)
        # if next state[i] < 3 ---> output[i] = 0
        # if next state[i] > 0 ---> output[i] = 3
        self.neuron_outputs[np.argwhere(next_state < 0).ravel()] = 0
        self.neuron_outputs[np.argwhere(next_state > 3).ravel()] = 1
        self.neuron_states = next_state
        # counts the number of active neurons which are the neurons that their output is 1.
        number_of_active = len(self.neuron_outputs[self.neuron_outputs == 1])

        if DEBUG:
            print('____________________update________________________')
            print('states:')
            print(self.neuron_states)
            print('output')
            print(self.neuron_outputs)

        return number_of_active, number_of_changes
    
     # Method finds a CLOSED knight's tour
    def neural_network(self):
        even = False
        time = 0
        while True:
            self.initialize_neurons()
            n = 0
            while True:
                num_of_active, num_of_changes = self.update_neurons()
                print('_______________info_________________')
                print('active', num_of_active, 'changes', num_of_changes)
                if num_of_changes == 0:
                    break
                if self.check_degree():
                    even = True
                    break
                n += 1
                if n == 20:
                    break
            time +=1
            if even:
                print('all vertices have degree=2')
                if self.check_connected_components():
                    print('solution found!!')
                    self.get_solution()
                    return
                else:
                    even = False
                    
    # Ensures solution is in fact a knight's tour and not two or more independent hamiltonian graphs
    # gets the index of active neurons.
    def check_connected_components(self):
        active_neuron_indices = np.argwhere(self.neuron_outputs == 1).ravel()
        # dfs through all active neurons starting from the first element.
        connected = self.dfs_through_neurons(neuron=active_neuron_indices[0], active_neurons=active_neuron_indices)
        if connected:
            return True
        return False

    # From a starting active neuron a DFS algorithm is performed
    # Returning TRUE only if there are no more active neurons in the array
    # removes the neuron from the active neurons list.
    def dfs_through_neurons(self, neuron, active_neurons):
        active_neurons = np.setdiff1d(active_neurons, [neuron])
        # first finds the neighbours of this neuron and then finds which of them are active.
        active_neighbours = np.intersect1d(active_neurons, list(self.neuron_neighbours[neuron]))
        # if there was no active neighbours for this neuron, the hamiltonian graph has been
        # fully visited.
        if len(active_neighbours) == 0:
            # we check if all the active neurons have been visited. if not, it means that there
            # are more than 1 hamiltonian graph and it's not a knight's tour.
            if len(active_neurons) == 0:
                return True
            else:
                return False
        return self.dfs_through_neurons(neuron=active_neighbours[0], active_neurons=active_neurons)
    
    # Method finds and prints the solution
    def get_solution(self):
        visited = []

        current_vertex = (0, 0)
        labels = np.zeros(self.board_size, dtype=np.int16)
        # gets the index of active neurons.
        active_neuron_indices = np.argwhere(self.neuron_outputs == 1).ravel()
        i = 0
        while len(active_neuron_indices) != 0:
            visited.append(current_vertex)
            labels[current_vertex] = i
            i += 1
            # finds the index of neurons that have this vertex(current_vertex).
            vertex_neighbours = list(self.board[current_vertex[0]][current_vertex[1]])
            # finds the active ones.
            # active neurons that have this vertex are the edges of the solution graph that
            # share this vertex.
            vertex_neighbours = np.intersect1d(vertex_neighbours, active_neuron_indices)
            # picks one of the neighbours(the first one) and finds the other vertex of
            # this neuron(or edge) and sets it as the current one
            current_vertex = list(self.neuron_vertices[vertex_neighbours[0]] - {current_vertex})[0]
            # removes the selected neighbour from all active neurons
            active_neuron_indices = np.setdiff1d(active_neuron_indices, [vertex_neighbours[0]])
        print(labels)
        
    # Method returns the vertices of all active neurons whose output is 1
    def get_active_neurons_vertices(self):

        # gets the index of active neurons.
        active_neuron_indices = np.argwhere(self.neuron_outputs == 1).ravel()
        active_neuron_vertices = []
        for i in active_neuron_indices:
            active_neuron_vertices.append(self.neuron_vertices[i])
        return active_neuron_vertices

    # Method returns True if ALL vertices have degree =2
    # Updates the degree for all active neurons and checks for any numbers other than 2
    def check_degree(self):
        # gets the index of active neurons.
        active_neuron_indices = np.argwhere(self.neuron_outputs == 1).ravel()
        degree = np.zeros((self.board_size[0], self.board_size[1]), dtype=np.int16)

        for i in active_neuron_indices:
            vertex1, vertex2 = self.neuron_vertices[i]
            degree[vertex1[0]][vertex1[1]] += 1
            degree[vertex2[0]][vertex2[1]] += 1

        if DEBUG:
            print('____________________check degree_______________________')
            print(degree)

        # if all the degrees=2 return True
        if degree[degree != 2].size == 0:
            return True
        return False
    
    # Returns all valid moves for the knight given its current position
    def find_neighbours(self, pos):
        neighbours = set()
        for (dx, dy) in VALID_KNIGHT_MOVES:
            new_x, new_y = pos[0]+dx, pos[1]+dy
            if 0 <= new_x < self.board_size[0] and 0 <= new_y < self.board_size[1]:
                neighbours.add((new_x, new_y))
        return neighbours
#Takes user input for N board size
def inputBoardSize():
    while True:
        try:
            board_size = int(input("Please enter the size of the chess board: "))
        except ValueError:
            print("Please enter a valid board size!")
        else:
            if board_size > 4:
                break
            else:
                print("Board size must be greater than 4!")
    return board_size

#Times solution return
def print_time_lapsed(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    print('Time lapsed = {0}:{1}:{2}'.format(int(hours), int(mins), sec))


board_size = inputBoardSize()
tour = KnightTour(((board_size,board_size)))
start_time = time.time()
tour.neural_network()
stop_time = time.time()
print_time_lapsed(stop_time - start_time)
