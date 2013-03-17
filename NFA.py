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
        resposta = []
        estadosAtuais.append(self.estadoInicial)
        for simbolo in sentenca[0:self.tamanho]:
                simbolo = self.processaSimbolo(simbolo)
                aux = []
                for estadoAtual in estadosAtuais:
                    for cadaTransicao in self.transicao[estadoAtual].get(simbolo):
                        if cadaTransicao != None:
                            aux.append(cadaTransicao)
                estadosAtuais = self.epsilonAlcancavel(aux)
                if estadosAtuais != []:
                    resposta.append(simbolo)                
        self.responde(estadosAtuais, resposta, sentenca)
        
    def responde(self, estadosAtuais, resposta, sentenca):
        reconheceu = False
        for estado in estadosAtuais:
            if estado in self.estadosFinais:
                reconheceu = True
        if reconheceu:
            return resposta
        else:
            return None
                            
    def epsilonAlcancavel(self,estadosAtuais):
        epsilonAlcancavel = estadosAtuais
        for estado in epsilonAlcancavel:
            temp = self.transicao.get(estado,{}).get(self.epsilon,[])
            if temp != [] and temp not in epsilonAlcancavel:
                epsilonAlcancavel.append(temp)
        return epsilonAlcancavel