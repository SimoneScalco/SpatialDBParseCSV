
import sys
import os


# Get working directories and extension
directory = sys.argv[1]
extension = sys.argv[2]


# Gets the list of files for the directory to inspect
filesList = os.listdir(directory)
filesList.reverse()

filesListIndexes = []
# Gets the first column integer
for fileName in filesList:
    fileIndex = fileName.split('_')[1].split('-')[0]
    filesListIndexes.append(fileIndex)
    print fileName

sorted(filesList, key=lambda fileColumnIndex: filesListIndexes)

print filesList

# Opens the output file
outputFileName = 'DIRECTORY_MERGE'
outputFile = open(directory + outputFileName + extension, 'a')

# Checks if
for fileName in filesList:

    # Checks if the file meets the requirements
    if fileName.endswith(extension):

        print "[STATUS 2] Merging '" + fileName + "' with master file (path: '" + directory + "')"
        outputFile.write('--' + fileName + '\n')

        # Opens the file that needs to be appended to the output one
        inputFile = open(directory + fileName, 'r')

        # Reads the file
        allLines = inputFile.readlines()

        # Appends every line in the output file
        for singleLine in allLines:
            outputFile.write(singleLine)

        outputFile.write('\n\n\n')

        # Closes input file
        inputFile.close()

# Closes output file
outputFile.close()