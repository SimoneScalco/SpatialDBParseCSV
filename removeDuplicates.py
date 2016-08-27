import sys


print '[STATUS 3] Removing duplicated rows'

fileName=sys.argv[1]

#read all line of the file
file =open(fileName,'r')
lines=file.readlines()
file.close()

file=open(fileName,'w')

file.write(lines[0])

for i in range(1,len(lines)):
    str1=str(lines[i])
    str2=str(lines[i-1])

    if str1=='\n':
        file.write('\n')
        continue

    if str1!=str2:
        file.write(lines[i])
    else:
        #print "[STATUS 3] Removed line " + str(i + 1)

        continue

file.close()