from AEstrela import AEstrela, AEstrelaNo

class AEstrelaSokobanNo(AEstrelaNo):

    def __init__(self, agente, caixas, direcao, novaCaixa, profundidade):
        self.direcao = direcao 
        self.novaCaixa = novaCaixa
        self.caixas = caixas
        self.agente = agente
        self.agenteOrigem = agente
        self.hash = hash((self.agente, tuple(self.caixas)))
        self.profundidade = profundidade
        AEstrelaNo.__init__(self)

    def __hash__(self):
        return self.hash

    def __eq__(self, outro):
        return self.__hash__() == outro.__hash__()

    def custoMovimento(self, objetivo):
        custo = 1
        if self.novaCaixa != objetivo.agenteOrigem:
            custo += 0.2
        if self.direcao != objetivo.direcao:
            custo += 0.1
        return custo

    def agenteMaisAEsquerda(self, mapa):
        """
        Encontra o canto mais a esquerta no topo para posicionar o agente
        e também encontra possíveis deslocamentos de caixas
        """
        naoVisitado = set([self.agente])
        visitado = set()
        mudancaPosicao = set()
        maisEsqAcima = self.agente
        direcoes = (1, 1j, -1, -1j)

        while naoVisitado:
            coordenada = naoVisitado.pop()
            visitado.add(coordenada)
            for direcao in direcoes:
                novaCoordenada = coordenada + direcao
                if novaCoordenada in mapa:

                    if novaCoordenada in self.caixas:
                        if novaCoordenada + direcao in mapa and novaCoordenada + direcao not in self.caixas:
                            mudancaPosicao.add((novaCoordenada, novaCoordenada + direcao))

                    elif self.ehMaisAEsquerda(novaCoordenada, maisEsqAcima):
                        maisEsqAcima = novaCoordenada
                        if not novaCoordenada in visitado:
                            naoVisitado.add(novaCoordenada)
                    elif novaCoordenada not in visitado:
                        naoVisitado.add(novaCoordenada)

        self.agente  = maisEsqAcima
        return mudancaPosicao


    def ehMaisAEsquerda(self, coordenada, maisEsqAcima):
        if coordenada.real < maisEsqAcima.real:
            return True
        elif coordenada.real == maisEsqAcima.real and coordenada.imag < maisEsqAcima.imag:
             return True
        return False



class AEstrelaSokoban(AEstrela): 

    def __init__(self, mapa, objetivos, agente):
        self.mapa = mapa
        self.objetivos = objetivos
        self.direcoes = (1, 1j, -1, -1j)

    def ehObjetivo(self, no, fim):
        """
        Testa se é o objetivo.
        """
        for caixa in fim.caixas:
            if caixa not in no.caixas:
                return False
        return True

    def heuristica(self, no):
        """
        Distancia estimada entre o nó e o a posição objetivo.
        """
        distancia = 0
        for caixa in no.caixas:
            listaDistancias = []
            for objetivo in self.objetivos:
                diff = caixa - objetivo
                listaDistancias.append(abs(diff.real) + abs(diff.imag))
            distancia += min(listaDistancias)
        return distancia


    def sucessores(self, no):
        """
        Retorna um iterable contendo possíveis movimentos para o nó dado.
        """
        sucessores = []
        mudancaPosicao = no.agenteMaisAEsquerda(self.mapa)
        # pos[0] = de
        # pos[1] = para
        for pos in mudancaPosicao:
            novasCaixas = set(no.caixas)
            novasCaixas.remove(pos[0])
            novaCaixa = pos[1]
            agente = pos[0]
            novasCaixas.add(novaCaixa)
            sucessores.append(AEstrelaSokobanNo(agente, novasCaixas, pos[1] - pos[0], novaCaixa, (no.profundidade + 1)))
        return sucessores
