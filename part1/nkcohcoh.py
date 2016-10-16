# coding=UTF-8
# Problem 1.

# The problem is to find the possible moves that dont make the current player lose the game immediately and selecting a move which makes the other player’s future moves more restrictive. Passing on to the other player a board which is harder for him/her to win. The problem also includes the possibility to play more aggressively if the other player is already in a bad state.


# State space: Is the possible configuration of the n-k-cho-cho game.  Where each player can place each respective black or white marble as per their choice on n by n board by following a legal move. A legal move is defined as when a respective player can place a either a white or black marble on the board where there is an empty space


# Start state: The start state is an empty board of n by n, consisting of the size (n) specified by the user.  It can also be assumed that white player will always make the first move. The board also includes a parameter ‘k’ which is the max quantity in which a marble of a particular color can be placed in a row, column or diagonal.

# Goal state: There are 3 specific goal state 

# Player 1 wins (white marbles) – when player 2 losses i.e player 2 completes a row, column or diagonal of size k with black marbles, where k is provided by the user.
# Player 2 wins (black marbles) – when player 1 losses i.e player 1 completes a row, column or diagonal of size k with white marbles, where k is provided by the user.
# Draw – when there are no more blank space on the board where either of the player can place any marble and none of the players have placed their respective marbles in k quantity in any row, column or diagonal

# Successor function:  The successor function take the current board looks at all available place (blank places) places a marble in a legal move fashion with reference to the player and returns the board. These returned board are further evaluated by another function and finally a suggestion is made to the user.


# Cost: The cost is uniform as the we can make only one move in each successor and the cost of making the move is constant.


# Heuristic function: The heuristic function is composed of two parts 

# Avoid immediate loss idea  takes the board and calculates the place where the current player should not make a move or place the marble in order to not lose immediately- This part is based on the condition that the current move to be suggested does not meet the terminal or goal state with the current “k”

# Future evaluator of the all available moves after the immediate loss function this parts calculates the move which makes the next moves of the other player not so lucrative.



# Assumptions:  The white marble player is the user for us and we are recommending the moves for him/her


# Parts of the program:

# The program consists of the following parts:

# For Class Board we have the following functions . 

# add_piece -  adds a piece on the board
# get_available_place- returns the number of empty places that are available to make a move
# get_successors- returns the new intermediate board along with the player and some evaluation metric to choose the next best move
# has_lost- check whether the terminal condition has met or not
# get_diagonals- returns the diagonal elements based on the configuration of the board which is the result of “n’ the size of the board  

# For Class ChoCho we have 

# Attributes – state, whites and blacks array, white and black distribution centroids and alpha and beta values which are weights for evaluation
# print_stuff_single_line- print the board in the required format


# Explanation of the program:

# The program initially takes the input form the user 
# Generates the successors and passes each successor state to the evaluation part
# Check the place which the player1 or ‘W’ should not play in order not to lose the game immediately and make them unavailable to play for the white marble placement
# Then the program  check all the possible move  in a given time frame to see which move reduces the free available places for the next player and makes that move
# Finally based on the size of the board ‘n’ and ‘k’  there is a possibility that the program will apply min max algorithm to ensure at-least a draw if possible from the given configuration of the board
import sys, time, math
import numpy as np
from random import randint

class Board():
	def __init__(self, n, k):
		self.n = n
		self.k = k
		self.config = [['.']*n]*n
		self.open_places_indices = []

	def build_board(self, data):
		rows = [data[i:i+self.n] for i in range(0, len(data), self.n)]
		self.config = []
		for row in rows:
			self.config.append(row)

	def add_piece(self, row, col, data, player):
		data_list = list(data)
		index = row * self.n + col
		data_list[index] = player
		new_data = ''.join(data_list)
		rows = [new_data[i:i+self.n] for i in range(0, len(data), self.n)]
		new_config = []
		for row in rows:
			new_config.append(row)
		return new_config

	def get_available_places(self):
		available = []
		for row in xrange(0, self.n):
			for col in xrange(0, self.n):
				if self.config[row][col] == '.':
					available.append((row, col))
					self.open_places_indices.append((row, col))
		return available

	def get_successors(self, player):
		available = self.get_available_places()
		data = ''
		for i in xrange(0, self.n):
			for j in xrange(0, self.n):
				data += self.config[i][j]
		successors = []
		for place in available:
			successors.append(self.add_piece(place[0], place[1], data, player))
		return successors

	
	def has_lost(self, player):
		check = ''
		for i in xrange(0, self.k):
			check += player

		# horizontal 
		for i in xrange(0, self.n):
			row = self.config[i]
			if check in row:
				return True
		
		#vertical
		flipped_rows = map(list, zip(*self.config)) #cols are flipped rows (Transpose)
		for row in flipped_rows:
			t = ''
			for ele in row:
				t += str(ele)
			if check in t:
				return True

		#diagonal
		for diag in self.get_diagonals():
			t = ''
			for ele in diag:
				t += ele
			if check in t:
				return True


		return False

	def get_diagonals(self):
		# Ref: http://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python
		alternate_config = []
		for ele in self.config:
			row = list(ele)
			alternate_config.append(row)
		x,y = self.n,self.n
		a = np.array(alternate_config)
		diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
		diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
		return [n.tolist() for n in diags]

class CohCoh():
	def __init__(self, state):
		self.state = state
		self.whites = []
		self.blacks = []
		self.white_centroid_x = 0.0
		self.white_centroid_y = 0.0
		self.black_centroid_x = 0.0
		self.black_centroid_y = 0.0
		self.alpha = 0.0
		self.beta = 0.0

def print_stuff(stuff, n):
	for row in xrange(0, n):
		for col in xrange(0, n):
			print stuff[row][col],
		print ''

def print_stuff_single_line(stuff, n):
	result = ''
	for row in xrange(0, n):
		for col in xrange(0, n):
			result += stuff[row][col]
	print result

n = (int)(sys.argv[1])
k = (int)(sys.argv[2])
b = Board(n, k)
data = sys.argv[3]
b.build_board(data)
available_time = (float)(sys.argv[4])

start_time = time.time()

availables_black = 0
successors_black = b.get_successors('b')
bad_indices_for_black = []
i = 0
for successor_black in successors_black:
	bdash = Board(n, k)
	bdash.config = successor_black
	if not bdash.has_lost('b'):
		availables_black += 1
	# else:
	# 	b.open_places_indices.remove(i)
	# i += 1
	else:
		bad_indices_for_black.append(b.open_places_indices[i])
	i += 1

print "Bad indices for black", bad_indices_for_black
successors = b.get_successors('w')

target = successors[0]
availables = []

open_places_new_indices = []

i = 0
for successor in successors:
	bdash = Board(n, k)
	bdash.config = successor
	if not bdash.has_lost('w'):
		availables.append(bdash)
		open_places_new_indices.append(b.open_places_indices[i])
	i += 1
print "Open for white", open_places_new_indices

time_out_suggestion = availables[0]

while time.time() - start_time < available_time:
	#suggest next move
	coh_cohs = []
	ctr = 0
	for available in availables:
		if open_places_new_indices[ctr] not in bad_indices_for_black:

			i = open_places_new_indices[ctr][0]
			j = open_places_new_indices[ctr][1]

			c = CohCoh(available.config)
			sum_whites_x, sum_whites_y, sum_blacks_x, sum_blacks_y = 0.0, 0.0, 0.0, 0.0
			coh_cohs.append(c)
			
			#search vertical: i-k+1 to i+k-1, j same
			for p in xrange(i-k+1, i+k):
				if p >= 0 and p < n and p != i:
					if b.config[p][j] == 'w':
						c.whites.append((p, j))
						sum_whites_x += p
						sum_whites_y += j
					if b.config[p][j] == 'b':
						c.blacks.append((p, j))
						sum_blacks_x += p
						sum_blacks_y += j 
			#search horizontal: j-k+1 to j+k-1, i same
			for p in xrange(j-k+1, j+k):
				if p >= 0 and p < n and p != j:
					if b.config[i][p] == 'w':
						c.whites.append((i, p))
						sum_whites_x += i
						sum_whites_y += p
					if b.config[i][p] == 'b':
						c.blacks.append((i, p))
						sum_blacks_x += i
						sum_blacks_y += p
			#search obtuse diagonal: i-k+1, j-k+1 to i+k-1, j+k-1
			for p,q in zip(xrange(i-k+1,i+k), xrange(j-k+1,j+k)):
				if p >= 0 and p < n and q >= 0 and q < n:
					if b.config[p][q] == 'w':
						c.whites.append((p, q))
						sum_whites_x += p
						sum_whites_y += q
					if b.config[p][q] == 'b':
						c.whites.append((p, q))
						sum_blacks_x += p
						sum_blacks_y += q
			#search acute diagonal: i-k+1, j+k-1 to i+k-1, j-k+1
			for p,q in zip(xrange(i-k+1,i+k), xrange(j+k-1,j-k)):
				if p >= 0 and p < n and q >= 0 and q < n:
					if b.config[p][q] == 'w':
						c.whites.append((p, q))
						sum_whites_x += p
						sum_whites_y += q
					if b.config[p][q] == 'b':
						c.whites.append((p, q))
						sum_blacks_x += p
						sum_blacks_y += q

			if len(c.whites) > 0:
				c.white_centroid_x = sum_whites_x / len(c.whites)
				c.white_centroid_y = sum_whites_y / len(c.whites) 
			if len(c.blacks) > 0:
				c.black_centroid_x = sum_blacks_x / len(c.blacks)
				c.black_centroid_y = sum_blacks_y / len(c.blacks)
			print "Available", available.config, "Whites", c.whites, "Blacks", c.blacks,
			c.alpha = math.sqrt(abs(c.white_centroid_x - i) ** 2 + abs(c.white_centroid_y - j) ** 2)
			c.beta = math.sqrt(abs(c.black_centroid_x - i) ** 2 + abs(c.black_centroid_y - j) ** 2)

			print "Alpha", c.alpha, "Beta", c.beta
		ctr += 1

	if len(coh_cohs) == 0:
		ctr = 0
		print "Help black bcoz no other move available"
		for available in availables:
			i = open_places_new_indices[ctr][0]
			j = open_places_new_indices[ctr][1]

			c = CohCoh(available.config)
			sum_whites_x, sum_whites_y, sum_blacks_x, sum_blacks_y = 0.0, 0.0, 0.0, 0.0
			coh_cohs.append(c)
			
			#search vertical: i-k+1 to i+k-1, j same
			for p in xrange(i-k+1, i+k):
				if p >= 0 and p < n and p != i:
					if b.config[p][j] == 'w':
						c.whites.append((p, j))
						sum_whites_x += p
						sum_whites_y += j
					if b.config[p][j] == 'b':
						c.blacks.append((p, j))
						sum_blacks_x += p
						sum_blacks_y += j 
			#search horizontal: j-k+1 to j+k-1, i same
			for p in xrange(j-k+1, j+k):
				if p >= 0 and p < n and p != j:
					if b.config[i][p] == 'w':
						c.whites.append((i, p))
						sum_whites_x += i
						sum_whites_y += p
					if b.config[i][p] == 'b':
						c.blacks.append((i, p))
						sum_blacks_x += i
						sum_blacks_y += p
			#search obtuse diagonal: i-k+1, j-k+1 to i+k-1, j+k-1
			for p,q in zip(xrange(i-k+1,i+k), xrange(j-k+1,j+k)):
				if p >= 0 and p < n and q >= 0 and q < n:
					if b.config[p][q] == 'w':
						c.whites.append((p, q))
						sum_whites_x += p
						sum_whites_y += q
					if b.config[p][q] == 'b':
						c.whites.append((p, q))
						sum_blacks_x += p
						sum_blacks_y += q
			#search acute diagonal: i-k+1, j+k-1 to i+k-1, j-k+1
			for p,q in zip(xrange(i-k+1,i+k), xrange(j+k-1,j-k)):
				if p >= 0 and p < n and q >= 0 and q < n:
					if b.config[p][q] == 'w':
						c.whites.append((p, q))
						sum_whites_x += p
						sum_whites_y += q
					if b.config[p][q] == 'b':
						c.whites.append((p, q))
						sum_blacks_x += p
						sum_blacks_y += q

			if len(c.whites) > 0:
				c.white_centroid_x = sum_whites_x / len(c.whites)
				c.white_centroid_y = sum_whites_y / len(c.whites) 
			if len(c.blacks) > 0:
				c.black_centroid_x = sum_blacks_x / len(c.blacks)
				c.black_centroid_y = sum_blacks_y / len(c.blacks)
			print "Available", available.config, "Whites", c.whites, "Blacks", c.blacks,
			c.alpha = math.sqrt(abs(c.white_centroid_x - i) ** 2 + abs(c.white_centroid_y - j) ** 2)
			c.beta = math.sqrt(abs(c.black_centroid_x - i) ** 2 + abs(c.black_centroid_y - j) ** 2)

			print "Alpha", c.alpha, "Beta", c.beta
			ctr += 1

	solution = None
	if len(availables) > availables_black:
		#play ambitiously
		print "Ambi"
		max_alpha_plus_beta = 0.0
		for cohcoh in coh_cohs:
			if cohcoh.alpha + cohcoh.beta > max_alpha_plus_beta:
				max_alpha_plus_beta = cohcoh.alpha + cohcoh.beta
				solution = cohcoh.state
		print "Solution:"

	else:
		#play safe
		print "Safe"
		max_alpha = 0.0
		for cohcoh in coh_cohs:
			if cohcoh.alpha > max_alpha:
				max_alpha = cohcoh.alpha
				solution = cohcoh.state
		print "Solution:"

	if solution is not None:
		print "Eval Success", time.time() - start_time
		print_stuff_single_line(solution, n)
		#print "Eval Success", time.time() - start_time
		#print "I had time", available_time
		sys.exit()
	else:
		#iQuit
		print "iQuit"
		data = ''
		for i in xrange(0, n):
			for j in xrange(0, n):
				data += b.config[i][j]
		#print data
		for row in xrange(0, n):
			for col in xrange(0, n):
				if b.config[row][col] == '.':
					b.config = b.add_piece(row, col, data, 'w')
					#print b.config
		print_stuff_single_line(b.config, n)
		sys.exit()
print "Couldn't solve"
print_stuff_single_line(time_out_suggestion.config, n)