import sys
import random
from numpy.fft import fft
import math
import matplotlib.pyplot as plt
import configparser
import os

NUMBER_LEN = 32
NODES_COUNT = 200
GENERATIONS_COUNT = 500
COEF_MAX_NUMBER = 10
EPSILON = 0.001
ACH_LEN = 1024
a = []

class Node:
    def __init__(self, k, k1, generation, _id):
        if (k <= 0):#Python просто лучший язык
            self.massB = []
            self.massA = []
            self.n = 0
            self.m = 0
            self.numberLen = NUMBER_LEN
            self.rating = 0
            self.id = -1
            self.generation = -1
            self.cool = True;
        else:
            self.massB = []
            self.massA = []
            self.n = random.randint(1,k)
            self.m = random.randint(1,k1)
            self.numberLen = NUMBER_LEN
            self.rating = 0
            self.id = _id
            self.generation = generation
            self.cool = True;

            for i in range(self.n):
                s0 = []
                for j in range(self.numberLen):
                    q = random.random()
                    if (q < 0.5):
                        s0.append(0)
                    else: s0.append(1)
                
                s1 = s0[0:self.numberLen - 1]#s1 - сдвиг s0 на 1 бит вправо
                s1.insert(0,0)
                s = []
                for j in range(self.numberLen):
                    s.append((s0[j] + s1[j]) % 2)
        
                self.massB.append(s)
         
            for i in range(self.m):
                s0 = []
                for j in range(self.numberLen):
                    q = random.random()
                    if (q < 0.5):
                        s0.append(0)
                    else: s0.append(1)
                
                s1 = s0[0:self.numberLen - 1]#s1 - сдвиг s0 на 1 бит вправо
                s1.insert(0,0)
                s = []
                for j in range(self.numberLen):
                    s.append((s0[j] + s1[j]) % 2)
        
                self.massA.append(s)
        
    def getCoefA(self):
        q = []
        for i in self.massA:
            q.append(self.decToFloat(self.binToDec(self.getBinaryMass(i))))

        return q

    def getCoefB(self):
        q = []
        for i in self.massB:
            q.append(self.decToFloat(self.binToDec(self.getBinaryMass(i))))

        return q

    def calcRating(self):
        global a# [ [type, size, width, midle] ...]
        coefA = self.getCoefA()
        coefB = self.getCoefB()

        w = []
        wB = fft(coefB, 2*ACH_LEN)
        wA = fft(coefA, 2*ACH_LEN)
        for i in range(len(wA)):
            w.append(wB[i] / wA[i])

        e = []
        for i in range(ACH_LEN):
            e.append(math.sqrt(w[i].real**2 + w[i].imag**2))
        
        s = 0.0
        stage = 0
        offset = 0
        for curX in range(ACH_LEN):
            if (int(a[stage][0]) == 0):
                kq = abs(e[curX] - a[stage][3]) - a[stage][2] / 2
                try:
                    kw = abs(curX - a[stage + 1][3]) - a[stage + 1][2] / 2
                except:
                    kw = 1000*1000*1000
                    
                k = min(kq, kw)
                s += max(k, 0.0)

                if (curX + 1 == offset + int(a[stage][1])):
                    offset += int(a[stage][1])
                    stage += 1
            elif (int(a[stage][0]) == 1):
                kq = abs(curX - int(a[stage][3])) - a[stage][2] / 2
                try:
                    kw = abs(e[curX] - a[stage + 1][3]) - a[stage + 1][2] / 2
                except:
                    kw = 1000*1000*1000

                k = min(kq, kw)
                s += max(k, 0.0)

                if(curX +1 == offset + int(a[stage][2] / 2)):
                    offset += int(a[stage][2] / 2)
                    stage += 1
        
        self.rating = s

    def mutate(self):
        k = random.randint(0, self.n + self.m)
        for i in range(k):
            f = random.randint(0, 1)
            if (f == 0):#forA
                q = random.randint(0, len(self.massA) - 1)
                index = random.randint(0, len(self.massA[q]) - 1)
                self.massA[q][index] = 1 - self.massA[q][index]
            else:
                q = random.randint(0, len(self.massB) - 1)
                index = random.randint(0, len(self.massB[q]) - 1)
                self.massB[q][index] = 1 - self.massB[q][index]

    def getBinaryMass(self, st):
        index = 0
        for i in range(self.numberLen):
            if (st[i] == 1):
                index = i
                break
        
        n = []
        for i in range(self.numberLen):
            n.append(0)

        for i in range(self.numberLen - index):
            s1 = st[0:self.numberLen-i]
            for k in range(i):
                s1.insert(0,0)
                
            for j in range(self.numberLen):
                n[j] = (n[j] + s1[j]) % 2

        return n

    def binToDec(self, st):
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
            step *= 2

        if (flag):
            answer += 1
            answer *= -1
        
        return answer

    def decToFloat(self, numb):
        maxV = 1.0
        minV = -1.0
        answer = numb / (2**(self.numberLen - 1))#1 bit for sign

        return answer

    def getValue(self, coefB, coefA, first, mass):
        s = 0.0
        up = 0.0
        down = 1.0
        #if (first == True):
        #    for i in range(0, coefsA):
                

        return s

    def calcStability(self):
        #coefs = self.getCoef()
        #m = []

        #x = []
        #for i in range(ACH_LEN):
        #    x.append(i / ACH_LEN)

        #epsilon = 0.000001
        #count = 0
        flag = True
        """
        for i in range(1, ACH_LEN):
            k = self.getValue(coefs)
            m.append(k)
            if (abs(k) <= epsilon):
                count += 1
                if (count >= 4):
                    flag = True
            else: count = 0
        """
        #plt.plot(x, m)
        #plt.savefig('signal.png', format = 'png')
        #plt.clf()
        
        return flag

    def printMe(self, f = None):
        if (f == None):
            print(self.generation, "," , self.id, ";", self.rating)
            for i in self.massB:
                print(i)
            print()
            for i in self.massA:
                print(i)
            print()
        else:
            f.write(str(self.generation) + "; " + str(self.id) + " " + str(self.rating) + "\n")
            for i in self.massB:
                f.write("   ")
                f.write(str(self.decToFloat(self.binToDec(self.getBinaryMass(i)))))
                f.write("\n")
            for i in self.massA:
                f.write("   ")
                f.write(str(self.decToFloat(self.binToDec(self.getBinaryMass(i)))))
                f.write("\n")

class NodeManager:
    def __init__(self, nodeCount, generations):
        self.nodes = []
        self.nodeCount = nodeCount
        self.generations = generations
        self.currentGeneration = 0
        self.currentId = 0
        
        for i in range(self.nodeCount):
            self.nodes.append(Node(COEF_MAX_NUMBER, COEF_MAX_NUMBER, self.currentGeneration, self.currentId))
            self.nodes[len(self.nodes) - 1].calcRating()
            self.currentId += 1

    def selection(self):
        self.sortNodes()
        
        nodes = []
        nodes.append(self.nodes[0])#add the coolest node

        for i in range(1, len(self.nodes)):#kill the old ones
            if (self.nodes[i].generation == self.currentGeneration):
                nodes.append(self.nodes[i])

        if (len(nodes) > self.nodeCount):
            self.nodes = nodes[0:self.nodeCount]
        else: self.nodes = nodes;

    def crossover(self):
        self.sortNodes()

        allSum = 0
        for i in self.nodes:
            allSum += i.rating

        rate = []
        rate.append(self.nodes[len(self.nodes) - 1].rating / allSum)#0
        for i in range(1, len(self.nodes)):
            rate.append(rate[i-1] + self.nodes[len(self.nodes) - i - 1].rating / allSum)

        for k in range(int(len(self.nodes) / 2)):
            f = random.random()
            for i in range(len(rate)):
                if (f >= rate[i]):
                    f = int(i)
                    break
            s = random.random()
            for i in range(len(rate)):
                if (s >= rate[i]):
                    s = int(i)
                    break
        
            self.crossNodes(self.nodes[int(f)], self.nodes[int(s)])
        
    def mutate(self):
        self.sortNodes()
        
        for i in range(int(0.05*len(self.nodes)), len(self.nodes)):
              self.nodes[i].mutate()

    def crossNodes(self, m, p):        
        childA = Node(-1, -1, -1, -1)
        childB = Node(-1, -1, -1, -1)

        #поделим количество коэффициентов A в каком-то соотношении между особями        
        maxCount = m.m + p.m
        borderA = random.randint(1, maxCount - 1)

        #Смешаем все гены A
        oldGenes1A = []
        oldGenes1A.extend(m.massA)
        oldGenes1A.extend(p.massA)

        oldGenes2A = []
        oldGenes2A.extend(oldGenes1A)
        oldGenes2A.reverse()

        genesA = []
        for i in range(maxCount):
            k = random.randint(1, NUMBER_LEN - 1)
            gen = []
            for j in range(NUMBER_LEN):
                if (j < k):
                    gen.append(oldGenes1A[i][j])
                else: gen.append(oldGenes2A[i][j])

            genesA.append(gen)

        #Распределим новые гены A между детьми в заданном соотношении
        childA.m = borderA;
        for i in range(0, borderA):
            childA.massA.append(genesA[i])

        childB.m = maxCount - borderA;
        for i in range(borderA, maxCount):
            childB.massA.append(genesA[i]);

        #print("A", maxCount)
        #поделим количество коэффициентов B в каком-то соотношении между особями        
        maxCount = m.n + p.n
        borderB = random.randint(1, maxCount - 1)

        #Смешаем все гены B
        oldGenes1B = []
        oldGenes1B.extend(m.massB)
        oldGenes1B.extend(p.massB)

        oldGenes2B = []
        oldGenes2B.extend(oldGenes1B)
        oldGenes2B.reverse()
  
        genesB = []
        for i in range(maxCount):
            k = random.randint(1, NUMBER_LEN - 1)
            gen = []
            for j in range(NUMBER_LEN):
                if (j < k):
                    gen.append(oldGenes1B[i][j])
                else: gen.append(oldGenes2B[i][j])

            genesB.append(gen)

        #Распределим новые гены B между детьми в заданном соотношении
        childA.n = borderB;
        for i in range(0, borderB):
            childA.massB.append(genesB[i])

        childB.n = maxCount - borderB;
        for i in range(borderB, maxCount):
            childB.massB.append(genesB[i]);

        #print("B", maxCount)

        childA.id = self.currentId
        self.currentId += 1
        childA.generation = self.currentGeneration

        childB.id = self.currentId
        self.currentId += 1
        childB.generation = self.currentGeneration

        #Добавим особей в популяцию
        self.nodes.append(childA)
        self.nodes.append(childB)
        
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
        for i in leader.massB:
            print(leader.decToFloat(leader.binToDec(leader.getBinaryMass(i))))

        print()
        for i in leader.massA:
            print(leader.decToFloat(leader.binToDec(leader.getBinaryMass(i))))

        leader.calcStability()

        x = []
        y = []

        offset = 0
        for i in range(len(a)):
            if (int(a[i][0]) == 0):
                x1 = []
                y1 = []
                x2 = []
                y2 = []
                try:
                    for j in range(int(a[i][1] - a[i+2][1])):
                        x1.append(offset + len(x1))
                        y1.append(a[i][3] - a[i][2] / 2)
                        x2.append(offset + len(x2))
                        y2.append(a[i][3] + a[i][2] / 2)
                except:
                    for j in range(int(a[i][1])):
                        x1.append(offset + len(x1))
                        y1.append(a[i][3] - a[i][2] / 2)
                        x2.append(offset + len(x2))
                        y2.append(a[i][3] + a[i][2] / 2)
                x.append(list(x1))
                y.append(list(y1))
                x.append(list(x2))
                y.append(list(y2))
                offset += a[i][1]
            

        """    
        for i in range(ACH_LEN):
            x.append(i / ACH_LEN)
            if (int(a[stage][0]) == 0):
                y.append(a[stage][3])
                if (i + 1 == offset + int(a[stage][1])):
                    offset += int(a[stage][1])
                    stage += 1
            elif (int(a[stage][0]) == 1):
                y.append(int((offset + a[stage][2] * ACH_LEN / 2) / ACH_LEN))
                if(i + 1 == offset + int(a[stage][2] * ACH_LEN / 2)):
                    offset += int(a[stage][2] / 2)
                    stage += 1
        """
        for i in range(len(x)):
            plt.plot(x[i], y[i])
               
        coefA = leader.getCoefA()
        coefB = leader.getCoefB()
        w = []
        wB = fft(coefB, 2*ACH_LEN)
        wA = fft(coefA, 2*ACH_LEN)
        for i in range(len(wA)):
            w.append(wB[i] / wA[i])

        x = []
        e = []
        for i in range(ACH_LEN):
            x.append(i)
            e.append(math.sqrt(w[i].real**2 + w[i].imag**2))
    
        plt.plot(x, e, label = "АЧХ фильтра")

        plt.xlabel("Normalized Frequency (Pi rad / sample)")
        plt.ylabel("Magnitude (normalized to 1)")
        plt.title("Результаты работы алгоритма")
        plt.legend()
        plt.savefig('result.png', format = 'png')

    def printMe(self, f = None):
        for i in self.nodes:
            i.printMe(f)

def getSetting(config, section, setting):
    value = config.get(section, setting)
    return value

def setSetting(config, section, setting, value):
    config.set(section, setting, str(value))

def printSetting(config, section):
    first = 1
    
    for i in config.items(section):
        if (first == 1):
            first = 0
            continue
        print(i)

def getStr(_list):
    st = ""
    for i in range(len(_list) - 1):
        st += str(_list[i]) + "; "

    st += str(_list[len(_list)-1])
    return st

def getAFC(n, mass, flag):
    index = 0
    m = []

    for i in range(1, len(mass)):
        lx = mass[i-1][0]
        rx = mass[i][0]

        stepY = (mass[i][1] - mass[i-1][1]) / (rx-lx+1)
        curY = mass[i-1][1]
        for curX in range(lx, rx):
            m.append(curY)
            curY += stepY

    return getStr(m)
    
def menu():
    config = configparser.ConfigParser()
    config.read("input.ini")

    while (True):
        os.system("cls")

        printSetting(config, "Settings")
        
        print("1 - Старт")
        print("2 - Задать количетсво особей")
        print("3 - Задать количество поколений")
        print("4 - Задать максимальное количество коэффициентов")
        print("5 - Задать минимальное соответствие")
        print("6 - Задать АЧХ")
        print("7 - Выход")

        a = int(input())
        if (a == 1):
            break
        elif (a == 2):
            print("Введите новое количество особей n (n > 0, кратно 2)")
            try:
                count = int(input())
                if (count <= 0 or count % 2 != 0):
                    print("Неправильный формат ввода")
            except:
                print("Неправильный формат ввода")
                continue

            setSetting(config, "Settings", "speciesCount", count)
            print("Успешно изменено")
        elif (a == 3):
            print("Введите новое количество поколений m (m > 0)")
            try:
                count = int(input())
                if (count <= 0):
                    print("Неправильный формат ввода")
            except:
                print("Неправильный формат ввода")
                continue
            
            setSetting(config, "Settings", "iterationsCount", count)
            print("Успешно изменено")
        elif (a == 4):
            print("Введите новое максимальное количество коэффициентов k (m > 1)")
            try:
                count = int(input())
                if (count <= 1):
                    print("Неправильный формат ввода")
            except:
                print("Неправильный формат ввода")
                continue
            
            setSetting(config, "Settings", "maxCoefCount", count)
            print("Успешно изменено")
        elif (a == 5):
            print("Введите новое минимальное соответствие epsilon (epsilon > 0.0)")
            try:
                count = float(input())
                if (count <= 0.0):
                    print("Неправильный формат ввода")
            except:
                print("Неправильный формат ввода")
                continue
            
            setSetting(config, "Settings", "epsilon", count)
            print("Успешно изменено")
        elif (a == 6):
            #try:
                print("Введите количество частот, количество отрезков")
                n = int(input())
                count = int(input())
                mass = []
                for i in range(count + 1):
                    print("Введите контрольные точки в формате Частота:Амплитуда")
                    q = input().split(" ")
                    print(q)
                    q[0] = int(q[0])
                    q[1] = float(q[1])
                    mass.append(list(q))

                print("Добавить биение?(y/n)")
                c = input()

                st = getAFC(n, mass, c == "y")
                print(st)
                setSetting(config, "Settings", "amplitude-frequency", st)
            #except:
            #    print("Неправильный формат ввода")
                
        elif (a == 7):
            exit(0);

    config.write(open("input.ini", "w"))
    
def main(argv = None):
    if (argv is None):
        argv = sys.argv

    """
    Считывание входных данных из файла
    Создание популяции с заданными характеристиками
    Сбор результатов
    """

    menu()

    #Считывание данных из файла
    config = configparser.ConfigParser()

    print(config.sections())
    config.read("input.ini")
    print(config.sections())

    q = getSetting(config, "Settings", "amplitude-frequency").split(" | ")

    global a
    
    for i in q:
        w = []
        ew = (str(i)).split("; ")
        for j in ew:
            w.append(float(j))
        a.append(list(w))

    NODES_COUNT = int(getSetting(config, "Settings", "speciescount"))
    GENERATIONS_COUNT = int(getSetting(config, "Settings", "iterationscount"))
    COEF_MAX_NUMBER = int(getSetting(config, "Settings", "maxcoefcount"))
    EPSILON = float(getSetting(config, "Settings", "epsilon"))
  
    #Создание популяции
    nm = NodeManager(NODES_COUNT, GENERATIONS_COUNT)
    nm.run()

    #Вывод результатов
    nm.printLeader()

if __name__ == "__main__":
    sys.exit(main())
