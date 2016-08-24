
import sys

# Gets the input file name
inputFileName = sys.argv[1]
outputFileName = sys.argv[2]

# Output file handler
outputFile=open('results/' + outputFileName,'w')

# First input file handler (create tables directory)
inputFile=open('results/create_tables/' + inputFileName,'r')

# Optional input parameters
if len(sys.argv) > 3:

    # Gets the script name and opens the file
    inputSQLClearScriptName = sys.argv[3]
    inputSQLClearScript = open('Scripts_vari/' + inputSQLClearScriptName, 'r')

    # Reads all the lines in the file
    lines = inputSQLClearScript.readlines()

    # Writes all the data just read to the output file
    for line in lines:
        outputFile.write(line)

    outputFile.write('\n\n\n')

    inputSQLClearScript.close()

print '[STATUS 5] Merging DIRECTORY_MERGE files...'

# Gets all the lines from the input file
lines=inputFile.readlines()

# Writes all the data just read to the output file
for line in lines:
    outputFile.write(line)

inputFile.close()


# Second input file handler (insert queries directory)
inputFile=open('results/insert_queries/' + inputFileName,'r')

# Gets all the lines from the input file
lines=inputFile.readlines()

# Writes all the data just read to the output file
for line in lines:
    outputFile.write(line)

inputFile.close()
outputFile.close()

print '[STATUS 5] All local merged files have been copied entirely in ' + outputFileName