# Zadanie 3a - Zenová záhrada (Evolučný algoritmus)
# Samuel Kováč
import random
import copy
import statistics
import matplotlib.pyplot as plt

#Trieda génov záhrany
class Hrabanie:
    def __init__(self, zahrada):
        i = random.randint(0, len(zahrada.okraje)-1)
        self.riadok = zahrada.okraje[i][0]    #Riadková súradnica začiatku hrabania
        self.stlpec = zahrada.okraje[i][1]    #Stĺpcová súradnica začiatku hrabania
        zahrada.okraje.remove(zahrada.okraje[i])      

        if self.riadok == 0:
            self.smer = "Dole"
        elif self.riadok == zahrada.riadky-1:
            self.smer = "Hore"
        elif self.stlpec == 0:
            self.smer = "Doprava"
        elif self.stlpec == zahrada.stlpce-1:
            self.smer = "Dolava"
        
        self.rozhodnutia = ""
        self.vygeneruj_rozhodnutia()

    def vygeneruj_rozhodnutia(self):
        #Vygeneruje náhodné rozhodnutia mnícha
        self.rozhodnutia = ""
        for _ in range(8):
            self.rozhodnutia += random.choice(["0", "1"])        

#Hlavná trieda - záhrada
class Zahrada:
    def __init__(self, riadky, stlpce, *kamene):
        self.riadky = riadky
        self.stlpce = stlpce
        self.zahrada = [[0]*int(stlpce) for i in range(int(riadky))]
        self.kamene = 0
        self.hrabania = []
        self.hrabanie = 0
        self.okraje = []
        self.fitness = 0

        self.zisti_volne_okraje()

        #Pridanie kameňov do záhrady
        for k in kamene:
            self.zahrada[k[0]][k[1]] = "K"
            self.kamene += 1

        #Uložíme si pôvodnú záhradu do budúcna
        self.povodna_zahrada = copy.deepcopy(self.zahrada)

    def zisti_volne_okraje(self):
        self.okraje.clear()

        for s in range(self.stlpce):
            if self.policko(0, s) == 0:
                self.okraje.append((0, s))
        for r in range(self.riadky):
            if self.policko(r, self.stlpce-1) == 0:
                self.okraje.append((r, self.stlpce-1))
        for s in range(self.stlpce):
            if self.policko(self.riadky-1, s) == 0:
                self.okraje.append((self.riadky-1, s))
        for r in range(self.riadky):
            if self.policko(r, 0) == 0:
                self.okraje.append((r, 0))

    def policko(self, riadok, stlpec):
        if((riadok >= 0 and riadok < self.riadky) and (stlpec >= 0 and stlpec < self.stlpce)):
            if self.zahrada[riadok][stlpec] != "K":
                return self.zahrada[riadok][stlpec]
            else:
                return 99
        else:
            return -1

    #Funkcia na výpis záhrady
    def vypis(self):
        print("╔", end="")
        for i in range(self.stlpce):
            print("════", end="")
        print("╗")

        for i in range(self.riadky):
            print("║", end="")
            for j in range(self.stlpce):
                if len(str(self.zahrada[i][j])) < 2:
                    print(" ", end="")
                print(" ", end="")
                print(self.zahrada[i][j], end =" ")
            print("║")

        print("╚", end="")
        for i in range(self.stlpce):
            print("════", end="")
        print("╝")

    #Funkcia spočíta počet pohrabaných políčok
    def pocet_pohrabanych(self):
        uspesne = 0
        for i in range(self.riadky):
            for j in range(self.stlpce):
                if self.zahrada[i][j] != 0:
                    uspesne += 1
        return (uspesne - self.kamene)

    #Počet pohrabaných delené počtom všetkých políčok bez kameňov (0 - nepohrabaná, 1 - pohrabaná celá záhrada)
    def vypocitaj_fitness(self):
        self.fitness = self.pocet_pohrabanych() / ((self.riadky * self.stlpce) - self.kamene)

    def vygeneruj_hrabania(self):
        n = self.riadky + self.stlpce + self.kamene
        for _ in range(n):
            self.hrabania.append(Hrabanie(self))           
        self.pohrab()
        self.vypocitaj_fitness()

    def pohrab(self):
        self.hrabanie = 0
        for h in self.hrabania:
            r = h.riadok
            s = h.stlpec
            if self.policko(r, s) == 0:
                self.hrabanie += 1
            else:
                continue
            i = 0
            smer = h.smer
            while(self.policko(r, s) != -1):
                if self.policko(r, s) == 0:
                    self.zahrada[r][s] = self.hrabanie

                    if smer == "Hore":
                        r -= 1
                    elif smer == "Dole":
                        r += 1
                    elif smer == "Doprava":
                        s += 1
                    elif smer == "Dolava":
                        s -= 1
                else :  #je tam prekazka, musime sa vratit
                    #Smery Hore a Dole
                    if smer == "Hore" or smer == "Dole":
                        if smer == "Hore":
                            r += 1
                        else:
                            r -= 1
                        #Ak sú dostupné oba smery, vyberieme na základe rozhodnutia
                        if self.policko(r, s+1) <= 0 and self.policko(r, s-1) <= 0:
                            if h.rozhodnutia[i % 8] == 0:
                                i += 1
                                s += 1
                                smer = "Doprava"
                            else :
                                i += 1
                                s -= 1
                                smer = "Dolava"
                        elif self.policko(r, s+1) <= 0:
                            s += 1
                            smer = "Doprava"
                        elif self.policko(r, s-1) <= 0:
                            s -= 1
                            smer = "Dolava"
                        else :
                            return -1

                    #Smery Doprava a Dolava
                    else:
                        if smer == "Doprava":
                            s -= 1
                        else:
                            s += 1
                        #Ak sú dostupné oba smery, vyberieme na základe rozhodnutia
                        if self.policko(r+1, s) <= 0 and self.policko(r-1, s) <= 0:
                            if h.rozhodnutia[i % 8] == 0:
                                i += 1
                                r += 1
                                smer = "Dole"
                            else :
                                i += 1
                                r -= 1
                                smer = "Hore"
                        elif self.policko(r+1, s) <= 0:
                            r += 1
                            smer = "Dole"
                        elif self.policko(r-1, s) <= 0:
                            r -= 1
                            smer = "Hore"
                        else :
                            return -1   
                   
                    
    def zamiesaj_geny(self, z2):
        #Skopírujem pôvodnu záhradu do z1 a premažem pôvodnú záhradu
        z1 = copy.deepcopy(self)
        self.zahrada = copy.deepcopy(self.povodna_zahrada)
        self.hrabania.clear()
        x = random.random()
        if x < 0.49:
            #Náhodne rozdelí hrabania, pričom prvú časť zoberie zo záhrady 1 a druhú časť zo záhrady 2
            r = random.randrange(z2.hrabanie)
            self.hrabania = z1.hrabania[:r] + z2.hrabania[r:]
        else :
            #Náhodne vyberá gény medzi záhradami 1 a 2 a pridáva ich do novej záhrady
            for i in range(len(z1.hrabania)):
                if random.random() <= 0.49:
                    self.hrabania.append(z1.hrabania[i])
                else:
                    self.hrabania.append(z2.hrabania[i])
        
        #Mutácie génov
        for h in self.hrabania:
            if self.hrabania.index(h) > self.hrabanie:
                break
            x = random.random()
            #Šanca na nové vygenerovanie rozhodnutí
            if x < 0.15:
                h.vygeneruj_rozhodnutia()
            #Šanca že celé hrabanie nahradíme novým
            elif x < 0.2:
                i = self.hrabania.index(h)
                self.hrabania.remove(h)
                self.zisti_volne_okraje()
                self.hrabania.insert(i, Hrabanie(self))            

        #Na základe zamiešaných génov sa znova pohrabe záhrada
        self.pohrab()
        self.vypocitaj_fitness()

#Vygeneruje hrabania pre prvú generáciu záhrad
def vytvor_generaciu(zahrada, pocet):
    generacia = []

    for j in range(pocet):
        z = copy.deepcopy(zahrada)
        z.vygeneruj_hrabania()
        generacia.append(z)

    return generacia

#Náhodne vyberá jedincov, čím vyššia hodnota fitness, tým väčšia šanca na výber
def ruleta(generacia, fitness_list, pocet_najlepsich):
    fitness_spolu = float(sum(fitness_list))
    fitness_rel = []
    for f in fitness_list:
        fitness_rel.append(f / fitness_spolu)
    
    sance = [sum(fitness_rel[:i+1]) for i in range(len(fitness_rel))]

    najlepsie_riesenia = []
    for n in range(pocet_najlepsich):
        r = random.random()
        for (i, zahrada) in enumerate(generacia):
            if r <= sance[i]:
                najlepsie_riesenia.append(zahrada)               
                break
    
    g = []
    #Každý z vybraných jedincov sa kríži s dvoma náhodnými vybranými jedincami
    for z in najlepsie_riesenia:
            z1 = copy.deepcopy(z)
            z2 = copy.deepcopy(z)
            k1 = random.choice(najlepsie_riesenia)           
            k2 = random.choice(najlepsie_riesenia)

            z1.zamiesaj_geny(k1)        
            z2.zamiesaj_geny(k2)
          
            g.append(z1)
            g.append(z2)

    return g

#Vyberie IBA najlepších jedincov z každej generácie
def najlepsi(generacia, pocet_najlepsich):
    poradie = sorted(generacia, key=lambda z: z.fitness, reverse=True)
    najlepsie_riesenia = poradie[:pocet_najlepsich]
    g = []
    #Každý z vybraných jedincov sa kríži s dvoma náhodnými vybranými jedincami
    for z in najlepsie_riesenia:
            z1 = copy.deepcopy(z)
            z2 = copy.deepcopy(z)
            k1 = random.choice(najlepsie_riesenia)           
            k2 = random.choice(najlepsie_riesenia)

            z1.zamiesaj_geny(k1)        
            z2.zamiesaj_geny(k2)
          
            g.append(z1)
            g.append(z2)

    return g

def vzorkovanie(generacia, najlepsia):
    najlepsie_riesenia = [najlepsia]
    for _ in range(len(generacia)-1):
        sample = random.sample(generacia, 4)
        i1, i2 = sorted(sample, key=lambda x: x.fitness, reverse=True)[:2]
        z1 = copy.deepcopy(i1)
        z1.zamiesaj_geny(i2)
        najlepsie_riesenia.append(z1)
    return najlepsie_riesenia

def evolucia(generacia, maxGeneracii):
    priemery = []
    najlepsie = []
    fitness_list = []
    g = 0
    pocet_najlepsich = int(len(generacia) / 2)

    while(g < maxGeneracii):
        g += 1
        fitness_list.clear()
        for z in generacia:
            fitness_list.append(z.fitness)
            if z.fitness == 1:
                print("Riešenie bolo nájdené v generácií ", g)
                z.vypis()

                plt.plot(priemery)
                plt.ylabel('Priemerna fitness')
                plt.xlabel('Generacia')
                plt.show()

                plt.plot(najlepsie)
                plt.ylabel('Najlepsia fitness')
                plt.xlabel('Generacia')
                plt.show()

                return 1

        median_fitnes = statistics.median(fitness_list)
        max_fit = max(fitness_list)
        max_zahrada = max(generacia, key=lambda z: z.fitness)


        generacia = ruleta(generacia, fitness_list, pocet_najlepsich)
        #generacia = najlepsi(generacia, pocet_najlepsich)        
        #generacia = copy.deepcopy(vzorkovanie(generacia, max_zahrada))
        
        generacia[0] = max_zahrada
      
        priemery.append(sum(fitness_list) / len(fitness_list))
        najlepsie.append(max(fitness_list))
        print("Generacia " + str(g) +" | Priemerna fitness : " + str(round(priemery[-1], 2)) + " | Najlepsia fitness : " + str(najlepsie[-1]))

    plt.plot(priemery)
    plt.ylabel('Priemerna fitness')
    plt.xlabel('Generacia')
    plt.show()

    plt.plot(najlepsie)
    plt.ylabel('Najlepsia fitness')
    plt.xlabel('Generacia')
    plt.show()
    max_zahrada.vypis()


#Vytvorenie záhrady - riadky, stĺpce, lubovoľný počet kameňov(riadok, stĺpec)
zahrada = Zahrada(10, 12, (2,1), (4,2), (1,5), (3,4), (6,8), (6,9))
generacia = vytvor_generaciu(zahrada, 100)
evolucia(generacia, 200)