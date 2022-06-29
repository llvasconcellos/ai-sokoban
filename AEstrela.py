class AEstrela(object):

    def insort(self, a, x, key=lambda x:x):
        """
        Insere 'x' na lista 'a' e mantém ordenada inversamente presumindo 
        que 'a' é de ordem inversa. 
        Se 'a' já contem 'x', insere ao lado direito do 'x' mais a direita.
        """
        lo = 0
        hi = len(a)
        self.treeNodesCt = hi

        val = key(x)
        while lo < hi:
            mid = (lo+hi)//2
            if val > key(a[mid]): hi = mid
            else: lo = mid+1
        a.insert(lo, x)

    def heuristica(self, no):
        """
        Distancia estimada entre o nó e o a posição objetivo.
        """
        raise NotImplementedError

    def sucessores(self, no):
        """
        Retorna um iterable contendo possíveis movimentos para o nó dado.
        """
        raise NotImplementedError

    def ehObjetivo(self, no, fim):
        """
        Testa se é o objetivo.
        """
        raise NotImplementedError

    def busca(self, inicio, fim, log=False, algoritimo=1):
        """
        Executa a busca A*. Se o caminho não é encontrado uma exceção é levantada,
        caso contrário o caminho é retornado.
        """
        self.fim = fim
        inicio.h = self.heuristica(inicio)
        inicio.f = inicio.h
        conjuntoFechado = set()
        conjuntoAberto = set([inicio])
        listaAberta = [inicio]

        self.treeNodesCt = 0
        totalNodesGenerated = 0
        frontierDiscardedNodesCt = 0
        exploredDicardedNodesCt = 0

        if log:
            print("Inicialização da Árvore de Busca...\n")
            if algoritimo == 1:
                print("---- Algoritimo => A*\n")
            else:
                print("---- Algoritimo => Custo Uniforme\n")

        while conjuntoAberto:
            totalNodesGenerated += 1
            no = listaAberta.pop()

            if self.ehObjetivo(no, fim):
                if log:
                    print("\n*****\n***** SOLUÇÃO ENCONTRADA\n*****\n")
                    print("!!! Custo:        {}" . format(no.g))
                    print("!!! Profundidade: {}\n" . format(no.profundidade))
                    print("\n{0:<30}{1}" . format("Nós na árvore: ", self.treeNodesCt))
                    print("{0:<30}{1}" . format("Descartados já na fronteira: ", frontierDiscardedNodesCt))
                    print("{0:<30}{1}" . format("Descartados já explorados: ", exploredDicardedNodesCt))
                    print("{0:<30}{1}\n" . format("Total de nós gerados: ", totalNodesGenerated))

                return self.reconstruirCaminho(inicio, no, conjuntoFechado)

            conjuntoAberto.remove(no)
            conjuntoFechado.add(no)

            for noSucessor in self.sucessores(no):
                totalNodesGenerated += 1
                if noSucessor in conjuntoFechado: 
                    frontierDiscardedNodesCt += 1
                    continue

                novoCustoAcumulado = no.g + no.custoMovimento(noSucessor)

                if noSucessor in conjuntoAberto:
                    if novoCustoAcumulado < noSucessor.g: 
                        exploredDicardedNodesCt += 1
                        continue
                else:
                    noSucessor.g = novoCustoAcumulado
                    noSucessor.h = self.heuristica(noSucessor)
                    if algoritimo == 1:
                        noSucessor.f = noSucessor.g + noSucessor.h
                    else:
                        noSucessor.f = noSucessor.g
                    noSucessor.pai = no
                    conjuntoAberto.add(noSucessor)
                    self.insort(listaAberta, noSucessor, key=lambda no: no.f)

        raise Exception("Nenhum caminho encontrado")
                

    def reconstruirCaminho(self, inicio, fim, conjuntoFechado):
        """
        Executa o back-tracking e recontroi o caminho.
        """
        no = fim
        caminho = [fim]

        while no != inicio and no != None:
            no = no.pai
            caminho.append(no)

        caminho.reverse()
        return caminho



class AEstrelaNo(object):

    def __init__(self):
        #Custo Acumulado
        self.g = 0
        # Valor Heurística
        self.h = 0
        # Custo Total
        self.f = 0
        self.pai = None

    def custoMovimento(self, objetivo):
        raise NotImplementedError

    def __hash__(self):
        raise NotImplementedError

    def __eq__(self, outro):
        raise NotImplementedError