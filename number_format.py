import sys
import copy
import re

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

reg=re.compile('[0-9]+\,[0-9]+')



# Parsing the remap inserted by the user as command line argument
#oldName=str(argument).split(':')[0]
#newName=str(argument).split(':')[1]

# Replacing old table names with the new ones
for i in range(0,len(lines)):
    linea=lines[i].split(";")
    lines[i]=''

    firstCycle=True;
    counter = 0
    for lin in linea:

        # Check if the string matches the pattern of our regular expression
        if reg.match(lin)!=None:

            lin=lin.replace(',','.')
            counter += 1

        if firstCycle:

            lines[i]=lines[i]+lin.split('\n')[0]
            firstCycle=False;

        else:

            lines[i]=lines[i]+';'+lin.split('\n')[0]


    lines[i]=lines[i]+'\n'

print '[NUMBER FORMAT] Lines replaced: ' + str(counter)

# Writing the output file
outputFile=open(fileName,'w')
for line in lines:
    outputFile.write(line)

outputFile.close()

print '[NUMBER FORMAT] Requested table names have been remapped'