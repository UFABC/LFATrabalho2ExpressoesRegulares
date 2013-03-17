class ER:
    def __init__(self, processaSimbolo = None, operadores = {}):
        self.alfabeto = set()
        self.corpo = []
        self.operacao = None
        self.op_num_args = operadores
        self.operadores = operadores.keys()
        if processaSimbolo:
            self.processaSimbolo = processaSimbolo
        else:
            self.processaSimbolo = lambda x : x
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
                nfa = self.criarNFABasico(pilha[topo])
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
        resultado.append(self.corpo[0](sentenca))
        if resultado:
            resultado.append(self.corpo[1](sentenca))
        return resultado
    
    def estrela(self, sentenca):
        resultado = []
        reconhece = True
        while reconhece:
            temp = self.corpo[0](sentenca)       
        
    def concatenacao(self, sentenca):
        resultado =[]
        temp = corpo[0]()
         
        
    def executa(self, sentenca):
        
            
        
        