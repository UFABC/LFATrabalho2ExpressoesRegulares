# coding=UTF-8
"""
Bruno Cesar RA: 11078407
Juliano Gomes RA: 1118509
"""

from NFA import NFA
import os

def is_number(s):
    try:
        float(s.replace(',', '.'))
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

    elif simbolo == ' ':
        return 'ESP'

    elif simbolo == ',':
        return 'VIR'

    elif simbolo.isalpha() or simbolo in ['(', ')']:
        return 'LET'
    elif simbolo == '1/2':
        return 'NUM'
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

def trataRespostaReceita(nfa, arquivo):
    quantidade = ""
    ingrediente = ""
    medida = ""
    for simboloEstado in nfa.simbolosESeusEstados:
        temporario = simboloEstado[0]
        for estado in simboloEstado[1]:
            if estado in ['q1', 'q6', 'q7']:
                quantidade += temporario
                break
            elif estado == 'q9' and ingrediente.rstrip()[len(ingrediente.rstrip())-2:] == 'de':   
                medida = ingrediente[:len(ingrediente)-3]
                ingrediente = ''
            elif estado == 'q14':
                ingrediente += temporario
            elif estado in ['q9']:
                ingrediente += temporario
                break
    print ('Quantidade:' + quantidade+ ' Medida:' + medida + ' Ingrediente:' + ingrediente)
    arquivo.write('Quantidade:' + quantidade+ ' Medida:' + medida + ' Ingrediente:' + ingrediente)
        
if __name__ == "__main__":
    nfa = NFA.arquivoNFA("nfa.txt")
    nfa.processaSimbolo = processaSimboloReceita
    
    receitas = leituraReceitas()
#    nfa.executa("100gr manteiga".strip())
#    trataRespostaReceita(nfa)
    arquivo = open('../saida.txt','w')
    for receita in receitas:
        for linha in receita:
            nfa.executa(linha.strip())
            arquivo.write(linha.strip() +"\n")
            trataRespostaReceita(nfa, arquivo)
            arquivo.write("\n")
    arquivo.close()
#    arquivo = open('saida.csv','w')
#    arquivo.write('qtde;medida;ingrediente\n')
#    for i in resultado:
#        arquivo.write(i[0] + ';' + i[1] + ';' + i[2] + '\n')
