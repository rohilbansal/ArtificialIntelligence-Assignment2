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
available_time = (int)(sys.argv[4])

start_time = time.time()

#while time.time()- start_time < available_time:
	#suggest next move

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
	print_stuff_single_line(solution, n)
else:
	#iQuit
	print_stuff_single_line(b.config, n)
