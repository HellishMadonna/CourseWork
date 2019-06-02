import sys
import random
from numpy.fft import fft
import math
import matplotlib.pyplot as plt

NUMBER_LEN = 32
NODES_COUNT = 200
GENERATIONS_COUNT = 500
COEF_MAX_NUMBER = 10
EPSILON = 0.001
a = []

class Node:
    """
    Класс особи
    """
    def __init__(self, k, generation, _id):
        """
        Создание особи, присвоение основных параметров
        mass - хранит коэффициенты фильтра в двоичном коде в коде Грея
        getBinaryMass - преобразует строку из кода Грея в бинарный код
        """
        if (k <= 0):#Python просто лучший язык
            #print("Node __init__ clear")
        
            self.mass = []
            self.n = 0
            self.numberLen = NUMBER_LEN
            self.rating = 0
            self.id = -1
            self.generation = -1
        else:
            #print("Node __init__")
            
            self.mass = []
            self.n = random.randint(1,k)
            self.numberLen = NUMBER_LEN
            self.rating = 0
            self.id = _id
            self.generation = generation

            for i in range(self.n):
                s0 = []
                for j in range(self.numberLen):
                    q = random.random()
                    if (q < 0.5):
                        s0.append(0)
                    else: s0.append(1)
                #print(s0)
                
                s1 = s0[0:self.numberLen - 1]#s1 - сдвиг s0 на 1 бит вправо
                s1.insert(0,0)
                s = []
                for j in range(self.numberLen):
                    s.append((s0[j] + s1[j]) % 2)

                #print(s0)
                #print(s1)
                #print(s)
                #print()
                #print()
                
                self.mass.append(s)
            #print(self.mass)

    def getCoef(self):
        #print("getCoef")
        q = []
        for i in self.mass:
            q.append(self.decToFloat(self.binToDec(self.getBinaryMass(i))))

        #print(q)
        return q

    def calcRating(self):
        """
        Данная функция производит перерасчет рейтинга особи
        и ее приспособленности
        """
        #print("calcRating")
        #self.rating = random.random()
        global a
        q = self.getCoef()
        #print(q)
        w = fft(q, 2*len(a))

        #print(w)
        e = []
        for i in range(len(a)):
            e.append(math.sqrt(w[i].real**2 + w[i].imag**2))
        
        #print(q)
        #print(w)
        #print(e)

        #print(e)
        #print(a)
        s = 0.0
        deltaX = 1 / len(a)
        for i in range(1, len(e)):
            deltaY1 = abs(a[i-1] - e[i-1])
            deltaY2 = abs(a[i] - e[i])
            deltaS = (deltaY1 + deltaY2) / 2.0 * deltaX
            s += deltaS
            #print(deltaS)

        #print()
        #print()
        self.rating = s

    def mutate(self):
        """
        Данная функция производит изменение некоторых
        параметров особи (мутация)
        """
        #print("mutate")
        k = random.randint(0, self.n)
        #print(k)
        for i in range(k):
            q = random.randint(0, len(self.mass) - 1)
            #self.decToFloat(self.binToDec(self.getBinaryMass(self.mass[q])))

            index = random.randint(0, len(self.mass[q]) - 1)
            self.mass[q][index] = 1 - self.mass[q][index]
            #self.decToFloat(self.binToDec(self.getBinaryMass(self.mass[q])))

        #print("mutate end")

    def getBinaryMass(self, st):
        #print("getBinaryMass")
        #print("in:", st)
        
        index = 0
        for i in range(self.numberLen):
            if (st[i] == 1):
                index = i
                break
        #print(index)
        
        n = []
        for i in range(self.numberLen):
            n.append(0)

        for i in range(self.numberLen - index):
            s1 = st[0:self.numberLen-i]
            for k in range(i):
                s1.insert(0,0)
                
            #print(s1)
            for j in range(self.numberLen):
                n[j] = (n[j] + s1[j]) % 2

        #print("out:", n)
        #print("getBinaryMass end")
        return n

    def binToDec(self, st):
        #print("binToDec")
        #print("in:", st)
        answer = 0
        step = 1
        if (st[0] == 1):#<0
            flag = True
        else: flag = False

        st.reverse()
        for i in range(len(st)-1):
            if (flag):
                answer += step * (1 - st[i])
            else: answer += step * st[i]
            #print(answer)
            step *= 2

        if (flag):
            answer += 1
            answer *= -1
        
        #print("out:", answer)
        #print ("binToDec end")
        return answer

    def decToFloat(self, numb):
        #print("decToFloat")
        #print("in:", numb)
        maxV = 1.0
        minV = -1.0
        answer = numb / (2**(self.numberLen - 1))#1 bit for sign

        #print("out:", answer)
        #print("decToFloat end")
        return answer

    def printMe(self, f = None):
        if (f == None):
            print(self.generation, "," , self.id, ";", self.rating)
            for i in self.mass:
                print(i)
            print()
        else:
            f.write(str(self.generation) + "; " + str(self.id) + " " + str(self.rating) + "\n")
            for i in self.mass:
                f.write("   ")
                f.write(str(self.decToFloat(self.binToDec(self.getBinaryMass(i)))))
                f.write("\n")

class NodeManager:
    def __init__(self, nodeCount, generations):
        """
        Данная функция создает первичную популяцию особей
        """
        #print("init")
        self.nodes = []
        self.nodeCount = nodeCount
        self.generations = generations
        self.currentGeneration = 0
        self.currentId = 0
        
        for i in range(self.nodeCount):
            self.nodes.append(Node(COEF_MAX_NUMBER, self.currentGeneration, self.currentId))
            self.nodes[len(self.nodes) - 1].calcRating()
            self.currentId += 1

    def selection(self):
        """
        Данная функция выбирает кто из текущих особей будет жить
        """
        #print("selection")
        self.sortNodes()
        #print("in:")
        #self.printMe()
        
        nodes = []
        nodes.append(self.nodes[0])#add the coolest node

        for i in range(1, len(self.nodes)):#kill the old ones
            if (self.nodes[i].generation == self.currentGeneration):
                nodes.append(self.nodes[i])

        if (len(nodes) > self.nodeCount):
            self.nodes = nodes[0:self.nodeCount]
        else: self.nodes = nodes;

        #print("out:")
        #self.printMe()
        #print("selection end")

    def crossover(self):
        """
        Данная функция создает новое поколение особей
        """
        #print("crossover")
        self.sortNodes()
        
        for i in range(1, len(self.nodes), 2):
            self.crossNodes(self.nodes[i-1], self.nodes[i])
        
        #print("crossover end")

    def mutate(self):
        #print("mutate")
        for i in range(1, len(self.nodes)):
              self.nodes[i].mutate()

        #print("mutate end")

    def crossNodes(self, m, p):
        #print("crossNodes")
        #print("in:")
        #m.printMe()
        #print("in:")
        #p.printMe()
        
        
        childA = Node(-1, -1, -1)
        childB = Node(-1, -1, -1)

        #поделим количество коэффициентов в каком-то соотношении между особями        
        maxCount = m.n + p.n
        border = random.randint(1, maxCount - 1)

        #Смешаем все гены
        oldGenes1 = []
        oldGenes1.extend(m.mass)
        oldGenes1.extend(p.mass)

        #print("oldGenes1:", oldGenes1)

        oldGenes2 = []
        oldGenes2.extend(oldGenes1)
        oldGenes2.reverse()

        #print("oldGenes2:", oldGenes2)
        
        genes = []
        for i in range(maxCount):
            k = random.randint(1, NUMBER_LEN - 1)
            gen = []
            for j in range(NUMBER_LEN):
                if (j < k):
                    gen.append(oldGenes1[i][j])
                else: gen.append(oldGenes2[i][j])

            #print(gen)
            genes.append(gen)

        #Распределим новые гены между детьми в заданном соотношении
        childA.n = border;
        for i in range(0, border):
            childA.mass.append(genes[i])

        childB.n = maxCount - border;
        for i in range(border, maxCount):
            childB.mass.append(genes[i]);

        childA.id = self.currentId
        self.currentId += 1
        childA.generation = self.currentGeneration

        childB.id = self.currentId
        self.currentId += 1
        childB.generation = self.currentGeneration

        #Добавим особей в популяцию
        self.nodes.append(childA)
        self.nodes.append(childB)
        #print("created:", childA.generation, childA.id)
        #childA.printMe()
        #print("created:", childB.generation, childB.id)
        #childB.printMe()
        #print("crossNodes end")
    
    def sortNodes(self):
        for i in self.nodes:
            i.calcRating()
        self.nodes.sort(key = lambda x: x.rating, reverse = False)

    def run(self):
        print("run")
        f = open("rawData.txt", "w")
        self.printMe(f)
        f.write("--------------------------------" + "\n" + "\n")

        for i in range(0, self.generations):
                self.currentGeneration += 1
                self.crossover()
                self.mutate()
                self.selection()
                self.printMe(f)
                f.write("--------------------------------" + "\n" + "\n")
                print(self.currentGeneration)
                if (self.nodes[0].rating <= EPSILON):
                    break

        f.close()

    def printLeader(self):
        global a
        leader = self.nodes[0]
        print(leader.generation, ',', leader.id, ';', leader.rating)
        for i in leader.mass:
            print(leader.decToFloat(leader.binToDec(leader.getBinaryMass(i))))
        
        x = []
        for i in range(len(a)):
            x.append(i * math.pi / len(a))

        plt.plot(x, a)
               
        q = leader.getCoef()
        w = fft(q, 2*len(a))

        e = []
        for i in range(len(a)):
            e.append(math.sqrt(w[i].real**2 + w[i].imag**2))

        plt.plot(x, e)
        plt.savefig('spirit.png', format = 'png')

    def printMe(self, f = None):
        for i in self.nodes:
            i.printMe(f)

def main(argv = None):
    if (argv is None):
        argv = sys.argv

    """
    Считывание входных данных из файла
    Создание популяции с заданными характеристиками
    Сбор результатов
    """

    #Считывание данных из файла
    f = open("input.txt", "r")

    global a
    q = f.readline().split(" ")

    for i in q:
        a.append(float(i))

    NODES_COUNT = int(f.readline())
    GENERATIONS_COUNT = int(f.readline())
    COEF_MAX_NUMBER = int(f.readline())
    EPSILON = float(f.readline())
    
    #Создание популяции
    nm = NodeManager(NODES_COUNT, GENERATIONS_COUNT)
    nm.run()

    #Вывод результатов
    nm.printLeader()

if __name__ == "__main__":
    sys.exit(main())
