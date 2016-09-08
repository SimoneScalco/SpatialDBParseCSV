
# Dictionary of characters
charachters={}

# Opens the INSERT_ALL file and reads every line, then appends the content in the dictionary
with open('results/INSERT_ALL.sql','r') as file:
    for line in file:
        for c in line:
            charachters[c]=1


print charachters

# Opens the output file
outFile=open('results/chars.txt','w')

# For each character in the dictionary, write it in the output file
for k in charachters:
    outFile.write(str(k)+'\n')

# Closes the output file
outFile.close()
