# coding=ISO-8859-1
import sys

reload(sys)
sys.setdefaultencoding('UTF-8')

insertValuesFile=open('results/FIXED_INSERT_ALL.sql','w')

with open('results/INSERT_ALL.sql','r') as file:
    for line in file:
        for singleCharacter in line:

            if singleCharacter == 'ü':
                # Removes non-ascii characters from the query
                insertValuesFile.write('u')

            elif singleCharacter == 'ß':
                insertValuesFile.write('ss')

            elif singleCharacter == 'ö' or singleCharacter == 'ò' or singleCharacter == 'ô':
                insertValuesFile.write('o')

            elif singleCharacter == 'é' or singleCharacter == 'è' or singleCharacter == 'ê':
                insertValuesFile.write('e')

            elif singleCharacter == 'à' or singleCharacter == 'â':
                insertValuesFile.write('a')

            elif singleCharacter == 'ì':
                insertValuesFile.write('i')

            elif singleCharacter == 'ù':
                insertValuesFile.write('u')

            elif singleCharacter == 'ç':
                insertValuesFile.write('c')

            else:
                insertValuesFile.write(singleCharacter)



insertValuesFile.close()
