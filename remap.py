import sys
import copy

arguments=copy.copy(sys.argv)
fileName=arguments[1]

print '[STATUS 4]remapping table names...'

del arguments[0]
del arguments[0]

inputFile=open(fileName,'r')
lines=inputFile.readlines()
inputFile.close()

for argument in arguments:
    oldName=str(argument).split(':')[0]
    newName=str(argument).split(':')[1]
    for i in range(0,len(lines)):
        lines[i]=lines[i].replace(oldName,newName)

outputFile=open(fileName,'w')

for line in lines:
    outputFile.write(line)

outputFile.close()

print '[STATUS 4]done'