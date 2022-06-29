import tkinter as tk
import tkinter.filedialog as filedialog
import os
import time
import sys

from AEstrela import AEstrela, AEstrelaNo
from AEstrelaSokoban import AEstrelaSokoban, AEstrelaSokobanNo


_ROOT = os.path.abspath(os.path.dirname(__file__))

def labirintoIterator(arquivo):
    for numLinha, linha in enumerate(arquivo):
        for numCol, char in enumerate(linha):
            if char != '\n':
                yield char, numCol + 1j * numLinha

class AEstrelaMapaNo(AEstrelaNo):

    def __init__(self, direcao, coordenada):
        self.direcao   = direcao
        self.coordenada = coordenada
        AEstrelaNo.__init__(self)

    def __hash__(self):
        return hash((self.coordenada, self.direcao))

    def __eq__(self, outro):
        return self.__hash__() == outro.__hash__()

    def custoMovimento(self, objetivo):

        if self.coordenada + self.direcao == objetivo.coordenada:
            return 1
        else:
            return 2


class AEstrelaMapa(AEstrela): 

    def __init__(self, mapa):
        self.mapa = mapa

    def heuristica(self, no):
        diff = no.coordenada - self.fim.coordenada
        return abs(diff.real) + abs(diff.imag)

    def ehObjetivo(self, no, fim):
        return no.coordenada == fim.coordenada

    def sucessores(self, no):
        sucessores = []
        for direcao in (1, -1, 1j, -1j):
            coordenada   = no.coordenada + direcao
            if coordenada in self.map:
                sucessores.append(AEstrelaMapaNo(direcao, coordenada))
        return sucessores

class AboutDialog(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self = tk.Toplevel()
        self.title("About")

        info = tk.Label(self, text=("Inteligência Artificial Sokoban\nDesenvolvido por Leonardo Lima de Vasconcellos"))
        info.grid(row=0)

        self.ok_button = tk.Button(self, text="OK", command=self.destroy)
        self.ok_button.grid(row=1)

class StdoutRedirector(object):
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.configure(background="black")
        self.master.title("Inteligência Artificial")
        self.master.resizable(0,0)
        
        self.caixaImg = tk.PhotoImage(file='caixa.png')
        self.agenteImg = tk.PhotoImage(file='agente.png')
        self.alvoImg = tk.PhotoImage(file='alvo.png')
        self.paredeImg = tk.PhotoImage(file='parede.png')

        self.master.tk.call('wm', 'iconphoto', self.master._w, self.caixaImg)
        self.criarMenu()

        self.frame = tk.Frame(self, height=800, width=1024)
        self.frame.grid()

        tk.Button(self.frame, text="Abrir Labirinto", command=self.abrirArquivo).grid(row=0, column=0)
        tk.Button(self.frame, text="Executar", command=self.executar).grid(row=0, column=1)

        self.algoritimo = tk.IntVar(self.frame, 1)
        tk.Radiobutton(self.frame, text="Algoritmo A*", variable=self.algoritimo, value=1).grid(row=0, column=2)
        tk.Radiobutton(self.frame, text="Algoritmo Custo Uniforme", variable=self.algoritimo, value=2).grid(row=0, column=3)

        self.canvas = tk.Canvas(self.frame, width=800, height = 400)
        self.canvas.grid(row=1, column=0, columnspan=4)

        self.console = tk.Text(self.frame, height=20, width=110)
        self.console.grid(row=2, column=0, columnspan=4)
        sys.stdout = StdoutRedirector(self.console)
    
    def criarMenu(self):
        root = self.master
        menu = tk.Menu(root)
        root.config(menu=menu)

        menuArquivo = tk.Menu(menu)
        menu.add_cascade(label="Arquivo", menu=menuArquivo)
        menuArquivo.add_command(label="Abrir", command=self.abrirArquivo)
        menuArquivo.add_separator()
        menuArquivo.add_command(label="Sair", command=menu.quit)

        menuAjuda = tk.Menu(menu)
        menu.add_cascade(label="Ajuda", menu=menuAjuda)
        menuAjuda.add_command(label="Sobre", command=AboutDialog)

    def abrirArquivo(self):
        arquivo = filedialog.askopenfilenames(multiple=False, initialdir=os.path.join(_ROOT, 'labirintos'), title="Escolha um Labirinto", filetypes=(('Arquivo Texto','*.txt'),))[0]
        self.carregarLabirinto(arquivo)

    def carregarLabirinto(self, arquivo):
        self.labirinto = []
        self.mapa = set()
        self.objetivos = set()
        self.caixas = set()

        with open(arquivo, 'r') as arquivo:
            for char, coordenada in labirintoIterator(arquivo):
                self.labirinto.append((char, coordenada))
                if char in [' ', 'A', '+', 'C']:
                    self.mapa.add(coordenada)
                    if char == 'A':
                        self.agente = coordenada
                    elif char == '+':
                        self.objetivos.add(coordenada)
                    elif char == 'C':
                        self.caixas.add(coordenada)

        print("Labirinto Interpretado")
        
        self.inicio = AEstrelaSokobanNo(self.agente, self.caixas,   0, -1, 0)
        self.fim   = AEstrelaSokobanNo(self.agente, self.objetivos, 0, -1, 0)
        self.desenhaEstado(self.inicio.caixas, self.agente, self.labirinto)

    def executar(self):
        print('Pensando...')
        tempoInicial = time.time()
        mecanismo = AEstrelaSokoban(self.mapa, self.objetivos, self.agente)
        
        try:
            caminho = mecanismo.busca(self.inicio, self.fim, True, self.algoritimo.get())
            self.animaCaminho(caminho, self.mapa, self.agente, self.labirinto)
        except Exception as error:
            print("{0}".format(error))
        
        tempoFinal = time.time()
        print("*** Tempo de Execução => {} segundos" . format(tempoFinal - tempoInicial))
            
    def animaCaminho(self, caminho, mapa, agente, labirinto):

        mecanismo = AEstrelaMapa(mapa)
        inicio  = caminho[0]

        for estado in caminho[1:]:
            agenteFim = (inicio.caixas - estado.caixas).pop() 
            noInicial  = AEstrelaMapaNo(0, agente)
            noFinal    = AEstrelaMapaNo(0, agenteFim - estado.direcao)

            mecanismo.map  = mapa - inicio.caixas

            agenteCaminho = [passo.coordenada for passo in mecanismo.busca(noInicial, noFinal)]
            for coordenada in agenteCaminho:
                self.desenhaEstado(inicio.caixas, coordenada, labirinto)

            self.desenhaEstado(estado.caixas, agenteFim, labirinto)
            agente = agenteFim
            inicio   = estado

    def desenhaEstado(self, caixas, agente, labirinto):
        size = 30
        self.canvas.delete("all")
        for char, coordenada in labirinto:
            x, y = coordenada.real * size, coordenada.imag * size
            if coordenada in caixas:
                self.canvas.create_image(x, y, image=self.caixaImg, anchor=tk.NW)
            elif coordenada == agente:
                self.canvas.create_image(x, y, image=self.agenteImg, anchor=tk.NW)
            elif char == "+":
                self.canvas.create_image(x, y, image=self.alvoImg, anchor=tk.NW)
            elif char == "0":
                self.canvas.create_image(x, y, image=self.paredeImg, anchor=tk.NW)
        
        self.canvas.update()
        time.sleep(0.1)

if __name__ == '__main__':

    app = Application()
    app.mainloop()
