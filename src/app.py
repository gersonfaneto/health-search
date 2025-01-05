# Autor: Gerson Ferreira dos Anjos Neto
# Componente Curricular: Algoritmos I
# Concluído em: 03/06/2022
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum trecho de código de colega ou
# de outro autor, tais como provindos de livros e apostilas, e páginas ou documentos eletrônicos da internet.
# Qualquer trecho de código de outra autoria que não a minha está destacado com uma citação do autor e a fonte do
# código e estou ciente que estes trechos não serão considerados para fins de avaliação.

from os.path import isfile
from sys import argv

from cli import helpMessage, validateInput, processInput
from inverted_index import readCache, writeCache, getStopWords, addFile, addDir, removeFile, removeDir, updateIndex, \
    searchIndex, printSearch, showIndex

# Os arquivos com as StopWords e o Índice Invertido são lidos automaticamente no ínicio de qualquer execução.
stopWordsFile, cacheFilePath = "src\\db\\stop_words.ignore", "src\\db\\inverted_index.ignore"
stopWords, invertedIndex = getStopWords(stopWordsFile, []), readCache(cacheFilePath, {})

# Caso o usuaŕio utilize "-h"/"--help" ou chame o script sem argumentos a mensagem de ajuda será exibida.
if "-h" in argv or "--help" in argv or len(argv) == 1:
    helpMessage()
else:
    rawArgs = argv
    hadSucess, resultOutput = validateInput(rawArgs)
    # Caso a validação dos parâmetros não passe, a mensagem de ajuda do comando é exibida.
    if not hadSucess:
        print(resultOutput)
    else:
        # Caso a validação dos complementos não passe, a mensagem de ajuda do comando é exibida.
        hadSucess, commandType, processedOutput = processInput(resultOutput)
        if not hadSucess:
            print(processedOutput)
        else:
            # Adição ao Index -> Arquivo/Diretório.
            if commandType == "addDirFile":
                if isfile(processedOutput):
                    invertedIndex, hadSucess = addFile(processedOutput, stopWords, invertedIndex)
                    print(f"Error! Couldn´t open file at: {processedOutput}\n" if not hadSucess else "", end="")
                else:
                    invertedIndex, addedFiles, addedDirs = addDir(processedOutput, stopWords, invertedIndex)
                    invertedIndex = updateIndex(invertedIndex, addedFiles, addedDirs, processedOutput)
            # Remoção do Index -> Arquivo/Diretório.
            elif commandType == "removeDirFile":
                if isfile(processedOutput):
                    invertedIndex = removeFile(processedOutput, invertedIndex)
                else:
                    invertedIndex = removeDir(processedOutput, invertedIndex)
            # Pesquisa no Index -> Retorna (ou não) uma lista contendo os arquivos correspondentes.
            elif commandType == "searchIndex":
                quantMatchs, foundPaths = searchIndex(processedOutput.lower(), invertedIndex)
                # Busca não encontrou correspondências.
                if quantMatchs == -1:
                    print(f"Não foram encontradas ocorrências do termo \"{processedOutput.capitalize()}\" no índice!")
                else:
                    # Busca encontrou uma ou mais correspondências.
                    print((
                              "Foi encontrada 1 ocorrência " if quantMatchs == 1 else f"Foram encontradas {quantMatchs} ocorrências ") + f"do termo \"{processedOutput.capitalize()}\" no índice!")
                    printSearch(foundPaths)
            else:
                # Exibição do Index -> Imprimi o Index (termo por termo).
                showIndex(invertedIndex)

# Ao fim da execução o cache e escrito automaticamente, garantindo a atualização dos dados.
writeCache(cacheFilePath, invertedIndex)
