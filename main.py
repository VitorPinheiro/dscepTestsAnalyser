import pandas as pd
import xlsxwriter
import subprocess
import utils as utils
import matplotlib.pyplot as plt

# Falta colocar generico para qualquer quantidade de operadores.
# Ja ta imprimindo no Excel
# Falta Plotar os graficos também, talvez podemos plotar dos DFs... mas se for mto complicado, plota no excel mesmo.
# Falta deixar escrito no excel o total de demora do processamento tb (soma de todas as janelas de um operador)

# Entradas do script
number_of_operators = 8
query_num = 14
numOfTweets = 4800
TestNum = 2

sizeOfWindow = 5000

# Variaveis calculadas
folder_name = "Query{numQuery}-intra-{numOp}-{numTweets}-Test{numTest}-auto".format(numQuery=query_num,
                                                                              numOp=number_of_operators,
                                                                              numTweets=numOfTweets,
                                                                               numTest = TestNum);

# Run script to generate folder with test files.
subprocess.check_call(['/Users/vitor/git-repository/DSCEP/scep-operator/createFolderForTest.sh', "/Users/vitor/git-repository/DSCEP/scep-operator/", folder_name])
#folder_name2 = "Query11-intra-2-1430-Test1-final"; # JUST FOR DEBUG

# Passo 1 do loop: Para cada teste (Gerar nomes do Speed e Agg files)
speedFiles = utils.generateSpeedFilesNames(query_num, number_of_operators)

#speedFile1 = "SOpbasicOp1_node_1_query_11Speed.txt"
#speedFile2 = "SOpbasicOp2_node_1_query_11Speed.txt"
aggFile = utils.generateAggFileName(query_num) #"Agg_node_1_query_{numQuery}Speed.txt".format(numQuery=query_num)



# Passo 2 do loop: Read Agg file to calculate numOfTriples processesed
df0 = pd.read_csv('/Users/vitor/git-repository/DSCEP/scep-operator/'+folder_name+'/'+aggFile,
                  delimiter = " ",
                  names=["Operator1", "WindowNum", "ms", "TripleIn", "TripleOut"])
NumOfLines = len(df0.index)
print("num of lines = "+str(NumOfLines))
numOfTriplesOnStream = NumOfLines * sizeOfWindow
print("numOfTriplesOnStream = "+str(numOfTriplesOnStream))


# Passo 3 do loop (loop separado): Create a Pandas dataframe for each speed file (each operator).

dfs = []
num = 1

for elem in speedFiles:
    df1 = pd.read_csv('/Users/vitor/git-repository/DSCEP/scep-operator/'+folder_name+'/'+elem,
                  delimiter = " ",
                  names=["Operator"+str(num), "WindowNum", "ms", "Temp", "NumOfTriples"])
    del df1['Temp']
    df1['Operator1'] = ''

    if len(df1.index) > 1:
        value = df1.iloc[1]['ms']
        df1._set_value(0, 'ms', value)
    else:
        df1._set_value(0, 'ms', 0)

    df1['sec'] = df1.apply(lambda row: utils.ms_to_sec(row), axis=1)
    num = num + 1

    mean_df = df1['sec'].mean()
    df1['mean-secs'] = mean_df

    df1['WindowNum'] = df1['WindowNum'].str.replace(':', '')
    #df1.plot('WindowNum', y=['sec'])
    #plt.show()

    dfs.append(df1)
''''
df2 = pd.read_csv('/Users/vitor/git-repository/DSCEP/scep-operator/'+folder_name2+'/'+speedFile2,
                  delimiter = " ",
                  names=["Operator2", "WindowNum", "ms", "Temp", "NumOfTriples"])
del df2['Temp']
df2['Operator2'] = ''

print('/Users/vitor/git-repository/DSCEP/scep-operator/'+folder_name2+'/'+speedFile2)
'''

# Passo 4 do loop: Create a Pandas Excel writer using XlsxWriter as the engine to write each operator.
writer = pd.ExcelWriter('/Users/vitor/git-repository/DSCEP/scep-operator/'+folder_name+'/DSCEP_test_NumOp'+str(number_of_operators)+'_results.xlsx', engine='xlsxwriter')


startCol = 1
for df in dfs:
    df.to_excel(writer, sheet_name='Sheet1',
             startrow=1, startcol=startCol, header=True, index=False)
    startCol = startCol + len(df.columns) + 2

''''
df1.to_excel(writer, sheet_name='Sheet1',
             startrow=1, startcol=1, header=True, index=False)
startCol = len(df1.columns) + 2

df2.to_excel(writer, sheet_name='Sheet1',
             startrow=1, startcol=startCol, header=True, index=False)
'''
# Close the Pandas Excel writer and output the Excel file.
writer.save()





