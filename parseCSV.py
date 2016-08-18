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

def varcharMaxLenght(rows,column):
    maxLenght=0

    for row in rows:
        riga=''.join(row).split(';')
        lungh=len(riga[column])
        if lungh>maxLenght:
            maxLenght=lungh

    return maxLenght


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
            insertValuesFile.write('ss')
            insertValuesFileRaw.write('ss')

        elif singleCharacter == 'ö' or singleCharacter == 'ò':
            insertValuesFile.write('o')
            insertValuesFileRaw.write('o')

        elif singleCharacter == 'é' or singleCharacter == 'è':
            insertValuesFile.write('e')
            insertValuesFileRaw.write('e')

        elif singleCharacter == 'à':
            insertValuesFile.write('a')
            insertValuesFileRaw.write('a')

        elif singleCharacter == 'ì':
            insertValuesFile.write('i')
            insertValuesFileRaw.write('i')

        elif singleCharacter == 'ù':
            insertValuesFile.write('u')
            insertValuesFileRaw.write('u')

        else:
            insertValuesFile.write(singleCharacter)
            insertValuesFileRaw.write(singleCharacter)


# Opens dataset
datasetFileName = sys.argv[1]
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
headersTypesRelatedTableNum = []
randomRow = random.randint(1, len(allLines)-2)
#commandLineArguments = ''.join(sys.argv[2]).split(',')
columnIndexes = []
primaryKeyIndexes = []
foreignKeyIndexes = []

# Copies the command line parameters considering a specific syntax
for counterCommandLineArguments in range(2, len(sys.argv)):

    # Copies the column indexes for the tables division
    tempString = ''.join(sys.argv[counterCommandLineArguments])
    columnIndexes.append(tempString.split(',')[0])

    # Copies the primary keys
    tempString = ''.join(sys.argv[counterCommandLineArguments])
    primaryKeyIndexes.append(tempString.split(',')[1])

    # Copies the foreign keys
    tempString = ''.join(sys.argv[counterCommandLineArguments])
    foreignKeyIndexes.append(tempString.split(',')[2])


print "[STATUS] Input arguments: " + str(columnIndexes)

# Gets the header of each column and appends it to the header list
firstLine = allLines[0].split(',')
for singleAttribute in firstLine[0].split(';'):
    headersList.append(singleAttribute)


print "[STATUS] Headers copied: " + str(len(headersList))

counter = 0
counterTableNum = 0
# Appends the related table numbers for each header in the previous list
for singleColumnIndex in columnIndexes:

    for currentHeaderCounter in range(counter, int(singleColumnIndex)+1):

        # Appends the related table number in a new list
        headersTypesRelatedTableNum.append(counterTableNum)

    # Updates the counters
    counterTableNum += 1
    counter = int(singleColumnIndex) + 1


print "[STATUS] Table num headers appended: " + str(len(headersTypesRelatedTableNum))

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
        headersTypes.append("varchar("+str(varcharMaxLenght(rowsSplitted,counterColumn)+1)+")")
        headersTypesBool.append(False)

    counterColumn += 1

print "[STATUS] " + str(len(headersTypes)) + " types checked for the CSV headers list"



###############################################
############ CREATE TABLE FILE ################
###############################################

counter = 0
counterFile = 0
counterTableNum = 0
for singleCommandLineArgument in columnIndexes:

    # Opens a new file for the create tables script
    fileName = str(counterFile) + '_create_' + str(counter) + "-" + str(singleCommandLineArgument) + fileExtension
    createTableFile = open(directoryCreate + fileName, 'w')

    # Prints the create table statements
    createTableFile.write('CREATE TABLE ' + tableName + "_" + str(counterTableNum) + ' (\n')

    # Adding primary keys as table attributes
    tempString = ''.join(primaryKeyIndexes[counterTableNum])
    primaryKeyList = tempString.split('_')

    primaryKeyTemp=[]

    for singlePrimaryKeyColumn in primaryKeyList:
        print singlePrimaryKeyColumn
        primaryKeyTemp.append(headersList[int(singlePrimaryKeyColumn)])
        createTableFile.write(headersList[int(singlePrimaryKeyColumn)] + ' ' + headersTypes[int(singlePrimaryKeyColumn)] + ',\n')

    #print headersList[int(counter):int(singleCommandLineArgument)+1]
    #print primaryKeyTemp
    # Cycle variables
    counterHeader = counter
    counterRow = 0
    # Prints the headers names and their types
    for singleHeader in headersList[int(counter):int(singleCommandLineArgument)]:

        if not singleHeader in primaryKeyTemp:
            createTableFile.write(singleHeader + ' ' + headersTypes[counterHeader] + ',\n')
        counterHeader += 1


    # Removes escape characters from last element
    tempString = ''.join(e for e in headersList[int(singleCommandLineArgument)] if e.isalnum())

    # Prints the last element
    if not tempString in primaryKeyTemp:
        createTableFile.write(tempString + " " + headersTypes[counterHeader] + ',\n')

    # Printing the primary key of the table
    createTableFile.write('PRIMARY KEY(')
    createTableFile.write(headersList[int(primaryKeyList[0])])
    del primaryKeyList[0]
    for singlePrimaryKeyColumn in primaryKeyList:
        createTableFile.write(', ' + headersList[int(singlePrimaryKeyColumn)])

    createTableFile.write(')')

    # Printing the foreign keys of the table
    tempString = ''.join(foreignKeyIndexes[counterTableNum])
    foreignKeyList = tempString.split('_')

    # Check if at least one foreign key is present
    if(int(foreignKeyList[0]) != -1):

        createTableFile.write(',\n')
        createTableFile.write('FOREIGN KEY(')
        firstCycle = True

        # Writes the foreign keys that need to be referenced in the current table
        for singleForeignKeyColumn in foreignKeyList:

            if firstCycle:
                createTableFile.write(headersList[int(singleForeignKeyColumn)])
                firstCycle = False

            else:
                createTableFile.write(', ' + headersList[int(singleForeignKeyColumn)])


        # Reference clause
        createTableFile.write(') REFERENCES ' + tableName + '_' + str(headersTypesRelatedTableNum[int(singleForeignKeyColumn)]) + ' (')
        firstCycle = True

        # Writes the reference for the foreign keys just printed
        for singleForeignKeyColumn in foreignKeyList:

            if firstCycle:
                createTableFile.write(headersList[int(singleForeignKeyColumn)])
                firstCycle = False

            else:
                createTableFile.write(', ' + headersList[int(singleForeignKeyColumn)])

        # Closes the foreign key statement
        createTableFile.write(')')

    # Closes create table statement
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
    for singleCommandLineArgument in columnIndexes:

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

                insertValuesFile.write("\"")
                insertValuesFileRaw.write("\"")

                # Parse rare characters and substitute them
                parseCharacters(singleElement)

                insertValuesFile.write("\"")
                insertValuesFileRaw.write("\"")

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