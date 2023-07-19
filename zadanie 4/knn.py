#Zadanie 4a - klasifikácia
#Samuel Kováč

import random
import time
import math
import copy
import numpy as np
import matplotlib.pyplot as plt

N = 5000    #pocet bodov pre kazdu farbu

graf_farby = {
  'R': "red",
  'G': "green",
  'B': "blue",
  'P': "purple"
}

dataset = []

red = []
green = []
blue = []
purple = []

class Bod:
    def __init__(self, x, y, farba):
        self.x = x
        self.y = y
        self.farba = farba
        self.vzdialenost = 0

    def vypocitaj_vzdialenost(self, x, y):
        self.vzdialenost = math.sqrt(pow(x - self.x, 2) + pow(y - self.y,2))

def classify(X, Y, k):
    global dataset

    #Každému bodu prepočíta vzdialenosť
    for bod in dataset:
        bod.vypocitaj_vzdialenost(X, Y)

    #Zoradí body podľa vzdialenosti
    najblizsi = sorted(dataset, key=lambda b: b.vzdialenost)

    r = 0
    g = 0
    b = 0
    p = 0

    #Zistíme najfrekventovanejšiu farbu medzi *k* najbližšími bodmi
    for bod in najblizsi[:k]:
        if bod.farba == 'R':
            r += 1
        elif bod.farba == 'G':
            g += 1
        elif bod.farba == 'B':
            b += 1
        else:
            p += 1

    farba = max(r,g,b,p)

    if farba == r:
        dataset.append(Bod(X, Y, 'R'))
        return 'R'
    elif farba == g:
        dataset.append(Bod(X, Y, 'G'))
        return 'G'
    elif farba == b:
        dataset.append(Bod(X, Y, 'B'))
        return 'B'
    else:
        dataset.append(Bod(X, Y, 'P'))
        return 'P'

#Vymaže dataset a pridá body zo zadania
def inicializuj_dataset():
    global dataset
    dataset.clear()
    R1 = Bod(-4500, -4400, 'R')
    R2 = Bod(-4100, -3000, 'R')
    R3 = Bod(-1800, -2400, 'R')
    R4 = Bod(-2500, -3400, 'R')
    R5 = Bod(-2000, -1400, 'R')
    G1 = Bod(4500, -4400, 'G')
    G2 = Bod(4100, -3000, 'G')
    G3 = Bod(1800, -2400, 'G')
    G4 = Bod(2500, -3400, 'G')
    G5 = Bod(2000, -1400, 'G')
    B1 = Bod(-4500, 4400, 'B')
    B2 = Bod(-4100, 3000, 'B')
    B3 = Bod(-1800, 2400, 'B')
    B4 = Bod(-2500, 3400, 'B')
    B5 = Bod(-2000, 1400, 'B')
    P1 = Bod(4500, 4400, 'P')
    P2 = Bod(4100, 3000, 'P')
    P3 = Bod(1800, 2400, 'P')
    P4 = Bod(2500, 3400, 'P')
    P5 = Bod(2000, 1400, 'P')

    dataset.extend((R1, R2, R3, R4, R5, G1, G2, G3, G4, G5, B1, B2, B3, B4, B5, P1, P2, P3, P4, P5))

#Vygeneruje body do zásobníkov
def vygeneruj_body():
    #RED
    for i in range(N):
        if random.random() < 0.99:
            while True:
                x = random.randint(-5000, 500)
                y = random.randint(-5000, 500)
                b = Bod(x, y, 'R')
                if b not in red:
                    break
        else:            
            while True:
                x = random.randint(-5000, 5000)
                y = random.randint(-5000, 5000)
                b = Bod(x, y, 'R')
                if b not in red:
                    break
        red.append(b)

    #GREEN
    for i in range(N):
        if random.random() < 0.99:
            while True:
                x = random.randint(-500, 5000)
                y = random.randint(-5000, 500)
                b = Bod(x, y, 'G')
                if b not in green:
                    break
        else:            
            while True:
                x = random.randint(-5000, 5000)
                y = random.randint(-5000, 5000)
                b = Bod(x, y, 'G')
                if b not in green:
                    break
        green.append(b)

    #BLUE
    for i in range(N):
        if random.random() < 0.99:
            while True:
                x = random.randint(-5000, 500)
                y = random.randint(-500, 5000)
                b = Bod(x, y, 'B')
                if b not in blue:
                    break
        else:            
            while True:
                x = random.randint(-5000, 5000)
                y = random.randint(-5000, 5000)
                b = Bod(x, y, 'B')
                if b not in blue:
                    break
        blue.append(b)

    #PURPLE
    for i in range(N):
        if random.random() < 0.99:
            while True:
                x = random.randint(-500, 5000)
                y = random.randint(-500, 5000)
                b = Bod(x, y, 'P')
                if b not in purple:
                    break
        else:            
            while True:
                x = random.randint(-5000, 5000)
                y = random.randint(-5000, 5000)
                b = Bod(x, y, 'P')
                if b not in purple:
                    break
        purple.append(b)

#Inicializácia grafu
plt.xlim(-5000, 5000)
plt.ylim(-5000, 5000)
plt.yticks(np.arange(-5000, 5001, 1000))
plt.yticks(np.arange(-5000, 5001, 1000))
plt.xlabel("x")
plt.ylabel("y")
fig, axs = plt.subplots(2, 2)
plt.suptitle('Zadanie 4a - klasifikácia')

vygeneruj_body()

for k in [1, 3, 7, 15]:
    zaciatok = time.time()
    pocet_chyb = 0
    inicializuj_dataset()
    zoznam_R = copy.deepcopy(red)
    zoznam_G = copy.deepcopy(green)
    zoznam_B = copy.deepcopy(blue)
    zoznam_P = copy.deepcopy(purple)

    farby = ['R', 'G', 'B', 'P']
    posledna_farba = ''
    while len(farby) > 1:
        while True:
            farba = random.choice(farby)
            if farba != posledna_farba:
                break
            if len(farby) == 1:
                farba = farby[0]
                break

        if farba == 'R':
            bod = zoznam_R.pop(0)
            posledna_farba = classify(bod.x, bod.y, k)

            if posledna_farba != 'R':
                pocet_chyb += 1

            if len(zoznam_R) == 0:
                farby.pop(farby.index('R'))

        elif farba == 'G':
            bod = zoznam_G.pop(0)
            posledna_farba = classify(bod.x, bod.y, k)

            if posledna_farba != 'G':
                pocet_chyb += 1

            if len(zoznam_G) == 0:
                farby.pop(farby.index('G'))

        elif farba == 'B':
            bod = zoznam_B.pop(0)
            posledna_farba = classify(bod.x, bod.y, k)

            if posledna_farba != 'B':
                pocet_chyb += 1

            if len(zoznam_B) == 0:
                farby.pop(farby.index('B'))

        else:
            bod = zoznam_P.pop(0)
            posledna_farba = classify(bod.x, bod.y, k)

            if posledna_farba != 'P':
                pocet_chyb += 1

            if len(zoznam_P) == 0:
                farby.pop(farby.index('P'))
        

    koniec = time.time()
    print("Pri klasifikácií (k = " + str(k) + ") bolo nájdených", pocet_chyb, "chýb, klasifikácia trvala", round(koniec - zaciatok), "s")

    x_2D_list = []
    y_list = []
    for bod in dataset:
        if k == 1:
            axs[0, 0].plot(bod.x, bod.y, marker="o", color=graf_farby[bod.farba])
            axs[0, 0].set_title("k = 1")
        if k == 3:
            axs[0, 1].plot(bod.x, bod.y, marker="o", color=graf_farby[bod.farba])
            axs[0, 1].set_title("k = 3")
        if k == 7:
            axs[1, 0].plot(bod.x, bod.y, marker="o", color=graf_farby[bod.farba])
            axs[1, 0].set_title("k = 7")
        if k == 15:
            axs[1, 1].plot(bod.x, bod.y, marker="o", color=graf_farby[bod.farba])
            axs[1, 1].set_title("k = 15")

fig.tight_layout()
plt.savefig(r'C:\Users\samue\Desktop\Skola\5. Semester\UI\zadanie 4\knn')