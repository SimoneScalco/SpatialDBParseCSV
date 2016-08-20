
# Output file handler
outputFileName = 'results/DB.sql'
outputFile=open(outputFileName,'w')

# First input file handler (create tables directory)
inputFile=open("results/create_tables/DIRECTORY_MERGE.sql","r")

print '[STATUS 5] Merging DIRECTORY_MERGE files...'

# Gets all the lines from the input file
lines=inputFile.readlines()

# Writes all the data just read to the output file
for line in lines:
    outputFile.write(line)

inputFile.close()


# Second input file handler (insert queries directory)
inputFile=open('results/insert_queries/DIRECTORY_MERGE.sql','r')

# Gets all the lines from the input file
lines=inputFile.readlines()

# Writes all the data just read to the output file
for line in lines:
    outputFile.write(line)

inputFile.close()
outputFile.close()

print '[STATUS 5] All local merged files have been copied entirely in ' + outputFileName