import os
import time

class Backtrack:
    # Inicializa os valores necessários para o backtracking e executa a recursao
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
        self._knapsack(0)

    # Funcao recursiva que executa o backtracking
    def _knapsack(self, at):
        # Se todos itens ja foram pegos
        if at == N:
            # Verifica se a solucao atual é valida
            if self.pesoPego <= self.pesoMaximo:
                # Verifica se a solucao atual é a melhor
                if self.valorPego > self.melhorValor:
                    # Se for a melhor solucao, ela é salva
                    self.melhorSolucao = self.solucao.copy()
                    self.melhorValor = self.valorPego
            return
        # Executa a recursao sem pegar o item atual
        self._knapsack(at+1)
        # Adiciona o item atual na solucao
        self.solucao.append(at)
        self.valorPego += self.valores[at]
        self.pesoPego += self.pesos[at]
        # Executa a recursao pegando o item atual
        self._knapsack(at+1)
        # Remove o item atual da solucao
        self.solucao.pop()
        self.valorPego -= self.valores[at]
        self.pesoPego -= self.pesos[at]

class BranchAndBound:
    # Inicializa os valores necessários para o branch and bound e executa a recursao
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
        self._knapsack(0)

    # Funcao recursiva que executa o branch and bound
    def _knapsack(self, at):
        # Se todos itens ja foram pegos
        if at == N:
            # Verifica se a solucao atual é valida
            if self.pesoPego <= self.pesoMaximo:
                # Verifica se a solucao atual é a melhor
                if self.valorPego > self.melhorValor:
                    # Se for a melhor solucao, ela é salva
                    self.melhorSolucao = self.solucao.copy()
                    self.melhorValor = self.valorPego
            return

        # Calcula o upper bound da solução atual
        melhorPossivel = self.valorPego + (self.pesoMaximo-self.pesoPego)*(self.valores[at]/self.pesos[at])

        # Se a solucao atual possui um upper bound melhor que o valor da melhor solucao ate o momento, continua construindo ela
        if melhorPossivel > self.melhorValor:
            # Executa a recursao sem pegar o item atual
            self._knapsack(at+1)
            # Adiciona o item atual na solucao
            self.solucao.append(at)
            self.valorPego += self.valores[at]
            self.pesoPego += self.pesos[at]
            # Executa a recursao pegando o item atual
            self._knapsack(at+1)
            # Remove o item atual da solucao
            self.solucao.pop()
            self.valorPego -= self.valores[at]
            self.pesoPego -= self.pesos[at]


# Abre o arquivo csv
saida = open('resultado.csv', "w")
# Escreve o cabecalho
saida.write("Arquivo;Nome do Aluno;Tempo Gasto(ms);Solucao Encontrada;Algoritmo\n")
# Lista os arquivos de teste
for file in os.listdir('files'):
    # Inicializa os valores que serao lidos do arquivo
    N = -1
    pesoMaximo = -1
    valores = []
    pesos = []
    # Abre o arquivo de teste
    with open('files/'+file) as f:
        # Le as linhas do arquivo
        lines = f.readlines()
        for line in lines:
            # Le os dois valores da linha
            v1, v2 = line.split(" ")
            # Converte os valores para float
            v1 = float(v1)
            v2 = float(v2)
            # Se for a primeira linha, salva o numero de itens e capacidade da mochila
            if N == -1:
                N = v1
                pesoMaximo = v2
            else: # Se nao salva o valor e o peso do item
                valores.append(v1)
                pesos.append(v2)
    # Executa o algoritmo de backtracking
    inicioBacktrack = time.time()
    backtrack = Backtrack(valores, pesos, pesoMaximo, N)
    fimBacktrack = time.time()
    # Executa o algoritmo de Branch and Bound
    inicioBranchBound = time.time()
    branchBound = BranchAndBound(valores, pesos, pesoMaximo, N)
    fimBranchBound = time.time()
    # Escreve no csv os resultados encontrados pelos dois algoritmos
    saida.write(str(file)+";"+"Vitor Rodarte Ricoy"+";"+str((fimBacktrack-inicioBacktrack)*1000)+";"+str(backtrack.melhorValor)+";Backtrack\n")
    saida.write(str(file)+";"+"Vitor Rodarte Ricoy"+";"+str((fimBranchBound-inicioBranchBound)*1000)+";"+str(branchBound.melhorValor)+";Branch and Bound\n")
# Fecha o csv de saida
saida.close()
