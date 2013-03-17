from NFA import NFA

class ER:
    def __init__(self, operadores = {}):
        self.alfabeto = set()
        self.corpo = []
        self.operacao = None
        self.op_num_args = operadores
        self.operadores = operadores.keys()
        self.processaSimbolo = lambda x : x.lower()
            
    def criarER(self,lista):
        pilha = []
        pilha.append(lista[0])
        proximaPosicao = 1
        ultimoOperador = 0
        while len(pilha) != 0:
            topo = len(pilha) - 1
            if pilha[topo] in self.operadores:
                ultimoOperador = len(pilha)
            else:
                nfa = NFA(processaSimbolo = self.criarProcessaSimbolo)
                nfa = nfa.criarNFABasico(pilha[topo])
                pilha.append(nfa)
                operador = pilha[ultimoOperador]
                distancia = topo - ultimoOperador
                if distancia == self.op_num_args[operador]:
                    args = []
                    while args < distancia:
                        args.append(pilha.pop())
                    self.criarERBasica(operador, args)
            
            pilha.append(lista[proximaPosicao])
            proximaPosicao += 1
            
            
    def uniao(self, sentenca):
        resultado = []
        resultado.append(self.corpo[0].executa(sentenca))
        if resultado:
            resultado.append(self.corpo[1].executa(sentenca))
        return resultado
    
    def estrela(self, sentenca):
        resultado = []
        temp = []
        pedaco = ""
        sentencas = []
        while  temp != None:
            temp = self.corpo[0].executa(sentenca)
            
            if temp:
                resultado.append(temp)
                   
        
    def concatenacao(self, sentenca):
        resultado =[]
        temp = 
        temp = corpo[0].executa(sentenca)
    
    def dividirSentenca(self, sentenca, tamanho, variasVezes = False):
        divisoes  = []
        
        
    def executa(self, sentenca):
        
            
        
        