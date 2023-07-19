# Zadanie 2 - Eulerov kôň
# Samuel Kováč

import time
import copy

posunutia = [[1,2],[1,-2],[2,1],[2,-1],[-1,2],[-1,-2],[-2,1],[-2,-1]]

class Sachovnica:
    def __init__(self, n, startX, startY):
        self.n = n
        self.sachovnica = [[0]*int(n) for i in range(int(n))]
        if (startX >= 0 and startX < n) and (startY >= 0 and startY < n):
            self.poziciaX = startX
            self.poziciaY = startY
        else:
            print("Neplatné súradnice, použijem [0, 0]")
            self.poziciaX = 0
            self.poziciaY = 0
        
        self.sachovnica[self.poziciaX][self.poziciaY] = 1     #Nastaví 1 na začiatočnú pozíciu jazdca
        self.krok = 1
        self.startTime = 0

        #Spustí hľadanie riešení šachovnice
        self.vyries() 

    #Vráti hodnotu daného políčka v prípade správnych súradníc, inak vráti -1
    def hodnota(self, x, y):
        if ((x < self.n and x >= 0) and (y < self.n and y >= 0)):
            return self.sachovnica[x][y]
        else:
            return -1

    #Vypíše šachovnicu
    def vypis(self):
        for i in range(len(self.sachovnica)):
            for j in range(len(self.sachovnica)):
                for k in range(len(str(self.n*self.n)) - len(str(self.sachovnica[i][j]))):
                    print(" ", end="")
                print(self.sachovnica[i][j], end ="")
                if j != len(self.sachovnica)-1:
                    print(" | ", end ="")
            print("")
            
    #Posunie jazdca o zadané súradnice, ak je pohyb neplatný, vráti -1
    def posun(self, x, y):
        if(((self.poziciaX + x) < self.n and (self.poziciaX + x) >= 0) and ((self.poziciaY + y) < self.n and (self.poziciaY + y) >= 0) and (self.hodnota(self.poziciaX + x, self.poziciaY + y) == 0)):
            self.poziciaX += x
            self.poziciaY += y
            self.krok += 1
            self.sachovnica[self.poziciaX][self.poziciaY] = self.krok
            return 1
        else:
            return -1

    #Zistí počet možností skoku z daného políčka
    def pocetMoznosti(self, x, y):
        if(self.hodnota(x, y) != 0):
            return -1

        p = 0
        for i in range(8):
            if (self.hodnota(x + posunutia[i][0], y + posunutia[i][1]) == 0):
                p += 1
    
        return p

    #Nájde daľší možný pohyb po šachovnici. X a Y sú súradnice pohybu ktorý ešte treba vykonať
    def najdiPohyb(self, x, y):
        minimum = 8
        pocty = []
        moznosti = []
        sachovnica = copy.deepcopy(self)
        
        #Kontrola či riešenie nehľadáme príliš dlho
        end = time.perf_counter()
        if(end - self.startTime > 15):
            print("Presiahnutý maximálny čas hladania riešenia")
            return -1

        if x != 0 and y != 0 :
            if(sachovnica.posun(x, y) == -1):
                return self

        for i in range(8):
            x = sachovnica.pocetMoznosti(sachovnica.poziciaX + posunutia[i][0], sachovnica.poziciaY + posunutia[i][1])
            if x == -1:
                pocty.append(10)
            elif x == 0:
                pocty.append(9)
            else:
                pocty.append(x)   

        # Pokiaľ jazdec nemá kam skočiť, zacyklil sa alebo sme našli riešenie
        if min(pocty) == 10:
            if sachovnica.krok >= (sachovnica.n*sachovnica.n):
                print("Nájdené riešenie :")
                sachovnica.vypis()               
                return 1    #Ak sme našli riešenie, začne rekurzívne vracať 1

            return self

        # V prípade viacerých políčok s najmenšou hodnotou ich izolujeme
        for i in range(8):
            if pocty[i] == min(pocty):
                moznosti.append(i)

        # Pre všetky vybrané políčka pokračuje rekurzívne prehľadávanie do hĺbky
        for m in moznosti:
            if sachovnica == 1:
                return 1
            if sachovnica.krok >= (sachovnica.n*sachovnica.n):
                break
            if sachovnica.najdiPohyb(posunutia[m][0], posunutia[m][1]) == 1:
                return 1
        
        return self

    # pomocná funkcia pre spustenie rekurzívneho hľadania riešení
    def vyries(self):
        self.startTime = time.perf_counter()    # zapíše čas spustenia
        if(self.najdiPohyb(0, 0) != 1):
            print("Pre zadanú šachovnicu neexistuje riešenie") 
            
         
# dĺžka hrany šachovnice, štartovacia súradnica X jazdca, štartovacia súradnica Y jazdca
sachovnica = Sachovnica(20, 0, 0)
sachovnica = Sachovnica(8, 0, 1)
sachovnica = Sachovnica(8, 0, 2)
sachovnica = Sachovnica(8, 0, 3)
sachovnica = Sachovnica(8, 1, 0)
sachovnica = Sachovnica(8, 1, 1)
sachovnica = Sachovnica(8, 1, 2)
sachovnica = Sachovnica(8, 1, 3)
sachovnica = Sachovnica(8, 2, 2)
sachovnica = Sachovnica(8, 3, 3)