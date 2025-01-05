# Autor: Gerson Ferreira dos Anjos Neto
# Componente Curricular: Algoritmos I
# Concluído em: 03/06/2022
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum trecho de código de colega ou
# de outro autor, tais como provindos de livros e apostilas, e páginas ou documentos eletrônicos da internet.
# Qualquer trecho de código de outra autoria que não a minha está destacado com uma citação do autor e a fonte do
# código e estou ciente que estes trechos não serão considerados para fins de avaliação.

from os.path import isfile, isdir

# Lista de argumentos válidos para a utilização do programa.
validArgs = ["-a", "--add", "-r", "--remove", "-s", "--searchIndex", "-S", "--showIndex"]


# Mensagem de ajuda, exibida para o usuário automaticamente ou utilizando "-h"/"--help".
def helpMessage():
    print("""Welcome to Health Search, your Inverted Index/Terminal based search engine!

        Usage: HealthSearch.py [OPTION] [FILE/DIR_PATH]
        or:    HealthSearch.py [OPTION] [TERM]

        Options:
        -h, --help            Shows this help message and exit.
        -a, --add             Add a file/dir to the Index.
        -r, --remove          Remove a file/dir from the Index.
        -s, --searchIndex     Seach for a specific word in the Index.
        -S, --showIndex       Show the entire Index.
    """)


# Exibi uma ajuda para utilização dos comandos, caso esses sejam utilizados incorretamente.
def getCommandHelp(chosenCommand, validCommands):
    helpHeader = "Invalid Syntax! Use Case.: \"HealthSearch.py "
    if chosenCommand not in validCommands or chosenCommand == "runSynError":
        return "Invalid Syntax! Use \"HealthSearch [--help or -h]\" to see program usage."
    else:
        if chosenCommand in validCommands[0:2]:
            return helpHeader + "[--add or -a] [FILE/DIR_PATH]\""
        elif chosenCommand in validCommands[2:4]:
            return helpHeader + "[--remove or -r] [FILE/DIR_PATH]\""
        elif chosenCommand in validCommands[4:6]:
            return helpHeader + "[--searchIndex or -s] [TERM]\""
        else:
            return helpHeader + "[--showIndex or -S]\""


# Validação dos Parâmetros.
def validateInput(rawInput):
    rawInput.pop(0)  # Remove o nome do script "HealthSearch.py" armazenado por padrão pela biblioteca.
    # 1º Caso - Chamada de "-S"/"--searchIndex" com outro complemento.
    if len(rawInput) == 1 and rawInput[0] not in ["-S", "--showIndex"]:
        return False, getCommandHelp(*rawInput, validArgs)
    # 2º Caso - Chamada dos outros parâmetros sem a utilização dos devidos complementos.
    elif len(rawInput) != 2 and rawInput[0] not in ["-S", "--showIndex"]:
        return False, getCommandHelp("runSynError", validArgs)
    # 3º Caso - Chamada sem um parâmetro válido.
    elif not rawInput[0].startswith("-"):
        return False, getCommandHelp("runSynError", validArgs)
    return True, rawInput


# Validação dos Complementos.
def processInput(termArgs):
    optionArg, *compArg = termArgs

    # 1/2º Caso - Adicionar ou Remover -> Exije um caminho de arquivo/diretório válido!
    if optionArg == "-a" or optionArg == "--add":
        if isfile(*compArg) or isdir(*compArg):
            return True, "addDirFile", *compArg
        else:
            return False, "addDirFile", getCommandHelp("-a", validArgs)
    elif optionArg == "-r" or optionArg == "--remove":
        if isfile(*compArg) or isdir(*compArg):
            return True, "removeDirFile", *compArg
        else:
            return False, "removeDirFile", getCommandHelp("-r", validArgs)

    # 3º Caso - Busca no Index -> Exije um único termo para ser buscado.
    elif optionArg == "-s" or optionArg == "--searchIndex":
        if len(termArgs) == 2:
            return True, "searchIndex", *compArg
        else:
            return False, "searchIndex", getCommandHelp("-s", validArgs)

    # 4º Caso - Exibição do Index -> Não aceita qualquer complemento.
    elif optionArg == "-S" or optionArg == "--showIndex":
        if len(termArgs) == 1:
            return True, "showIndex", None
        else:
            return False, "showIndex", getCommandHelp("-S", validArgs)

    # 5º Caso - Erro de Sintaxe -> Solicita ao usuário utilizar a mensagem de ajuda.
    else:
        return False, "invalidOption", getCommandHelp("runSynError", validArgs)


if __name__ == "__main__":
    # Caso o usuário execute esse script, a mensagem de ajuda será exibidia.
    helpMessage()
