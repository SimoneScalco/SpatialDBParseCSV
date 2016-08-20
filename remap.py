import sys
import copy

# Gets the command line arguments inserted by the user
arguments=copy.copy(sys.argv)
fileName=arguments[1]

print '[STATUS 4] Remapping table names...'

# Deletes the script names from the command line arguments list
del arguments[0]
del arguments[0]

# Input file handler
inputFile=open(fileName,'r')

# Reads all the lines written in the input file
lines=inputFile.readlines()
inputFile.close()

# Remapping of the table names
for argument in arguments:

    # Parsing the remap inserted by the user as command line argument
    oldName=str(argument).split(':')[0]
    newName=str(argument).split(':')[1]

    # Replacing old table names with the new ones
    for i in range(0,len(lines)):
        lines[i]=lines[i].replace(oldName,newName)

# Writing the output file
outputFile=open(fileName,'w')
for line in lines:
    outputFile.write(line)

outputFile.close()

print '[STATUS 4] Requested table names have been remapped'