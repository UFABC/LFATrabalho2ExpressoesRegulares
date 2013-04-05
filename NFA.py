import re
"""
Bruno Cesar RA: 11078407
Juliano Gomes RA: 1118509
"""
class NFA:
    def __init__(self, processaSimbolo = None):
        self.estados = []
        self.tamanho = 0
        self.alfabeto = set([])
        self.transicao = {}
        self.estadoInicial = None
        self.estadosFinais = []
        if processaSimbolo:
            self.processaSimbolo = processaSimbolo
        else:
            self.processaSimbolo = lambda x: x
        self.simboloMap = {}
        self.epsilon = "epsilon"
        self.simbolosESeusEstados = [] # Uma dupla sertaneja para la de legal, que ajudara todos a mapearmos a resposta

    def criarNFABasico(self, sentenca):
        self.tamanho = len(sentenca)
        for i,letra in enumerate(sentenca):
            self.transicao['q' + str(i)] = {letra:'q' + str(i)}
        del self.transicao[len(sentenca) - 1]                                 
    
    def adiciona_estado(self, nome, transicao, st_inic=0, st_final=0):
        self.estados.append(nome)
        self.transicao[nome] = transicao

        simbolos = set(transicao.keys())
        self.alfabeto.union(simbolos)

        if st_inic:
            self.estadoInicial = nome
        if st_final:
            self.estadosFinais.append(nome)

    def executa(self, sentenca):
        if not self.estadoInicial:
                raise("Initialization Error", "deve existir um estado inicial")
        if not self.estadosFinais:
                raise("Initialization Error", "deve existir pelo menos um estado final")
        estadosAtuais = []
        self.simbolosESeusEstados = []
        
        estadosAtuais.append(self.estadoInicial)
#        for simbolo in self.splitNFA(sentenca):
        for simbolo in sentenca:
            simboloProcessado = self.processaSimbolo(simbolo)
            proximosEstados = []
            for proximoEstado in estadosAtuais:
                try:
                    for cadaTransicao in self.transicao[proximoEstado][simboloProcessado]:
                        proximosEstados.append(cadaTransicao)
                except KeyError:
                    pass
            proximosEstados += self.epsilonAlcancavel(estadosAtuais)
            
            estadosAtuais = []
            for proximoEstado in proximosEstados:
                if proximoEstado not in estadosAtuais:
                    estadosAtuais.append(proximoEstado)
            
            self.simbolosESeusEstados += [(simbolo, estadosAtuais)]
                    # adiciona nas variaveis os caracteres de importancia

        self.responde(estadosAtuais, sentenca)

   
    def responde(self, estadosAtuais, sentenca):
        auxResposta = ""
        print estadosAtuais
        for estadoAtual in estadosAtuais:
            if estadoAtual in self.estadosFinais:
                auxResposta += estadoAtual        
        if auxResposta:
            print("A sentenca '" + sentenca + "' foi reconhecida pelo automato com estado final " + auxResposta + ".")
        else:
            print("A sentenca '" + sentenca + "' nao foi reconhecida pelo automato.")

                            
    def epsilonAlcancavel(self, estadosAtuais):
        aux = []
        if estadosAtuais != []:
            for estadoAtual in estadosAtuais:
                try:
                    for cadaTransicao in self.transicao[estadoAtual][self.epsilon]:
                        if cadaTransicao not in aux:
                            aux.append(cadaTransicao)
                except KeyError:
                    pass
            return aux
    
    def splitNFA(self, sentenca):
        match = re.split(r"([0-9]+)([a-z]+)", sentenca, re.I)
        
        listas = [i.split() for i in match]
        novaLista = []
        for i in listas:
            print i
            novaLista += i
        return novaLista
    
    def executaArquivo(self, diretorio):
        arquivo = open(diretorio)
        texto = arquivo.readlines()
        for linhas in texto:
            self.executa(linhas)
        arquivo.close()

    def inMap(self, simbolo):
        for key, values in self.simboloMap.items():
            for value in values:
                if simbolo.lower() == value:
                    return key
        return "PALAVRA"

    def processaMapaDeSimbolos(self, texto):
        linhas = texto.split("\n")
        for linha in linhas:
            if linha != "":
                chaveLista = linha.split("=")
                lista = chaveLista[1].split(";")
                for i, elemento in enumerate(lista):
                    lista[i] = ' '.join(elemento.split())
                self.simboloMap[' '.join(chaveLista[0].split())] = lista


    @classmethod
    def arquivoNFA(cls, diretorio):
        arquivo = open(diretorio)
        texto = arquivo.read()
        nfa = cls()
        
        processaSimboloOpcional = nfa.encontrarEntreChaves("processaSimbolo", texto)
        
        if processaSimboloOpcional != -1:
            nfa.processaMapaDeSimbolos(processaSimboloOpcional)
            nfa.processaSimbolo = nfa.inMap
        
        textoTransicao = nfa.encontrarEntreChaves("criarTransicao", texto)
        transicao = nfa.criarTransicao(textoTransicao)
        textoAdicionaEstado = nfa.encontrarEntreChaves("adicionaEstado", texto)
        nfa.adicionaEstado(textoAdicionaEstado,transicao)
        
        return nfa;

    def adicionaEstado(self, texto, transicao):
        linhas = texto.split("\n")
        for linha in linhas:            
            if linha != "":
                inicio = False
                final = False
                linha = "".join(linha.split())
                estado = linha.split(":")
                if len(estado) > 1:                    
                    condicoes = estado[1].split(",")                    
                    for condicao in condicoes:
                        condicao = condicao.split('=')
                        if condicao[0] == 'st_inic':
                            inicio = (condicao[1] == 'True')
                        if condicao[0] == 'st_final':
                            final = (condicao[1] == 'True')
                self.adiciona_estado(estado[0], transicao[estado[0]], st_inic = inicio, st_final = final)
        
    def criarTransicao(self, texto):
        transicao = {}
        linhas = texto.split("\n")
        for linha in linhas:
            if ''.join(linha.split()) != "":
                linha = "".join(linha.split())
                chaveValor = linha.split('=')
                chave = chaveValor[0]
                subMapaDeChaves = chaveValor[1].split(';')                
                primeiraEntrada = subMapaDeChaves[0].split(':')                
                subChave = primeiraEntrada[0]
                valor = primeiraEntrada[1].split(',')
                transicao[chave] = {subChave:valor}
                for subMapa in subMapaDeChaves[1:]:
                    subMapa = subMapa.split(':')
                    subChave = subMapa[0]                    
                    valor = subMapa[1].split(',')
                    transicao[chave].update({subChave:valor})
        return transicao
                

    def encontrarEntreChaves(self, palavraChave, texto):
        palavraTotal = palavraChave + " {"
        indicePalavra = texto.find(palavraTotal)
#        Verifica se tem espaco
        if indicePalavra < 0:
            palavraTotal = palavraChave + "{"
            indicePalavra = texto.find(palavraTotal)
            if indicePalavra < 0:
                return -1

        indice = texto.find(palavraTotal) + len(palavraTotal)

        return texto[indice:texto.find("}", indice)]
