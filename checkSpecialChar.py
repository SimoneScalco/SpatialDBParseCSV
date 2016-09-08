
charachters={}

with open('results/INSERT_ALL.sql','r') as file:
    for line in file:
        for c in line:
            charachters[c]=1


print charachters

outFile=open('results/chars.txt','w')

for k in charachters:
    outFile.write(str(k)+'\n')

outFile.close()
