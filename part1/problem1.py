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

n = 3
k = 2
b = Board(n, k)
b.print_board()
b.print_board_like_board()

data = ".w......b"
b.build_board(data)
b.print_board()
b.print_board_like_board()