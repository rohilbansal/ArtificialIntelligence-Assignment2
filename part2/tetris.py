# Simple tetris program! v0.2
# D. Crandall, Sept 2016

from AnimatedTetris import *
from SimpleTetris import *
from kbinput import *
import time, sys, copy, operator

class HumanPlayer:
    def get_moves(self, tetris):
        print "Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\nThen press enter. E.g.: bbbnn\n"
        moves = raw_input()
        return moves

    def control_game(self, tetris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": tetris.left, "n": tetris.rotate, "m": tetris.right, " ": tetris.down }
            commands[c]()

######
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. tetris is an object that lets you inspect the board, e.g.:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #
    '''
    def calculateFreq(self, list1):
	newVal = {}
	for element in list1:
		if(newVal.get(element)!= None):
			val = newVal.get(element)
			val += 1
			newVal[element] = val
		else:
			newVal[element] = 1
	return newVal'''

    def calculateNumberOfXs(self, newBoardList, tetris_orig):
	countList = {}
	orig_board = tetris_orig.get_board()
        for elements in newBoardList:
                count = 0
		count2 = 0
                #print(elements)
                #print(len(newBoardList[elements]))
		#print(newBoardList[elements][0][19])
                for i in range(0, 10):
                        if(newBoardList[elements][0][19][i] == "x"):
                                count += 1
			if(orig_board[19][i] == "x"):
				count2 += 1
		print("Orig",count2,"new",count)
		if(count2 > count):
			newBoardList[elements][1] = 10+count
			countList[elements] = 10+count
		else:
			newBoardList[elements][1] = count
                	countList[elements] = count
        #print("before", countList)
        #print("count value", count)
        '''
        if(all(value == count for value in countList.values())):
                for elements in newBoardList:
                        count = 0
                        #print(elements)
                        #print(len(newBoardList[elements]))
                        for i in range(0, 10):
                                if(newBoardList[elements][18][i] == "x"):
                                        count += 1
                        countList[elements] = count
                print("inside", countList)'''
        j = 1
        while(all(value == count for value in countList.values()) and j < 20):
                for elements in newBoardList:
                        count = 0
			count2 = 0
                        #print(elements)
                        #print(len(newBoardList[elements]))
                        for i in range(0, 10):
                                if(newBoardList[elements][0][19-j][i] == "x"):
                                        count += 1
				if(orig_board[19-j][i] == "x"):
					count2 += 1
			if(count2 > count):
                        	newBoardList[elements][1] = 10+count
                        	countList[elements] = 10+count
			else:
				newBoardList[elements][1] = count
                        	countList[elements] = count
                #print("inside j count", countList)
                j += 1
                #print("inside j value", j)
	print(newBoardList)
	return newBoardList
	#return(max(countList.iteritems(), key=operator.itemgetter(1))[0])
    
    def calculateAggregateHeight(self, newBoardList, tetris_orig):
	for elements in newBoardList:
		count = 0
		for i in range(0,10):
			for j in range(0,20):
				if(newBoardList[elements][0][j][i] == "x"):
					count += 20-j
					break;
		oldCount = newBoardList[elements][1]
		count = oldCount + (-0.03)*count
		newBoardList[elements][1] = count
	return newBoardList
		
				


    def checkPermutations(self, board, tetris_orig):
	#print("Inside perm")
	newBoardList = {}
	tetris1 = copy.deepcopy(tetris_orig)
	board1 = tetris_orig.get_board()
	for i in range(0, 4):
		string_commands = ""
		tetris1 = copy.deepcopy(tetris_orig)
		board1 = tetris_orig.get_board()
		for j in range(0, i+1):
			tetris1.rotate()
			string_commands += "n"
		#print(tetris1.get_piece())
		board2 = copy.deepcopy(board1)
		min_column_height = [ min ([r for r in range(len(board1)-1, 0, -1) if board1[r][c] == "x" ] + [100,]) for c in range(0, len(board1[0]))]
		index = min_column_height.index(max(min_column_height))
		#print(min_column_height)
		
		if(index < tetris1.col):
                	count = tetris1.col - index
                	for i in range(0, count):
				string_commands += "b"
				tetris1.left()
        	elif(index > tetris1.col):
                	count = index - tetris1.col
                	for i in range(0, count):
				string_commands += "m"
				tetris1.right()
		tetris1.down()
		newBoardList[string_commands] = [tetris1.get_board(),0]
		#print(newBoardList)
	newBoardList = self.calculateNumberOfXs(newBoardList, tetris_orig)
	print(newBoardList)
	newBoardList = self.calculateAggregateHeight(newBoardList, tetris_orig)
	temp_dict = {}
	for val in newBoardList:
		temp_dict[val] = newBoardList[val][1]
	return(max(temp_dict, key=(lambda key: temp_dict[key])))
	#print(newBoardList)
	'''
	countList = {}
	for elements in newBoardList:
		count = 0
		#print(elements)
		#print(len(newBoardList[elements]))
		for i in range(0, 10):
			if(newBoardList[elements][19][i] == "x"):
				count += 1
		countList[elements] = count
	print("before", countList)
	print("count value", count)
	
	if(all(value == count for value in countList.values())):
		for elements in newBoardList:
                	count = 0
                	#print(elements)
                	#print(len(newBoardList[elements]))
                	for i in range(0, 10):
                        	if(newBoardList[elements][18][i] == "x"):
                                	count += 1
                	countList[elements] = count
		print("inside", countList)
	j = 1
 	while(all(value == count for value in countList.values()) and j < 20):
                for elements in newBoardList:
                        count = 0
                        #print(elements)
                        #print(len(newBoardList[elements]))
                        for i in range(0, 10):
                                if(newBoardList[elements][19-j][i] == "x"):
                                        count += 1
                        countList[elements] = count
		print("inside j count", countList)
		j += 1
                print("inside j value", j)

	
	i = 1
	while (all( value == count for value in countList.values())) and (i<20):
		print("inside while")
		countList = self.createBoardSnapshot(newBoardList, i)
		print("new",countList)
		i += 1
		print("rohil")
	
	#print(max(countList.iteritems(), key=operator.itemgetter(1))[0])
	return(max(countList.iteritems(), key=operator.itemgetter(1))[0]) 
	#print(tetris1.get_board())
	#print(tetris1.get_piece())'''

    def get_moves(self, tetris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
	board = tetris.get_board()
	#print(board)
	#min_column_height = [ min ([r for r in range(len(board)-1, 0, -1) if board[r][c] == "x" ] + [100,]) for c in range(0, len(board[0]))]
	#index = min_column_height.index(max(min_column_height))
	#print(min_column_height)
	#print(self.calculateFreq(min_column_height))

	strVal = self.checkPermutations(board, tetris)
	print(strVal)
	return strVal
	'''	
	string_commands = ""

	if(index < tetris.col):
		count = tetris.col - index
		for i in range(0, count):
			string_commands += "b"
	elif(index > tetris.col):
		count = index - tetris.col
		for i in range(0, count):
			string_commands += "m"
	
	return string_commands'''
        #return random.choice("mnb") * random.randint(1, 10)
	
	
       
    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "tetris" object to control the movement. In particular:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, tetris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)

            board = tetris.get_board()
            column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            index = column_heights.index(max(column_heights))
	    print(board.get_next_piece)

            if(index < tetris.col):
                tetris.left()
            elif(index > tetris.col):
                tetris.right()
            else:
                tetris.down()


###################
#### main program

#tetris1 = SimpleTetris()
#tetris1.start_game(ComputerPlayer())

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print "unknown player!"

    if interface_opt == "simple":
        tetris = SimpleTetris()
    elif interface_opt == "animated":
        tetris = AnimatedTetris()
    else:
        print "unknown interface!"

    tetris.start_game(player)

except EndOfGame as s:
    print "\n\n\n", s



