import sys
import copy
import re
import os


directory = sys.argv[1] + '/'
extension = '.csv'

# Gets the list of files for the directory to inspect
filesList = os.listdir(directory)

# Opens the output file
outputFileName = 'mergeThemAllPokemon'
outputFile = open(directory + outputFileName + extension, 'w')

firstCycle = True

for fileName in filesList:

    inputFileName = directory + fileName
    inputFile = open(inputFileName, 'r')

    allLines = inputFile.readlines()

    if firstCycle:

        firstCycle = False

    else:

        del allLines[0]

    for singleLine in allLines:
        outputFile.write(singleLine)

    inputFile.close()

outputFile.close()