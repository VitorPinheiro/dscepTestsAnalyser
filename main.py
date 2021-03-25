import pandas as pd
import xlsxwriter

# Falta colocar generico para qualquer quantidade de operadores.
# Ja ta imprimindo no Excel
# Falta Plotar os graficos também, talvez podemos plotar dos DFs... mas se for mto complicado, plota no excel mesmo.

# Entradas do script
number_of_operators = 1
query_num = 11
numOfTweets = 1430
TestNum = 1

# Variaveis
folder_name = "Query{numQuery}-intra-{numOp}-{numTweets}-Test{numTest}-auto".format(numQuery=query_num,
                                                                              numOp=number_of_operators,
                                                                              numTweets=numOfTweets,
                                                                               numTest = TestNum);
print("folder_name1 = "+folder_name)
folder_name2 = "Query11-intra-2-1430-Test1-final";

#"SOpbasicOp1_node_1_query_11Speed"

speedFile1 = "SOpbasicOp1_node_1_query_11Speed.txt"
speedFile2 = "SOpbasicOp2_node_1_query_11Speed.txt"
aggFile = "Agg_node_1_query_11Speed.txt"

sizeOfWindow = 1000
numOfTriplesOnStream = 0


# convert ms to secs
def ms_to_sec (row):
    secs = row['ms']/1000
    return secs

# Read Agg file
df0 = pd.read_csv('/Users/vitor/git-repository/DSCEP/scep-operator/'+folder_name2+'/'+aggFile,
                  delimiter = " ",
                  names=["Operator1", "WindowNum", "ms", "TripleIn", "TripleOut"])
NumOfLines = len(df0.index)
print("num of lines = "+str(NumOfLines))
numOfTriplesOnStream = NumOfLines * sizeOfWindow
print("numOfTriplesOnStream = "+str(numOfTriplesOnStream))

# Create a Pandas dataframe from some data.
df1 = pd.read_csv('/Users/vitor/git-repository/DSCEP/scep-operator/'+folder_name2+'/'+speedFile1,
                  delimiter = " ",
                  names=["Operator1", "WindowNum", "ms", "Temp", "NumOfTriples"])
del df1['Temp']
df1['Operator1'] = ''

df1['sec'] = df1.apply (lambda row: ms_to_sec(row), axis=1)

df2 = pd.read_csv('/Users/vitor/git-repository/DSCEP/scep-operator/'+folder_name2+'/'+speedFile2,
                  delimiter = " ",
                  names=["Operator2", "WindowNum", "ms", "Temp", "NumOfTriples"])
del df2['Temp']
df2['Operator2'] = ''

print('/Users/vitor/git-repository/DSCEP/scep-operator/'+folder_name2+'/'+speedFile2)
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('DSCEP_test_results.xlsx', engine='xlsxwriter')

# Write the data in column and transposed (row) directions.
df1.to_excel(writer, sheet_name='Sheet1',
             startrow=1, startcol=1, header=True, index=False)
startCol = len(df1.columns) + 2
print(startCol)
df2.to_excel(writer, sheet_name='Sheet1',
             startrow=1, startcol=startCol, header=True, index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.save()



