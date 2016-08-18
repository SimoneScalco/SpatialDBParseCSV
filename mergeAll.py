outputFile=open('results/DB.sql','w')
inputFile=open("results/create_tables/DIRECTORY_MERGE.sql","r")

print '[STATUS 5] merging DIRECTORY_MERGE files...'

lines=inputFile.readlines()

for line in lines:
    outputFile.write(line)

inputFile.close()

inputFile=open('results/insert_queries/DIRECTORY_MERGE.sql','r')
lines=inputFile.readlines()

for line in lines:
    outputFile.write(line)

inputFile.close()
outputFile.close()

print '[STATUS 5] done'