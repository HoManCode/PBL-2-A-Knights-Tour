#!/usr/bin/env python
# coding: utf-8

# In[33]:





# In[36]:


import numpy as np
#Defines legal Knight's moves in chess

VALID_KNIGHT_MOVES = [(1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2)]
DEBUG = False

"""
Class to solve Knights Tour problem. Each legal Knight's move is represented by a neuron. All neurons have a state,
 2 vertices (which represent positions on the board), an output, and a maximum of 8 neighbours **neighbours are neurons
 that share a vertex with the neuron in question.
 If a neuron output is 1 it is the correct solution 
"""

class KnightTour:
    

    #Initializes necessary arrays & board size 
    
    def __init__(knight_tour_class, board_size):
        knight_tour_class.board_size = board_size
        knight_tour_class.board = []
        for i in range(knight_tour_class.board_size[0]):
            temp = []
            for j in range(knight_tour_class.board_size[1]):
                temp.append(set())
            knight_tour_class.board.append(temp)
        knight_tour_class.neuron_vertices = []
        knight_tour_class.neuron_outputs = np.array([])
        knight_tour_class.neuron_states = np.array([])
        knight_tour_class.neuron_neighbours = []
        if DEBUG:
            print('------FIRST-------')
            knight_tour_class.print_board(knight_tour_class.board)

        knight_tour_class.initialize()

    
   #Method to print the relevant sized board
   
    def print_board(knight_tour_class, board):
        if len(board) == knight_tour_class.board_size[0]:
            for i in range(knight_tour_class.board_size[0]):
                print(board[i])
        else:
            m = 0
            strin = ''
            for i in range(0, len(board), 6):
                print(board[i: i+6])
                
    
    #Method to find all the possible Knight moves AKA neurons on the board
    #Also sets the neuron_vertices and neuron neighbours
    
    def initialize(knight_tour_class):
    
        neuron_num = 0
        # For loop iterates through the board for both x and y coordinates
        for x_position_1 in range(knight_tour_class.board_size[0]):
            for y_position_1 in range(knight_tour_class.board_size[1]):
                i = x_position_1 * knight_tour_class.board_size[1] + y_position_1

                for (x_position_2, y_position_2) in knight_tour_class.find_neighbours((x_position_1, y_position_1)):
                    j = x_position_2 * knight_tour_class.board_size[1] + y_position_2

                    # each neuron has 2 vertices
                    # this ensures that we add the neuron only once.
                    if j > i:
                        knight_tour_class.board[x_position_1][y_position_1].add(neuron_num)
                        knight_tour_class.board[x_position_2][y_position_2].add(neuron_num)
                        knight_tour_class.neuron_vertices.append({(x_position_1, y_position_1), (x_position_2, y_position_2)})
                        neuron_num += 1

        for i in range(len(knight_tour_class.neuron_vertices)):
            vertex1, vertex2 = knight_tour_class.neuron_vertices[i]
            # neighbours of neuron i = neighbours of vertex1 + neighbours of vertex2 - i
            neighbours = knight_tour_class.board[vertex1[0]][vertex1[1]].union(knight_tour_class.board[vertex2[0]][vertex2[1]]) - {i}
            knight_tour_class.neuron_neighbours.append(neighbours)

        if DEBUG:
            print("----init-----")
            print('board')
            knight_tour_class.print_board(knight_tour_class.board)
            print('vertices')
            knight_tour_class.print_board(knight_tour_class.neuron_vertices)
            print('neighbours')
            knight_tour_class.print_board(knight_tour_class.neuron_neighbours)
            
       
    #Initializes each neuron state to 0 and a random number
    #between 0 and 1 for neuron outputs.
        
    def initialize_neurons(knight_tour_class):
     
        knight_tour_class.neuron_outputs = np.random.randint(2, size=(len(knight_tour_class.neuron_vertices)), dtype=np.int16)
        knight_tour_class.neuron_states = np.zeros((len(knight_tour_class.neuron_vertices)), dtype=np.int16)

        if DEBUG:
            print('_________initialize_neurons__________________________')
            print('states:')
            print(knight_tour_class.neuron_states)
            print('outputs')
            print(knight_tour_class.neuron_outputs)
            
    #Updates the state and output of each neuron
    def update_neurons(knight_tour_class):

        sum_of_neighbours = np.zeros((len(knight_tour_class.neuron_states)), dtype=np.int16)
        for i in range(len(knight_tour_class.neuron_neighbours)):
            sum_of_neighbours[i] = knight_tour_class.neuron_outputs[list(knight_tour_class.neuron_neighbours[i])].sum()

        next_state = knight_tour_class.neuron_states + 4 - sum_of_neighbours - knight_tour_class.neuron_outputs
        # counts the number of changes between the next state and the current state.
        number_of_changes = np.count_nonzero(next_state != knight_tour_class.neuron_states)
        # if next state[i] < 3 ---> output[i] = 0
        # if next state[i] > 0 ---> output[i] = 3
        knight_tour_class.neuron_outputs[np.argwhere(next_state < 0).ravel()] = 0
        knight_tour_class.neuron_outputs[np.argwhere(next_state > 3).ravel()] = 1
        knight_tour_class.neuron_states = next_state
        # counts the number of active neurons which are the neurons that their output is 1.
        number_of_active = len(knight_tour_class.neuron_outputs[knight_tour_class.neuron_outputs == 1])

        if DEBUG:
            print('____________________update________________________')
            print('states:')
            print(knight_tour_class.neuron_states)
            print('output')
            print(knight_tour_class.neuron_outputs)

        return number_of_active, number_of_changes
    
    #Method finds a CLOSED knight's tour
    def neural_network(knight_tour_class):

        even = False
        time = 0
        while True:
            knight_tour_class.initialize_neurons()
            n = 0
            while True:
                num_of_active, num_of_changes = knight_tour_class.update_neurons()
                print('_______________info_________________')
                print('active', num_of_active, 'changes', num_of_changes)
                if num_of_changes == 0:
                    break
                if knight_tour_class.check_degree():
                    even = True
                    break
                n += 1
                if n == 20:
                    break
            time += 1
            if even:
                print('all vertices have degree=2')
                if knight_tour_class.check_connected_components():
                    print('solution found!!')
                    knight_tour_class.get_solution()
                    return
                else:
                    even = False

    #Ensures solution is in fact a knight's tour and not two or more independent hamiltonian graphs
    def check_connected_components(knight_tour_class):

        # gets the index of active neurons.
        active_neuron_indices = np.argwhere(knight_tour_class.neuron_outputs == 1).ravel()
        # dfs through all active neurons starting from the first element.
        connected = knight_tour_class.dfs_through_neurons(neuron=active_neuron_indices[0], active_neurons=active_neuron_indices)
        if connected:
            return True
        return False
    
    #From a starting active neuron a DFS algorithm is performed
    #Returning TRUE only if there are no more active neurons in the array 
    def dfs_through_neurons(knight_tour_class, neuron, active_neurons):

        # removes the neuron from the active neurons list.
        active_neurons = np.setdiff1d(active_neurons, [neuron])
        # first finds the neighbours of this neuron and then finds which of them are active.
        active_neighbours = np.intersect1d(active_neurons, list(knight_tour_class.neuron_neighbours[neuron]))
        # if there was no active neighbours for this neuron, the hamiltonian graph has been
        # fully visited.
        if len(active_neighbours) == 0:
            # we check if all the active neurons have been visited. if not, it means that there
            # are more than 1 hamiltonian graph and it's not a knight's tour.
            if len(active_neurons) == 0:
                return True
            else:
                return False
        return knight_tour_class.dfs_through_neurons(neuron=active_neighbours[0], active_neurons=active_neurons)
    
    #Method finds and prints the solution
    def get_solution(knight_tour_class):

        visited = []
        current_vertex = (0, 0)
        labels = np.zeros(knight_tour_class.board_size, dtype=np.int16)
        # gets the index of active neurons.
        active_neuron_indices = np.argwhere(knight_tour_class.neuron_outputs == 1).ravel()
        i = 0
        while len(active_neuron_indices) != 0:
            visited.append(current_vertex)
            labels[current_vertex] = i
            i += 1
            # finds the index of neurons that have this vertex(current_vertex).
            vertex_neighbours = list(knight_tour_class.board[current_vertex[0]][current_vertex[1]])
            # finds the active ones.
            # active neurons that have this vertex are the edges of the solution graph that
            # share this vertex.
            vertex_neighbours = np.intersect1d(vertex_neighbours, active_neuron_indices)
            # picks one of the neighbours(the first one) and finds the other vertex of
            # this neuron(or edge) and sets it as the current one
            current_vertex = list(knight_tour_class.neuron_vertices[vertex_neighbours[0]] - {current_vertex})[0]
            # removes the selected neighbour from all active neurons
            active_neuron_indices = np.setdiff1d(active_neuron_indices, [vertex_neighbours[0]])
        print(labels)

    #Method returns the vertices of all active neurons whose output is 1
    def get_active_neurons_vertices(knight_tour_class):

        # gets the index of active neurons.
        active_neuron_indices = np.argwhere(knight_tour_class.neuron_outputs == 1).ravel()
        active_neuron_vertices = []
        for i in active_neuron_indices:
            active_neuron_vertices.append(knight_tour_class.neuron_vertices[i])
        return active_neuron_vertices

    #Method returns True if ALL vertices have degree =2
    #Updates the degree for all active neurons and checks for any numbers other than 2
    def check_degree(knight_tour_class):

        # gets the index of active neurons.
        active_neuron_indices = np.argwhere(knight_tour_class.neuron_outputs == 1).ravel()
        degree = np.zeros((knight_tour_class.board_size[0], knight_tour_class.board_size[1]), dtype=np.int16)

        for i in active_neuron_indices:
            vertex1, vertex2 = knight_tour_class.neuron_vertices[i]
            degree[vertex1[0]][vertex1[1]] += 1
            degree[vertex2[0]][vertex2[1]] += 1

        if DEBUG:
            print('____________________check degree_______________________')
            print(degree)

        # if all the degrees=2 return True
        if degree[degree != 2].size == 0:
            return True
        return False

    #Returns all valid moves for the knight given its current position
    def find_neighbours(knight_tour_class, pos):

        neighbours = set()
        for (dx, dy) in KNIGHT_MOVES:
            new_x, new_y = pos[0]+dx, pos[1]+dy
            if 0 <= new_x < knight_tour_class.board_size[0] and 0 <= new_y < knight_tour_class.board_size[1]:
                neighbours.add((new_x, new_y))
        return neighbours


# tour = KnightTour((6, 6))
# tour.neural_network()


# In[37]:


tour = KnightTour((6, 6))
tour.neural_network()


# In[ ]:




