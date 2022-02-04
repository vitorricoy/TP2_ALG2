import os
from datetime import datetime

class Backtrack:

    def __init__(self, valores, pesos, pesoMaximo, N):
        self.solucao = []
        self.valores = valores
        self.pesos = pesos
        self.pesoPego = 0
        self.valorPego = 0
        self.melhorSolucao = []
        self.melhorValor = 0
        self.pesoMaximo = pesoMaximo
        self.N = N

    def knapsack(self, at):
        if at == N:
            if self.pesoPego <= self.pesoMaximo:
                if self.valorPego > self.melhorValor:
                    self.melhorSolucao = self.solucao.copy()
                    self.melhorValor = self.valorPego
            return

        self.knapsack(at+1)
        self.solucao.append(at)
        self.valorPego += self.valores[at]
        self.pesoPego += self.pesos[at]
        self.knapsack(at+1)
        self.solucao.pop()
        self.valorPego -= self.valores[at]
        self.pesoPego -= self.pesos[at]

class BranchAndBound:
    def __init__(self, valores, pesos, pesoMaximo, N):
        itens = list(zip(valores, pesos))
        # Ordena os itens pela maior razão v[0]/v[1]
        itens.sort(key=lambda v: -v[0]/v[1])
        itens = list(zip(*itens))
        self.solucao = []
        self.valores = itens[0]
        self.pesos = itens[1]
        self.pesoPego = 0
        self.valorPego = 0
        self.melhorSolucao = []
        self.melhorValor = 0
        self.pesoMaximo = pesoMaximo
        self.N = N

    def knapsack(self, at):
        if at == N:
            if self.pesoPego <= self.pesoMaximo:
                if self.valorPego > self.melhorValor:
                    self.melhorSolucao = self.solucao.copy()
                    self.melhorValor = self.valorPego
            return

        melhorPossivel = self.valorPego + (self.pesoMaximo-self.pesoPego)*(self.valores[at]/self.pesos[at])

        if melhorPossivel > self.melhorValor:
            self.knapsack(at+1)
            self.solucao.append(at)
            self.valorPego += self.valores[at]
            self.pesoPego += self.pesos[at]
            self.knapsack(at+1)
            self.solucao.pop()
            self.valorPego -= self.valores[at]
            self.pesoPego -= self.pesos[at]
    
class Backtrack:

    def __init__(self, valores, pesos, pesoMaximo, N):
        self.solucao = []
        self.valores = valores
        self.pesos = pesos
        self.pesoPego = 0
        self.valorPego = 0
        self.melhorSolucao = []
        self.melhorValor = 0
        self.pesoMaximo = pesoMaximo
        self.N = N

    def knapsack(self, at):
        if at == N:
            if self.pesoPego <= self.pesoMaximo:
                if self.valorPego > self.melhorValor:
                    self.melhorSolucao = self.solucao.copy()
                    self.melhorValor = self.valorPego
            return

        self.knapsack(at+1)
        self.solucao.append(at)
        self.valorPego += self.valores[at]
        self.pesoPego += self.pesos[at]
        self.knapsack(at+1)
        self.solucao.pop()
        self.valorPego -= self.valores[at]
        self.pesoPego -= self.pesos[at]



backtrackOutput = open('backtrack.csv', "w")
branchboundOutput = open('branchbound.csv', "w")
for file in os.listdir('files'):
    N = -1
    pesoMaximo = -1
    valores = []
    pesos = []
    with open('files/'+file) as f:
        lines = f.readlines()
        for line in lines:
            v1, v2 = line.split(" ")
            v1 = float(v1)
            v2 = float(v2)
            if N == -1:
                N = v1
                pesoMaximo = v2
            else:
                valores.append(v1)
                pesos.append(v2)
    inicioBacktrack = datetime.now()
    backtrack = Backtrack(valores, pesos, pesoMaximo, N)
    backtrack.knapsack(0)
    fimBacktrack = datetime.now()
    inicioBranchBound = datetime.now()
    branchBound = BranchAndBound(valores, pesos, pesoMaximo, N)
    branchBound.knapsack(0)
    fimBranchBound = datetime.now()
    backtrackOutput.write(str(file)+";"+"Vitor Rodarte Ricoy"+";"+str((fimBacktrack-inicioBacktrack).total_seconds() * 1000)+";"+str(backtrack.melhorValor)+"\n")
    branchboundOutput.write(str(file)+";"+"Vitor Rodarte Ricoy"+";"+str((fimBranchBound-inicioBranchBound).total_seconds() * 1000)+";"+str(branchBound.melhorValor)+"\n")

backtrackOutput.close()
branchboundOutput.close()
