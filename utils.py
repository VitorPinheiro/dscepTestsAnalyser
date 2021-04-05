import subprocess

"""
Função que gera os nomes dos arquivos Speed. Para os testes do DSCEP
"""
def generateSpeedFilesNames(query_num, numOperators):
    speedFiles = []

    for i in range(numOperators):
        speedFiles.append("SOpbasicOp{opNum}_node_1_query_{numQuery}Speed.txt".format(numQuery=query_num, opNum=i+1) )

    return speedFiles


"""
Função que gera os nomes dos arquivos Speed. Para os testes do DSCEP
"""
def generateAggFileName(query_num):
    aggFile = "Agg_node_1_query_{numQuery}Speed.txt".format(numQuery=query_num)

    return aggFile

"""
Convert ms to secs
"""
def ms_to_sec (row):
    secs = row['ms']/1000
    return secs


# Run script to generate folder with test files.
#subprocess.call(['sh', '/Users/vitor/git-repository/DSCEP/scep-operator/createFolderForTest.sh ', folder_name])
#subprocess.check_call(['/Users/vitor/git-repository/DSCEP/scep-operator/createFolderForTest.sh', folder_name])