import sys

# Column index to count
columnIndex = sys.argv[2]

# Opens the input file
inputFileName = sys.argv[1]
inputFile = open(inputFileName, 'r')

# Reads all the lines of the input file
allLines = inputFile.readlines()

# Closes the input file
inputFile.close()

# Maximum length
maxLen = 0

# For each line read in input
for singleLine in allLines:

    # Takes each element of the row in a list
    lineFields = singleLine.split(';')

    # String representing the parameter of the column
    tempString = lineFields[int(columnIndex)]

    # Checks if the current string length is greater than the maximum
    if len(tempString) > maxLen:
        maxLen = len(tempString)


print "[STATUS 6] Maximum parameter length: " + str(maxLen)