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

    # Checks the maximum characters number in a specific varchar column
    for row in rows:
        riga=''.join(row).split(';')
        lungh=len(riga[column])
        if lungh>maxLenght:
            maxLenght=lungh

    return maxLenght


def parseCharacters(singleElement):

    # Substitutes non-ASCII characters with their safe representation
    for singleCharacter in singleElement:

        if singleCharacter == ';':
            insertValuesFile.write(', ')

        elif singleCharacter == '\n' or singleCharacter == '\r':
            # Removes escape characters from last element
            insertValuesFile.write('')

        elif singleCharacter == 'ü':
            # Removes non-ascii characters from the query
            insertValuesFile.write('u')

        elif singleCharacter == 'ß':
            insertValuesFile.write('ss')

        elif singleCharacter == 'ö' or singleCharacter == 'ò':
            insertValuesFile.write('o')

        elif singleCharacter == 'é' or singleCharacter == 'è':
            insertValuesFile.write('e')

        elif singleCharacter == 'à':
            insertValuesFile.write('a')

        elif singleCharacter == 'ì':
            insertValuesFile.write('i')

        elif singleCharacter == 'ù':
            insertValuesFile.write('u')

        else:
            insertValuesFile.write(singleCharacter)


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
headersTypesIsInteger = []
headersTypesRelatedTableNum = []
randomRow = random.randint(1, len(allLines)-2)
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

        headersTypesIsInteger.append(True)

    else:
        headersTypes.append("varchar(" + str(varcharMaxLenght(rowsSplitted,counterColumn) + 1) + ")")
        headersTypesIsInteger.append(False)

    counterColumn += 1

print "[STATUS] " + str(len(headersTypes)) + " types checked for the CSV headers list"



###############################################
############ CREATE TABLE FILE ################
###############################################

counter = 0
counterFile = 0
counterTableNum = 0
for singleColumnIndex in columnIndexes:

    # Opens a new file for the create tables script
    fileName = str(counterFile) + '_create_' + str(counter) + "-" + str(singleColumnIndex) + fileExtension
    createTableFile = open(directoryCreate + fileName, 'w')

    # Prints the create table statements
    createTableFile.write('CREATE TABLE ' + tableName + "_" + str(counterTableNum) + ' (\n')

    # Gets the list of column indexes related to the primary keys for the current table
    tempString = ''.join(primaryKeyIndexes[counterTableNum])
    primaryKeyColNumsSingleTable = tempString.split('_')

    primaryKeysAlreadyWritten=[]

    for singleColumnPrimaryKey in primaryKeyColNumsSingleTable:

        # Appends the name of the column in the temporary list
        primaryKeysAlreadyWritten.append(headersList[int(singleColumnPrimaryKey)])

        # Writes the name of the column of the primary key in the create table file
        createTableFile.write(headersList[int(singleColumnPrimaryKey)] + ' ' + headersTypes[int(singleColumnPrimaryKey)] + ',\n')


    counterHeader = counter
    counterRow = 0
    # Prints the headers names and their types
    for singleHeader in headersList[int(counter):int(singleColumnIndex)]:

        # Checks if the current header is in the list of the primary keys inserted before
        if not singleHeader in primaryKeysAlreadyWritten:
            createTableFile.write(singleHeader + ' ' + headersTypes[counterHeader] + ',\n')

        counterHeader += 1


    # Removes escape characters from last element
    tempString = ''.join(e for e in headersList[int(singleColumnIndex)] if e.isalnum())

    # Writes the last element in the create table file
    if not tempString in primaryKeysAlreadyWritten:
        createTableFile.write(tempString + " " + headersTypes[counterHeader] + ',\n')


    # Writes the primary keys of the table in the file
    createTableFile.write('PRIMARY KEY(')
    createTableFile.write(headersList[int(primaryKeyColNumsSingleTable[0])])
    deleteFirstElement(primaryKeyColNumsSingleTable)
    for singleColumnPrimaryKey in primaryKeyColNumsSingleTable:
        createTableFile.write(', ' + headersList[int(singleColumnPrimaryKey)])

    createTableFile.write(')')

    # Gets the list of column indexes related to the foreign keys for the current table
    tempString = ''.join(foreignKeyIndexes[counterTableNum])
    foreignKeyColNumsSingleTable = tempString.split('_')

    # Check if at least one foreign key is present (if it's different than -1)
    if(int(foreignKeyColNumsSingleTable[0]) != -1):

        # Foreign key clause
        createTableFile.write(',\n')
        createTableFile.write('FOREIGN KEY(')

        firstCycle = True

        # Writes the name of the column of the foreign key in the create table file
        for singleColumnForeignKey in foreignKeyColNumsSingleTable:

            if firstCycle:
                createTableFile.write(headersList[int(singleColumnForeignKey)])
                firstCycle = False

            else:
                createTableFile.write(', ' + headersList[int(singleColumnForeignKey)])


        # Reference clause
        createTableFile.write(') REFERENCES ' + tableName + '_' + str(headersTypesRelatedTableNum[int(singleColumnForeignKey)]) + ' (')

        firstCycle = True

        # Writes the references for the foreign keys just printed
        for singleColumnForeignKey in foreignKeyColNumsSingleTable:

            if firstCycle:
                createTableFile.write(headersList[int(singleColumnForeignKey)])
                firstCycle = False

            else:
                createTableFile.write(', ' + headersList[int(singleColumnForeignKey)])

        # Closes the foreign key statement
        createTableFile.write(')')

    # Closes create table statement
    createTableFile.write('\n);')

    # Update the counters
    counter = int(singleColumnIndex) + 1
    counterTableNum += 1
    counterFile += 1

    # Close create table file
    createTableFile.close()


print "[STATUS] Create table statements have been written in '" + directoryCreate + "'"


###############################################
############### INSERT FILE ###################
###############################################


# Writes all the insert statements in the file
for singleRow in rowsSplitted:

    # Convert the row list into string
    singleRowString = ''.join(singleRow)
    singleRowListDivided = singleRowString.split(';')

    counter = 0
    counterFile = 0
    counterTableNum = 0
    # For each subdivision in input
    for singleColumnIndex in columnIndexes:

        # Dictionary used to track and write the insert values and their names in the same order
        dictionaryRow = {}


        counterDictionary = counter
        # Inserting the headers and their values for the current row in the dictionary
        for singleHeader in headersList[counter:int(singleColumnIndex)+1]:

            dictionaryRow[singleHeader] = singleRowListDivided[counterDictionary]

            counterDictionary += 1

        # Re-building the primary key column indexes list (in fact the previous construction has been altered)
        primaryKeyColNumsSingleTable = ''.join(primaryKeyIndexes[counterTableNum]).split('_')

        # Inserting the primary keys and their values for the current row in the dictionary
        for singleColumnPrimaryKey in primaryKeyColNumsSingleTable:

            dictionaryRow[headersList[int(singleColumnPrimaryKey)]] = singleRowListDivided[int(singleColumnPrimaryKey)]

        #print dictionaryRow



        # Opens a new file for the insert scripts
        fileName = str(counterFile) + '_insert_' + str(counter) + "-" + str(singleColumnIndex) + fileExtension
        insertValuesFile = open(directoryInsert + fileName, 'a')

        # Writes the insert statement clause
        insertValuesFile.write('INSERT INTO ' + tableName + '_' + str(counterTableNum) + '(')

        # Writing all the names and the values inserted in the dictionary
        firstCycle=True
        for singleKey in dictionaryRow:

            # Removes the possible escape characters in the strings
            tempString = ''.join(e for e in singleKey if e.isalnum())

            if firstCycle:
                insertValuesFile.write(tempString)
                firstCycle=False
            else:
                insertValuesFile.write(', ' + tempString)

        insertValuesFile.write(') VALUES(')

        counterElementNum = counter
        # Check characters of every single element extracted from the row
        firstCycle=True
        for singleElement in dictionaryRow:

            if firstCycle:
                firstCycle=False
            else:
                insertValuesFile.write(', ')

            # Check if we need to write into a varchar
            if not str(dictionaryRow[singleElement]).isdigit():

                insertValuesFile.write("'")

                # Parse rare characters and substitute them
                parseCharacters(dictionaryRow[singleElement])

                insertValuesFile.write("'")

            else:
                # Parse rare characters and substitute them
                parseCharacters(dictionaryRow[singleElement])

            # Update the counter of the elements
            counterElementNum += 1

        # Closes the insert statement
        insertValuesFile.write(');\n')

        # Update the counters
        counter = int(singleColumnIndex) + 1
        counterTableNum += 1
        counterFile += 1


    # Close insert
    insertValuesFile.close()


print "[STATUS] Insert queries have been written in '" + directoryInsert + "'"