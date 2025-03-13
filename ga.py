import random
import math
import struct

import pandas as pd
import matplotlib.pyplot as plt

class AlgoritmoGenetico:
    def __init__(self, tamanho_populacao, prob_mutacao, prob_cross, tipo_selecao, tolerancia_media_fitness):
        #Tipo seleção: 'roleta', 'classificacao', 'torneio'

        self.prob_mutacao = prob_mutacao
        self.prob_cross = prob_cross

        self.tamanho_populacao = tamanho_populacao
        self.quantidade_selecao = tamanho_populacao #Ele gera dois novos individuos a partir de um casal de pais
        self.tipo_selecao = tipo_selecao

        self.tamanho_cromossomo = 4 * 8 # size of chromossome in bits

        self.populacao = pd.DataFrame(['Cromossomo', 'Fitness'])

        media_fitness = []
        historico_populacao = []
        
        #Gerar População Originária
        for i in range(self.tamanho_populacao):
            bits = ''
            for i2 in range(self.tamanho_cromossomo):
                bits += '1' if random.random() > 0.5 else '0'
            fitness = self.funcao_fitness(self.get_float(bits))
            self.populacao = pd.concat([self.populacao, 
                                        pd.DataFrame({'Cromossomo': bits,
                                                      'Fitness': fitness})], ignore_index=True)
              
        historico_populacao.append(self.populacao)
        media_fitness.append(self.populacao['Fitness'].mean())

        while True:
            
            #Seleciona os indivíduos que gerarão a nova população
            lista_pais = self.selecao()

            #Nova era
            self.populacao = pd.DataFrame(['Cromossomo', 'Fitness'])

            for ind in range(len(lista_pais)/2):
                filhos = self.crossover([int(random.uniform(0,1)*self.tamanho_cromossomo)],
                            lista_pais[ind*2], lista_pais[ind*2+1])
                
                filho_1 = self.mutacao(filhos[0])
                filho_2 = self.mutacao(filhos[1])
                
                self.populacao = pd.concat([self.populacao, 
                                            pd.DataFrame({'Cromossomo': filho_1,
                                                        'Fitness': self.funcao_fitness(self.get_float(filho_1))})], ignore_index=True)
                self.populacao = pd.concat([self.populacao, 
                                            pd.DataFrame({'Cromossomo': filho_2,
                                                        'Fitness': self.funcao_fitness(self.get_float(filho_2))})], ignore_index=True)
            
            media_fitness_atual = self.populacao['Fitness'].mean()
            media_fitness.append(media_fitness_atual)
            historico_populacao.append(self.populacao)
            if (media_fitness_atual - (sum(media_fitness)/len(media_fitness)) < tolerancia_media_fitness):
                break

        plt.plot(x, y)
        plt.title('Média do Fitness de cada população')
        plt.xlabel('População')
        plt.ylabel('Valor do Fitness')
        plt.show()

            

    def funcao_fitnees(self, y):
        if ((y < 0) or (y >= math.pi)):
            return 0
        else:
            return y + abs(32*math.sin(y))
        
    def selecao(self):
        escolhidos_procriar = []

        if (self.tipo_selecao == 'roleta'):
            for i in range(self.quantidade_selecao):
                escolhidos_procriar.append(self.populacao[(random.random()*self.tamanho_populacao)-1]['Cromossomo'])

        elif (self.tipo_selecao == 'classificacao'):
            populacao_classificada = self.populacao.sort_values(by='Fitness', ascending=False).head(self.quantidade_selecao)
            escolhidos_procriar = populacao_classificada['Cromossomo'].tolist()

        elif (self.tipo_selecao == 'torneio'):
            for i in range(self.quantidade_selecao):
                pessoa_1 = self.populacao[(random.random()*self.tamanho_populacao)-1]
                pessoa_2 = self.populacao[(random.random()*self.tamanho_populacao)-1]

                p = pessoa_1['Fitness'] / (pessoa_1['Fitness'] + pessoa_2['Fitness'])

                if (random.random() > p):
                    escolhidos_procriar.append(pessoa_1['Cromossomo'])
                else:
                    escolhidos_procriar.append(pessoa_2['Cromossomo'])

        else:
            print(f'ERRO: Problema no tipo de seleção escolhido -> {self.tipo_selecao}')

        return escolhidos_procriar

    def crossover(self, pontos_corte, cromossomo_pai, cromossomo_mae):
        #pontos_corte precisa ser uma lista
        #função testada
        filho_1 = ''
        filho_2 = ''
        ultimo_corte = 0
        if (random.random() < self.prob_cross):
            for i, corte in enumerate(pontos_corte):
                if (corte < self.tamanho_cromossomo):
                    if (corte >= 0):
                        if (i % 2 != 0):
                            filho_1 += cromossomo_mae[ultimo_corte:corte]
                            filho_2 += cromossomo_pai[ultimo_corte:corte]
                        else:
                            filho_1 += cromossomo_pai[ultimo_corte:corte]
                            filho_2 += cromossomo_mae[ultimo_corte:corte]
                    
                    if(i == len(pontos_corte)-1):
                        if (i % 2 != 0):
                            filho_1 += cromossomo_pai[corte:]
                            filho_2 += cromossomo_mae[corte:]
                        else:
                            filho_1 += cromossomo_mae[corte:]
                            filho_2 += cromossomo_pai[corte:]

                    ultimo_corte = corte
                else:
                    print(f'ERRO: Valor da posição de corte no Crossover é maior que o cromossomo -> Pontos de corte: {pontos_corte}')
        
            else:
                filho_1 = cromossomo_mae
                filho_2 = cromossomo_pai
        return [filho_1, filho_2]   
            


    def mutacao(self, cromossomo):
        novo_cromossomo = ''
        numero_aleatorio = random.random()
        if (numero_aleatorio > self.prob_mutacao):
            for i, bit in enumerate(cromossomo):
                novo_cromossomo += '1' if bit == '0' else '0'
        return novo_cromossomo


    def gerarPopulacao1(self, anos):
        self.idade += anos
        return f"{self.nome} agora tem {self.idade} anos."
    
###########################################################
######      Conversões numericas (Prof. Eric)
###########################################################
    def floatToBits(self, f):
        s = struct.pack('>f', f)
        return struct.unpack('>L', s)[0]

    def bitsToFloat(self, b):
        s = struct.pack('>L', b)
        return struct.unpack('>f', s)[0]

    # Exemplo:  1.23 -> '00010111100'
    def get_bits(self, x):
        x = self.floatToBits(x)
        N = 4 * 8
        bits = ''
        for bit in range(N):
            b = x & (2**bit)
            bits += '1' if b > 0 else '0'
        return bits

    # Exemplo:  '00010111100' ->  1.23
    def get_float(self, bits):
        x = 0
        assert(len(bits) == self.tamanho_cromossomo)
        for i, bit in enumerate(bits):
            bit = int(bit)  # 0 or 1
            x += bit * (2**i)
        return self.bitsToFloat(x)
######################################################

AlgoritmoGenetico(100, 0.01, 0.7, 'torneio', 0.05)

