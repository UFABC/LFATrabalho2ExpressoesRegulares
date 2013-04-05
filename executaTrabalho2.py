# coding=UTF-8
"""
Bruno Cesar RA: 11078407
Juliano Gomes RA: 1118509
"""

from NFA import NFA
import os

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def processaSimboloReceita(simbolo):
    """
    Metodo utilizado para processar o que foi obtido a partir
    do arquivo do NFA.
    """
    acentos = {'ç':'c', 'é':'e', 'á':'a', 'ã':'a', 'í':'i', 'ó':'o', 'ô':'o', 'ê':'e', 'â':'a', 'ú':'u'}

    simbolo=simbolo.lower()

    if simbolo in acentos.keys():
        simbolo = acentos[simbolo]

    if is_number(simbolo):
        return 'NUM'

    elif isinstance(simbolo, str):
        return 'LET'

    elif simbolo == ' ':
        return 'ESP'

    elif simbolo == ',':
        return 'VIR'

    elif simbolo == '/':
        return 'NEWLINE'
    else:
        return 'ERROR'


def leituraReceitas():
    resultado = []

    os.chdir("./receitas")
    for nomeArquivo in os.listdir("."):
        if nomeArquivo.endswith(".txt"):
            arquivo = open(nomeArquivo)
            resultado.append(arquivo.readlines())
            arquivo.close()

    return resultado

def trataRespostaReceita(nfa):
    for simboloEstado in nfa.simbolosSeusEstados:
        print simboloEstado
        
if __name__ == "__main__":
    nfa = NFA.arquivoNFA("nfa.txt")
    nfa.processaSimbolo = processaSimboloReceita
    
    receitas = leituraReceitas()
    for receita in receitas:
        for linha in receita:
            nfa.executa(linha)
#    arquivo = open('saida.csv','w')
#    arquivo.write('qtde;medida;ingrediente\n')
#    for i in resultado:
#        arquivo.write(i[0] + ';' + i[1] + ';' + i[2] + '\n')
