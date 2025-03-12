import random
import math
import struct

class AlgoritmoGenetico:
    def __init__(self, tamanho_populacao, prob_mutacao, prob_cross):

        self.prob_mutacao = prob_mutacao
        self.prob_cross = prob_cross

        self.L = 4 * 8 # size of chromossome in bits

        self.populacao = []


        #Gerar População Originária
        for i in range(tamanho_populacao):
            self.populacao.append('1' if random.random() > 0.5 else '0')



    def funcao_fitnees(self, y):
        if ((y < 0) or (y >= math.pi)):
            return 0
        else:
            return y + abs(32*math.sin(y))


    def mutação(self, cromossomo):
        novo_cromossomo = cromossomo
        numero_aleatorio = random.random()
        if (numero_aleatorio > self.prob_mutacao):
            #TODO: fazer a mutação
            novo_cromossomo = cromossomo

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
        assert(len(bits) == self.L)
        for i, bit in enumerate(bits):
            bit = int(bit)  # 0 or 1
            x += bit * (2**i)
        return self.bitsToFloat(x)
######################################################

for i in range(32):
    print(AlgoritmoGenetico(0,0,0).get_bits(2.56)[i])

