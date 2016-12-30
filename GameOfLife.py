import numpy
import sys

################################################################################
# helper methods are in this section

# converts a newline delimited input string into a numpy matrix
# added functionality for asterisks for improved visualization
def stringToMatrix(matrixAsString):
	# convert string into a format that can be used by numpy
	convertedString = ''
	tempString = matrixAsString.replace('\n', ';')
	for i in range(len(tempString)):
		# add spaces except before semicolons
		if (i+1) < len(tempString):
			if tempString[i+1] != ';':
				# no semicolon, add a space
				if (tempString[i] == '*'):
					convertedString += ('1 ')
				else:
					convertedString += (tempString[i] + ' ')
			else:
				if tempString[i] == '*':
					convertedString += '1'
				else:
					convertedString += tempString[i]
		# don't try to index past the string length (previous block is looking ahead one character)
		# but we can't do that now since were at the last index
		else:
			if (tempString[i] == '*'):
				convertedString += '1'
			else:
				convertedString += tempString[i]

	# convert formatted string to matrix
	return numpy.matrix(convertedString)

# converts a numpy matrix into a string format for printing
# added functionality for asterisks for improved visualization
def matrixToString(matrix):
	string = ''
	numRows = matrix.shape[0]
	for row in range(numRows):
		numCols = matrix[row].size
		for col in range(numCols):
			if matrix[row,col] == 1:
				string += '*'
			else:
				string += str(matrix[row,col])
			# add a newline if last column in row
			if col == (numCols-1):
				string += '\n'
	return string
		
# tries to access a given index in a given matrix, used for checking neighbors of a cell
def tryMatrix(matrix, row, col):
	# python allows for negative indexing
	# assuming we don't want a wrapping/continuous matrix, this is adverse behavior
	# so treat negative indices as non-existant neighbors, and give them 0
	if (row < 0) or (col < 0):
		return 0

	try:
		return matrix[row,col]
	except IndexError:
		# if a neighbor doesn't exist we can just treat it as a dead neighbor/0
		return 0

# calculates the next value of a single cell
def determineCell(matrix, row, col):
	cell = matrix[row,col]
	# cell neighbors, M=Middle R=Right U=Upper L=Lower or Left
	UL = tryMatrix(matrix, row-1, col-1)
	UM = tryMatrix(matrix, row-1, col)
	UR = tryMatrix(matrix, row-1, col+1)
	ML = tryMatrix(matrix, row, col-1)
	MR = tryMatrix(matrix, row, col+1)
	LL = tryMatrix(matrix, row+1, col-1)
	LM = tryMatrix(matrix, row+1, col)
	LR = tryMatrix(matrix, row+1, col+1)

	neighborsAlive = UL + UM + UR + ML + MR + LL + LM + LR
	# print str(row) + "," + str(col) + " value: " + str(cell) + " livingNeighbors: " + str(neighborsAlive)

	# cell is alive
	if cell == 1:
		if neighborsAlive < 2:
			return 0
		if neighborsAlive > 3:
			return 0
		return 1

	# cell is dead
	if cell == 0:
		if neighborsAlive == 3:
			return 1
		return 0

# prints the next generation matrix given an input matrix
def nextGeneration(matrix):
	# make a new matrix to store the next gen values
	newMatrix = numpy.zeros(matrix.shape, dtype=numpy.int)

	# iterate through the matrix and determine the next value of each cell
	numRows = matrix.shape[0] # shape returns a tuple of the dimensions
	for row in range(numRows):
		numColumns = matrix[row].size
		for column in range(numColumns):
			newMatrix[row, column] = determineCell(matrix, row, column)

	return newMatrix

################################################################################

################################################################################
# Main code is in this section

# TODO grab and convert input argument
# inputString = ''
# matrix = stringToMatrix(inputString)

# parse the command line args to get input from:
# 1. specified file (2nd arg is 'file' and 3rd arg is <filename>
#    pass in 4th arg 'loop' to allow for "looping" functionality)
# 2. as a command line argument/string (if using bash, args containing newlines must be
# 	 passed in like so: $'myStringWithNewLines\n\n\n')
# 3. using the hardcoded value below in the else block
loop = False
if len(sys.argv) > 1:
	# if the file arg is specified 2nd, then 3rd arg is the file name
	if sys.argv[1] == 'file':
		fileName = sys.argv[2]
		inputFile = open(fileName, 'r+')
		testInput = inputFile.read().rstrip() # rstrip removes whitespace, newlines, etc.
		# loop functionality
		# overwrite input file with output, so the game can continue
		if (len(sys.argv) > 3):
			if sys.argv[3] == 'loop':
				loop = True

	# otherwise, the 2nd arg is the game board in string form
	else:
		testInput = str(sys.argv[1])

# run the 'game of life' with the hardcoded test input below
else:
	testInput = '01000\n10011\n11001\n01000\n10001'

# update and output the game board
initialMatrix = stringToMatrix(testInput)
finalMatrix = nextGeneration(initialMatrix)
output = matrixToString(finalMatrix)
print output

if loop:
	# empty the file
	inputFile.truncate(0)
	# also close and reopen it or else funny stuff happens
	inputFile.close()
	inputFile = open(fileName, 'w')
	# write the new gameboard to the file
	inputFile.write(output)

inputFile.close()


################################################################################