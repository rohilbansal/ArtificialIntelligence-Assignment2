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
# My main approach to of formulating this search algorithm was that I will try to find the all the possible permutations of 
# all the possible moves on the board and then calculate the best available move based on the score calculated by my heuristics.
# State space: The state space if my whole 10x20 board
# Successor Function : The successor function is my piece that is to be placed on the board, that is the current piece
# Edge Weights: Although all the moves have equal edge weights in general, but when my algorithm works, it assigns 
# a score to every move and then based on that score, the algorithm decides to proceed with the move with the maximum score. Then 
# in that sense, there is a weight or a score attached to every move.
# Heuristic Functions: I have formulated quite a few heuristic functions which will calculate the score for every move:
#    	1) Maximum number of X’s: This heuristic evaluates every move and if any move places or increases number of X’s starting from the 
#          bottom level, then a good score is assigned to that move. And suppose if any move reduces the number of X’s at some level, then 
#          that means some line completion must’ve occurred and then that move is given a high good score because we want to achieve as high score as possible.
#)	2) Calculate Wells: The wells or depressions in the board in undesired. For eg. If column has height of 15 and column 2 has height 1 and 
#          again column 3 has height of 13, then that mean a kind of depression has been created on our board. And any move which helps in the 
#          creation of a depression is penalized.
#)	3) Calculate aggregate height: The aggregate height of the board is calculated for every move and then it is compared with the aggregate 
#          height of the original board. If our move increases the aggregate height of our board, then that move is penalized.
#)	4) Calculate holes: Holes are small squares in the board which has no X’s but they are covered with X’s from all 4 sides. These holes 
#          are harder to fill and hence are undesired and any move which creates holes is penalized
#)	5) Touching the floor: Any move which makes the piece fall on the floor is rewarded, because a piece falling on the floor means that 
#          the piece is closer to the ground and has no height.
#
#
# Question 2:
# the search algorithm first tries to calculate all the possible permutations of the moves, i.e where and how the piece can be placed on the board. Thses
# permutations are added to a dictionary with key as the moves needed to achieve that state say "nnmmmm" and the value is a list which contains the state
# of the board after executing that move and a score attached ot it which is initialized as 0. then that dictionary is passed to every heuristic which then
# calculates the score based on the conditions. The move with the highest score is chosen and if two moves have the same score, then then any move is
# chosen at random.
#
# Question 3: Initially i faced some problems with python programming, because I'm relatively new to python and I am not familiar with how python
# deals with object oriented concepts. Also finding the permutations of all the moves was a bit harder initially.
# Also, one assumption that my program makes is that all the pieces are equally probable which is quite not the case but this is one assumption. Also secondly,
# the rewards or the penalty assigned to any heuristic is purely based on gut feeling and just assumed how good a penalty or a reward should be
# given the particular heuristic and the conditions.
# References: For designing the heuristic functions, the follwing website came in handy:
# https://luckytoilet.wordpress.com/2011/05/27/coding-a-tetris-ai-using-a-genetic-algorithm/

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
		#print("Orig",count2,"new",count)
		if(count2 > count):
			newBoardList[elements][1] += (10.0)*count
			countList[elements] = 10+count
		else:
			newBoardList[elements][1] += (4.0)*count
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
                        	newBoardList[elements][1] += (10.0)*count
                        	countList[elements] = 10+count
			else:
				newBoardList[elements][1] += (4.0)*count
                        	countList[elements] = count
                #print("inside j count", countList)
                j += 1
                #print("inside j value", j)
	#print(newBoardList)
	return newBoardList
	#return(max(countList.iteritems(), key=operator.itemgetter(1))[0])
    
    def calculateAggregateHeight(self, newBoardList, tetris_orig):
	orig_board = tetris_orig.get_board()
	for elements in newBoardList:
		count = 0
		final_count = 0
		final_count2 = 0
		for i in range(0,10):
			count = 0
			count2 = 0
			for j in range(0,20):
				if(count == 0):
					if(newBoardList[elements][0][j][i] == "x"):
						count += 1
						final_count += 20-j
				if(count2 == 0):
					if(orig_board[j][i] == "x"):
						count2 += 1
						final_count2 += 20-j
		#oldCount = newBoardList[elements][1]
		#count = oldCount + (-2.0)*count
		if(final_count > final_count2):
			newBoardList[elements][1] += (final_count - final_count2)*(-20.0)
	return newBoardList

    def checkIfTouchingWall(self, newBoardList, tetris_orig):
	orig_board = tetris_orig.get_board()
	for elements in newBoardList:
		count = 0
		count2 = 0
		for i in range(0, 20):
			if(newBoardList[elements][0][i][0] == "x"):
				count += 1
			if(newBoardList[elements][0][i][9] == "x"):
				count += 1
			if(orig_board[i][0] == "x"):
				count2 += 1
			if(orig_board[i][9] == "x"):
				count2 += 1
		if(count > count2):
			newBoardList[elements][1] += (count - count2)*(0.5)
	return newBoardList

    def checkTouchingGround(self, newBoardList, tetris_orig):
	orig_board = tetris_orig.get_board()
	for elements in newBoardList:
		count = 0
		count2 = 0
		for i in range(0, 10):
			if(newBoardList[elements][0][19][i] == "x"):
				count += 1
			if(orig_board[19][i] == "x"):
				count2 += 1
		if(count > count2):
			newBoardList[elements][1] += (count-count2)*(10.0)
	return newBoardList 

    def calculateHoles(self, newBoardList, tetris_orig):
	holes = 0
	holes2= 0
	orig_board = tetris_orig.get_board()
	for elements in newBoardList:
		for i in range(0, 20):
			count = 0
			count2 = 0
			for j in range(0, 10):
				if(newBoardList[elements][0][19-i][j] == "x"):
					count += 1
				if(orig_board[19-i][j] == "x"):
					count2 += 1
			if(count != 0):
				holes += 10-count
			if(count2 != 0):
				holes2 += 10-count2
		if(holes > holes2):
			newBoardList[elements][1] += -1.0
	return newBoardList

    def calculateWells(self, newBoardList, tetris_orig):
	orig_board = tetris_orig.get_board()
	for elements in newBoardList:
		count = 0
                final_count = 0
                list1 = []
                for i in range(0,10):
			count = 0
			for j in range(0, 20):
				if(newBoardList[elements][0][j][i] == "x"):
					count = 20-j
					break
			if(i == 0):
				final_count = count
			else:
				list1.append(float(abs(final_count-count)))
				final_count = count
		sumVal = 0
		#print(list1)
		for values in list1:
			sumVal += values
		#print(sumVal)
		for i in range(0,10):
                        count = 0
                        for j in range(0, 20):
                                if(orig_board[j][i] == "x"):
                                        count = 20-j
                                        break
                        if(i == 0):
                                final_count = count
                        else:
                                list1.append(float(abs(final_count-count)))
                                final_count = count
		sumVal2 = 0
		for values in list1:
			sumVal2 += values
		#print(sumVal2)
		if(sumVal > sumVal2):
			newBoardList[elements] += (sumVal-sumVal2)*(-3.0)
		#elif( sumVal2 > sumVal):
		#	newBoardList[elements] += (sumVal2-sumVal)*(3.0)
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
		#board2 = copy.deepcopy(board1)
			pieceInfo = tetris1.get_piece()
			pieceColumn = pieceInfo[2]
			#print("piece column", pieceColumn)
			string_commands_copy = string_commands
			tetris2 = copy.deepcopy(tetris1)
			for i in range(0, pieceColumn):
				for j in range(0, i+1):
					tetris2.left()
					string_commands_copy += "b"
				tetris2.down()
				newBoardList[string_commands_copy] = [tetris2.get_board(), 0]
				string_commands_copy = string_commands
				tetris2 = copy.deepcopy(tetris1)
			string_commands_copy = string_commands
			tetris2 = copy.deepcopy(tetris1)
			for i in range(0, 10-pieceColumn):
				for j in range(0, i):
					tetris2.right()
					string_commands_copy += "m"
				tetris2.down()
				newBoardList[string_commands_copy] = [tetris2.get_board(), 0]
				string_commands_copy = string_commands
				tetris2 = copy.deepcopy(tetris1)
		'''
		while(pieceColumn >= 0):
			tetris1.left()
			string_commands_copy += "b"
			tetris1.down()
			newBoardList[string_commands_copy] = [tetris1.get_board(), 0]
			pieceColumn -= 1
			tetris1 = copy.deepcopy(tetris_orig)
		string_commands_copy = string_commands
		while(pieceColumn < 20):
			tetris1.right()
			string_commands_copy += "m"
			tetris1.down()
			newBoardList[string_commands_copy] = [tetris1.get_board(), 0]
			tetris1 = copy.deepcopy(tetris_orig)

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
		#print(newBoardList)'''
	#print(newBoardList)
	newBoardList = self.calculateNumberOfXs(newBoardList, tetris_orig)
	#print(newBoardList)
	newBoardList = self.calculateAggregateHeight(newBoardList, tetris_orig)
	temp_dict = {}
        for val in newBoardList:
                temp_dict[val] = newBoardList[val][1]
        #print("Height",temp_dict)

	newBoardList = self.checkIfTouchingWall(newBoardList, tetris_orig)
	#newBoardList = self.calculateHoles(newBoardList, tetris_orig)
	newBoardList = self.checkTouchingGround(newBoardList, tetris_orig)
	newBoardList = self.calculateWells(newBoardList, tetris_orig)
	temp_dict = {}
	for val in newBoardList:
		temp_dict[val] = newBoardList[val][1]
	#print(temp_dict)
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
	    '''
            column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            index = column_heights.index(max(column_heights))
	    
            if(index < tetris.col):
                tetris.left()
            elif(index > tetris.col):
                tetris.right()
            else:
                tetris.down()'''
	    strVal = self.checkPermutations(board, tetris)
	    #print(strVal)
	    for i in range(0, len(strVal)):
	    	if(strVal[i] == "b"):
	    		tetris.left()
	   	elif(strVal[i] == "m"):
			tetris.right()
		elif(strVal[i] == "n"):
			tetris.rotate()
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



