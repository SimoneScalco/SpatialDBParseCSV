# coding=ISO-8859-1
import sys

reload(sys)
sys.setdefaultencoding('UTF-8')

insertValuesFile=open('results/DB_EXTRA_FIXED_elenco_comuni.sql','w')

with open('results/DB_EXTRA_elenco_comuni.sql','r') as file:
    for line in file:
        for singleCharacter in line:

            if singleCharacter == '�':
                # Removes non-ascii characters from the query
                insertValuesFile.write('u')

            elif singleCharacter == '�':
                insertValuesFile.write('ss')

            elif singleCharacter == '�' or singleCharacter == '�' or singleCharacter == '�':
                insertValuesFile.write('o')

            elif singleCharacter == '�' or singleCharacter == '�' or singleCharacter == '�' or singleCharacter == '\xa8':

                insertValuesFile.write('e')

            elif singleCharacter == '\xc3':

                insertValuesFile.write('')

            elif singleCharacter == '�' or singleCharacter == '�' or singleCharacter == '\xa0':
                insertValuesFile.write('a')

            elif singleCharacter == '�':
                insertValuesFile.write('i')

            elif singleCharacter == '�':
                insertValuesFile.write('u')

            elif singleCharacter == '�':
                insertValuesFile.write('c')

            else:
                insertValuesFile.write(singleCharacter)



insertValuesFile.close()
