# coding=ISO-8859-1
import random
import sys

# Load the correct encoding
reload(sys)
sys.setdefaultencoding('UTF-8')

# Function that checks if an object is an integer or not
def checkIfInteger(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def detectPSQLOverflow(i):

    # Gets the integer value from the object representation
    mayOverflow = int(i)

    # Checks if the integer does not overflow the 32-bit representation of PostgreSQL
    if mayOverflow > 2147483647:
        print "[ALERT] Integer value " + str(i) + " may overflow in DB insertion. Converting to bigint..."
        return True

    else:
        return False

# Function that deletes the first element of a list
def deleteFirstElement(s):
    del s[0]


def parseCharacters(singleElement):

    for singleCharacter in singleElement:

        if singleCharacter == ';':
            insertValuesFile.write(', ')
            insertValuesFileRaw.write(', ')

        elif singleCharacter == '\n' or singleCharacter == '\r':
            # Removes escape characters from last element
            insertValuesFile.write('')
            insertValuesFileRaw.write('')

        elif singleCharacter == 'ü':
            # Removes non-ascii characters from the query
            insertValuesFile.write('u')
            insertValuesFileRaw.write('u')

        elif singleCharacter == 'ß':
            insertValuesFile.write('B')
            insertValuesFileRaw.write('B')

        else:
            insertValuesFile.write(singleCharacter)
            insertValuesFileRaw.write(singleCharacter)


# Opens dataset
datasetFileName = sys.argv[2]
datasetFile = open(str(datasetFileName), 'r')

# Read lines from test file
allLines = datasetFile.readlines()

datasetFile.close()

# Init empty lists and other parameters
directoryInsert = 'results/insert_queries/'
directoryCreate = 'results/create_tables/'
directoryInsertRaw = directoryInsert + 'raw/'
fileExtension = '.sql'
tableName = "census_area"
rowsSplitted = []
headersList = []
headersTypes = []
headersTypesBool = []
randomRow = random.randint(1, len(allLines)-2)
commandLineArguments = ''.join(sys.argv[1]).split(',')

print "[STATUS] Input arguments: " + str(commandLineArguments)

# Gets the header of each column and appends it to the header list
firstLine = allLines[0].split(',')
for singleAttribute in firstLine[0].split(';'):
    headersList.append(singleAttribute)

print "[STATUS] Headers copied: " + str(len(headersList))

counter = 0
# Create a list from the CSV file (each CSV row becomes an element)
for singleRow in allLines:
    rowsSplitted.append(singleRow.split(','))
    counter += 1

# Deletes the first element of the list (which contained the headers)
deleteFirstElement(rowsSplitted)


counterColumn = 0
# Checks the headers type by reading the lines of the file
for singleHeader in headersList:

    singleRow = ''.join(rowsSplitted[randomRow]).split(';')

    if checkIfInteger(singleRow[counterColumn]):

        if detectPSQLOverflow(singleRow[counterColumn]):
            headersTypes.append("bigint")

        else:
            headersTypes.append("integer")

        headersTypesBool.append(True)

    else:
        headersTypes.append("varchar(30)")
        headersTypesBool.append(False)

    counterColumn += 1

print "[STATUS] " + str(len(headersTypes)) + " types checked for the CSV headers list"



###############################################
############ CREATE TABLE FILE ################
###############################################

counter = 0
counterFile = 0
counterTableNum = 0
for singleCommandLineArgument in commandLineArguments:

    # Opens a new file for the create tables script
    fileName = str(counterFile) + '_create_' + str(counter) + "-" + str(singleCommandLineArgument) + fileExtension
    createTableFile = open(directoryCreate + fileName, 'w')

    # Prints the create table statements
    createTableFile.write('CREATE TABLE ' + tableName + "_" + str(counterTableNum) + ' (\n')

    # Cycle variables
    counterHeader = counter
    counterRow = 0
    # Prints the headers names and their types
    for singleHeader in headersList[int(counter):int(singleCommandLineArgument)]:
        createTableFile.write(singleHeader + ' ' + headersTypes[counterHeader] + ',\n')
        counterHeader += 1

    # Removes escape characters from last element
    tempString = ''.join(e for e in headersList[int(singleCommandLineArgument)] if e.isalnum())

    # Closes the create table statement
    createTableFile.write(tempString + " " + headersTypes[counterHeader])
    createTableFile.write('\n);')

    # Update the counters
    counter = int(singleCommandLineArgument)+1
    counterTableNum += 1
    counterFile += 1

    # Close create table file
    createTableFile.close()


print "[STATUS] Create table statements have been written in '" + directoryCreate + "'"


###############################################
############### INSERT FILE ###################
###############################################


# Prints the all the insert statements in the file
for singleRow in rowsSplitted:

    # Convert the row list into string
    singleRowString = ''.join(singleRow)
    singleRowListDivided = singleRowString.split(';')

    counter = 0
    counterFile = 0
    counterTableNum = 0
    # For each subdivision in input
    for singleCommandLineArgument in commandLineArguments:

        # Opens a new file for the insert scripts
        fileName = str(counterFile) + '_insert_' + str(counter) + "-" + str(singleCommandLineArgument) + fileExtension
        insertValuesFile = open(directoryInsert + fileName, 'a')
        insertValuesFileRaw = open(directoryInsertRaw + fileName, 'a')

        # Prints the insert statement
        insertValuesFile.write('INSERT INTO ' + tableName + '_' + str(counterTableNum) + ' VALUES(')


        counterElementNum = counter
        # Check characters of every single element from the row
        for singleElement in singleRowListDivided[counter:int(singleCommandLineArgument)+1]:

            # Check if we need to write into a varchar
            if headersTypesBool[counterElementNum] == False:

                insertValuesFile.write("'")
                insertValuesFileRaw.write("'")

                # Parse rare characters and substitute them
                parseCharacters(singleElement)

                insertValuesFile.write("'")
                insertValuesFileRaw.write("'")

            else:
                # Parse rare characters and substitute them
                parseCharacters(singleElement)

            # Check if this is the last element that should be printed in the query
            if counterElementNum != int(singleCommandLineArgument):
                insertValuesFile.write(', ')
                insertValuesFileRaw.write(",")

            counterElementNum += 1

        # Closes the insert statement
        insertValuesFile.write(');\n')
        insertValuesFileRaw.write("\n")

        # Update the counters
        counter = int(singleCommandLineArgument) + 1
        counterTableNum += 1
        counterFile += 1


    # Close insert
    insertValuesFile.close()
    insertValuesFileRaw.close()


print "[STATUS] Insert queries have been written in '" + directoryInsert + "'"