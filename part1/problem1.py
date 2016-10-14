import sys, time

class Board():
	def __init__(self, n, k):
		self.n = n
		self.k = k
		self.config = [['.']*n]*n

	def print_board(self):
		for row in xrange(0, self.n):
			for col in xrange(0, self.n):
				print self.config[row][col],
		print '' #avoids continuation of further prints

	def print_board_like_board(self):
		for row in xrange(0, self.n):
			for col in xrange(0, self.n):
				print self.config[row][col],
			print ''

	def build_board(self, data):
		rows = [data[i:i+self.n] for i in range(0, len(data), self.n)]
		self.config = []
		for row in rows:
			self.config.append(row)

	def add_piece(self, row, col, data):
		data_list = list(data)
		index = row * self.n + col
		data_list[index] = 'w'
		new_data = ''.join(data_list)
		rows = [new_data[i:i+self.n] for i in range(0, len(data), self.n)]
		new_config = []
		for row in rows:
			new_config.append(row)
		return new_config

	def get_available_places(self):
		available = set()
		for row in xrange(0, self.n):
			for col in xrange(0, self.n):
				if self.config[row][col] == '.':
					available.add((row, col))
		return available

	def get_successors(self):
		available = self.get_available_places()
		data = ''
		for i in xrange(0, self.n):
			for j in xrange(0, self.n):
				data += self.config[i][j]
		successors = []
		for place in available:
			successors.append(self.add_piece(place[0], place[1], data))
		return successors

	def get_meta(self, state):
		return 0

class CohCoh():
	def __init__(self, state):
		self.state = state
		self.meta = -2

	def update_meta(self, new_meta):
		self.meta = new_meta


def print_stuff(stuff, n):
	for row in xrange(0, n):
		for col in xrange(0, n):
			print stuff[row][col],
		print ''

def print_stuff_single_line(stuff, n):
	for row in xrange(0, n):
		for col in xrange(0, n):
			print stuff[row][col],

n = (int)(sys.argv[1])
k = (int)(sys.argv[2])
b = Board(n, k)
b.print_board()
b.print_board_like_board()

data = sys.argv[3]
b.build_board(data)
b.print_board()
b.print_board_like_board()

available_time = (int)(sys.argv[4])

start_time = time.time()

#while time.time()- start_time < available_time:
	#suggest next move

successors = b.get_successors()
print successors

target = CohCoh(successors[0]).state
min_meta = -2
for successor in successors:
	c = CohCoh(successor)
	c.update_meta(b.get_meta(successor))
	if min_meta < c.meta:
		min_meta = c.meta
		target = c.state

print_stuff_single_line(target, n)

