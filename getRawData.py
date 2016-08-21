
import os
import sys


# Get working directories and extension
directory = sys.argv[1]
directoryRaw = directory + 'raw/'
extension = '.sql'

# Gets the list of files for the directory to inspect
filesList = os.listdir(directory)
filesList.sort()

# For each file in the directory
for fileName in filesList:

    # Check if the file name meets the initial requirements
    if not (fileName.startswith('DIRECTORY')) and fileName.endswith(extension):

        # Opens the output file
        outputFile = open(directoryRaw + fileName + '_RAW' + extension, 'w')

        # Opens the input file
        inputFile = open(directory + fileName, 'r')

        # Reads all the lines of the input file
        lines = inputFile.readlines()

        # Closes the input file
        inputFile.close()

        # For each row in the input file
        for singleRow in lines:

            # Check if the current row is an insert query
            if singleRow.startswith('INSERT'):

                # Splits the row and writes the raw data in the output file
                tempRow = singleRow.split('(')
                outputFile.write(tempRow[2].split(')')[0])

            outputFile.write('\n')

        outputFile.write('\n\n\n')

    # Close the output file
    outputFile.close()