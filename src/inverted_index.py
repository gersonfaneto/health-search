# Autor: Gerson Ferreira dos Anjos Neto
# Componente Curricular: Algoritmos I
# Concluído em: 03/06/2022
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum trecho de código de colega ou
# de outro autor, tais como provindos de livros e apostilas, e páginas ou documentos eletrônicos da internet.
# Qualquer trecho de código de outra autoria que não a minha está destacado com uma citação do autor e a fonte do
# código e estou ciente que estes trechos não serão considerados para fins de avaliação.

from os import walk
from os.path import isfile, splitext, getsize, basename, dirname, join

from cli import helpMessage


# Formata o caminho dos arquivos. -> Evita duplicidade de chaves e garante...
# compatibilidade entre plataformas.
def normalizePath(workingPath):
    newPath = workingPath
    if "\\" in newPath:
        newPath = newPath.replace("\\", "/")
    if workingPath.endswith("/"):
        newPath = newPath.rstrip("/")
    if workingPath.endswith("\\"):
        newPath = newPath.rstrip("\\")
    return newPath


# Lê o arquivo de cache e remonta o dicionário contendo o Index.
def readCache(filePath, invertedIndex):
    filePath = normalizePath(filePath)
    if isfile(filePath):
        with open(filePath, "r") as cacheFile:
            for line in cacheFile.readlines():
                key, value = line.rstrip("\n").split("***")
                invertedIndex[key] = eval(value)
    return invertedIndex


# Atualiza o arquivo de cache com as informações do Index.
def writeCache(filePath, invertedIndex):
    filePath = normalizePath(filePath)
    with open(filePath, "w+") as cacheFile:
        for key, value in invertedIndex.items():
            newLine = f"{key}***{value}\n"
            cacheFile.write(newLine)


# Lê o arquivo contendo as StopWords e as armazena em uma lista.
def getStopWords(filePath, stopWords):
    filePath = normalizePath(filePath)
    with open(filePath, "r") as textFile:
        for line in textFile:
            line = line.replace(" ", "").rstrip("\n")
            stopWords.append(line)
    return stopWords


# Formata o contéudo de um arquivo de texto.
def normalizeString(anyString):
    # Divisão/Passagem das palavras para "lower-case".
    tempList = [word.lower() for word in anyString.split()]
    wordsIndex, wordsList = set(tempList), []
    for word in wordsIndex:
        # Remoção de caracteres especiais e números das palavras.
        normalizedWord = "".join(list(filter(lambda x: x.isalpha(), word)))
        wordsList.append((normalizedWord, tempList.count(word)))
    return wordsList


# Atualiza o Index (no caso da adição de um diretório) garantindo a confiabilidade...
# das informações.
def updateIndex(invertedIndex, addedFiles, addedDirs, dirPath):
    dirPath = normalizePath(dirPath)
    if invertedIndex:
        for keyWord in list(invertedIndex):
            for dirName in list(invertedIndex[keyWord]):
                # 1º Caso -> Diretório Excluido.
                if dirname(dirName) == dirPath and dirName not in addedDirs:
                    invertedIndex[keyWord].pop(dirName)
                if not invertedIndex[keyWord]:  # Eliminação de chaves vazias.
                    invertedIndex.pop(keyWord)
                if dirName in addedDirs:
                    # 2º Caso -> Arquivo(s) Excluido(s)!
                    for fileName in list(invertedIndex[keyWord][dirName]):
                        if fileName not in addedFiles:
                            invertedIndex[keyWord][dirName].pop(fileName)
                        # Eliminação de chaves vazias.
                        if not invertedIndex[keyWord][dirName]:
                            invertedIndex[keyWord].pop(dirName)
                        if not invertedIndex[keyWord]:
                            invertedIndex.pop(keyWord)
    return invertedIndex


# Adiciona um arquivo ao Index.
def addFile(filePath, stopWords, invertedIndex):
    filePath = normalizePath(filePath)
    fileName, dirName = basename(filePath), dirname(filePath)
    # Tratamento de exceção na abertura de arquivos.
    try:
        with open(filePath, "r") as textFile:
            # Formatação do contéudo do arquivo.
            fileIndex = normalizeString(textFile.read())
            for word, quantOcur in fileIndex:
                # Verifica se a palavra não é uma StopWord ou número.
                if word not in stopWords and word.isalpha():
                    # Criação/Atualização do Index -> Dicionário Aninhado de Três Etapas.
                    if word in invertedIndex:
                        # "setdefault" é utilizado para forçar a criação do dicionário.
                        if dirName in invertedIndex[word]:
                            invertedIndex[word][dirName][fileName] = quantOcur
                        else:
                            invertedIndex[word].setdefault(dirName, {})[fileName] = quantOcur
                    else:
                        invertedIndex.setdefault(word, {}).setdefault(dirName, {})[fileName] = quantOcur
        return invertedIndex, 1
    except Exception:
        return invertedIndex, 0


# Adiciona um diretório ao Index, utilizando a função "addFile".
def addDir(dirPath, stopWords, invertedIndex):
    # Armazena os nomes dos diretórios e arquivos, utilizados na atualização.
    addedFiles, addedDirs = set(), set()
    for root, dirs, files in walk(dirPath):
        if root != dirPath:
            addedDirs.add(root)
        for file in files:
            filePath = normalizePath(join(root, file))
            addedFiles.add(basename(filePath))
            hadSucess = addFile(filePath, stopWords, invertedIndex)
            # Caso a indexação falhe, o usuário é avisado.
            print(f"Error! Couldn´t open file at: {filePath}\n" if not hadSucess else "", end="")
    return invertedIndex, addedFiles, addedDirs


# Remove um arquivo do Index.
def removeFile(filePath, invertedIndex):
    filePath = normalizePath(filePath)
    fileName, dirName = basename(filePath), dirname(filePath)
    for keyWord in list(invertedIndex):
        if dirName in list(invertedIndex[keyWord]):
            if fileName in list(invertedIndex[keyWord][dirName]):
                invertedIndex[keyWord][dirName].pop(fileName)
            # Remoção de chaves vazias.
            if not invertedIndex[keyWord][dirName]:
                invertedIndex[keyWord].pop(dirName)
            if not invertedIndex[keyWord]:
                invertedIndex.pop(keyWord)
    return invertedIndex


# Remove um diretório do Index.
def removeDir(filePath, invertedIndex):
    dirName = normalizePath(filePath)
    for keyWord in list(invertedIndex):
        if dirName in list(invertedIndex[keyWord]):
            invertedIndex[keyWord].pop(dirName)
        # Remoção de chaves vazias.
        if not invertedIndex[keyWord]:
            invertedIndex.pop(keyWord)
    return invertedIndex


# Formata o tamanho e unidade do arquivo, utiliza base binária.
def getFileSize(filePath):
    filePath = normalizePath(filePath)
    # Validação Extra -> Caso o arquivo tenha sido apagado da memória, "getsize"...
    # levanta uma exceção e o usuário e avisado.
    try:
        baseSize, fileSize = 1024, getsize(filePath)
    except FileNotFoundError:
        return "Error -> File Not Found! Update Index!"

    if fileSize < baseSize:
        unitType = "B"
    elif fileSize < (baseSize ** 2):
        fileSize, unitType = fileSize / baseSize, "KB"
    elif fileSize < (baseSize ** 3):
        fileSize, unitType = fileSize / (baseSize ** 2), "MB"
    elif fileSize < (baseSize ** 4):
        fileSize, unitType = fileSize / (baseSize ** 3), "GB"
    elif fileSize < (baseSize ** 5):
        fileSize, unitType = fileSize / (baseSize ** 4), "TB"
    else:
        fileSize, unitType = fileSize / (baseSize ** 5), "PB"

    return f"{round(fileSize, 2)}{unitType}"


# Ordena os caminhos dos arquivos decrescentemente pela quantidade de ocorrências de um termo.
def selectionSort(toSort):
    n = len(toSort)
    for i in range(n - 1):
        pivot, pivotIndex = toSort[i][2], i
        for j in range(i, n):
            if toSort[j][2] > pivot:
                pivot, pivotIndex = toSort[j][2], j
        toSort[i], toSort[pivotIndex] = toSort[pivotIndex], toSort[i]
    return toSort


# Busca por um termo no Index, retorna a lista de arquivos ordenada.
def searchIndex(chosenWord, invertedIndex):
    foundPaths = []
    if chosenWord in invertedIndex:
        for dirName in invertedIndex[chosenWord]:
            for fileName, quantOcur in invertedIndex[chosenWord][dirName].items():
                foundPaths.append((dirName, fileName, quantOcur))
        sortedPaths = selectionSort(foundPaths)
        return len(sortedPaths), sortedPaths
    return -1, None


# Imprime o resultado da busca.
def printSearch(matchingPaths):
    for dirName, fileName, quantOcur in matchingPaths:
        filePath = join(dirName, fileName)
        (fileName, fileExt), fileSize = splitext(fileName), getFileSize(filePath)
        print(f"""
        Local:                  {dirName}
        Nome:                   {fileName}
        Extensão:               {fileExt}
        Tamanho:                {fileSize}
        Quant. de Ocorrências:  {quantOcur}
        """)


# Exibe o Index (termo por termo).
def showIndex(invertedIndex):
    for keyWord in invertedIndex:
        currentWordPaths = []
        print(f"Termo: \"{keyWord.capitalize()}\"")
        for dirName in invertedIndex[keyWord]:
            for fileName, quantOcur in invertedIndex[keyWord][dirName].items():
                currentWordPaths.append((dirName, fileName, quantOcur))
        for dirName, fileName, quantOcur in selectionSort(currentWordPaths):
            print(f"""
        Local:                  {dirName}
        Nome:                   {fileName}
        Quant. de Ocorrências:  {quantOcur}
            """)


if __name__ == "__main__":
    # Caso o usuário execute esse script, a mensagem de ajuda será exibidia.
    helpMessage()
