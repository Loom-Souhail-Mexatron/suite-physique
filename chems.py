#from alchemy import *
#from guiWorks import app
import inspect


raw = []
elems = []
configs = {}

with open("./res/chemsList.txt","r") as f:
    lines = f.readlines()
    for line in range(0,len(lines),3):
        raw.append(lines[line][:-1])

    f.close()

for line in raw:
    p1 = line.split(":")[0].split(" ")
    elems.append(p1[1])
    configs[p1[2]] = line.split(": ")[1]


#Classement
GN = "Gaz nobles"
gn = ["He", "Ne", "Ar", "Kr", "Xe", "Rn"]

HA = "Halogènes"
ha = ["F", "Cl", "Br", "I"]

NM = "Non-métaux"
nm = ["H", "C", "N", "O", "S", "P", "Se"]

ME = "Métalloïdes"
me = ["B", "Si", "Ge", "As", "Sb", "Te", "At"]

MP = "Métaux pauvres"
mp = ["Al", "Zn", "Ga", "Cd", "In", "Sn", "Hg", "Tl", "Pb", "Bi", "Po"]

MT = "Métaux de transition"
mt = ["Sc","Ti","V","Cr","Mn","Fe","Co",
      "Ni","Cu","Y","Zr","Nb","Mo","Tc",
      "Ru","Rh","Pd","Ag","Hf","Ta","W",
      "Re","Os","Ir","Pt","Au","Rf","Dd","Sg","Bh","Hs","Cn"]

MA = "Métaux alcalins"
ma = ["Li","Na","K","Rb","Cs","Fr"]

MN = "Métaux alcalino-terreux"
mn = ["Be","Mg","Ca","Sr","Ba","Ra"]

LA = "Lanthanides"
la = ["La","Ce","Pr","Nd","Pm","Sm","Eu",
      "Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu"]

AC = "Actinides"
ac = ["Ac","Th","Pa","U","Np","Pu","Am","Cm",
      "Bk","Cf","Es","Fm","Md","No","Lr"]

natures = [gn, ha, nm, me, mp, mt, ma, mn, la, ac]

#Couleurs
atomColors = ['FFFFFF', 'D9FFFF', 'CC80FF', 'C2FF00', 'FFB5B5', '909090', '3050F8', 'FF0D0D',
              '90E050', 'B3E3F5', 'AB5CF2', '8AFF00', 'BFA6A6', 'F0C8A0', 'FF8000', 'FFFF30',
              '1FF01F', '80D1E3', '8F40D4', '3DFF00', 'E6E6E6', 'BFC2C7', 'A6A6AB', '8A99C7',
              '9C7AC7', 'E06633', 'F090A0', '50D050', 'C88033', '7D80B0', 'C28F8F', '668F8F',
              'BD80E3', 'FFA100', 'A62929', '5CB8D1', '702EB0', '00FF00', '94FFFF', '94E0E0',
              '73C2C9', '54B5B5', '3B9E9E', '248F8F', '0A7D8C', '006985', 'C0C0C0', 'FFD98F',
              'A67573', '668080', '9E63B5', 'D47A00', '940094', '429EB0', '57178F', '00C900',
              '70D4FF', 'FFFFC7', 'D9FFC7', 'C7FFC7', 'A3FFC7', '8FFFC7', '61FFC7', '45FFC7',
              '30FFC7', '1FFFC7', '00FF9C', '0382E5', '00D452', '00BF38', '00AB24', '4DC2FF',
              '4DA6FF', '2194D6', '267DAB', '266696', '175487', 'D0D0E0', 'FFD123', 'B8B8D0',
              'A6544D', '575961', '9E4FB5', 'AB5C00', '754F45', '428296', '420066', '007D00',
              '70ABFA', '00BAFF', '00A1FF', '008FFF', '0080FF', '006BFF', '545CF2', '785CE3',
              '8A4FE3', 'A136D4', 'B31FD4', 'B31FBA', 'B30DA6', 'BD0D87', 'C70066', 'CC0059',
              'D1004F', 'D90045', 'E00038', 'E6002E', 'EB0026']

def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_globals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

def retrieveNature(symbol): #returns string of nature name
    for natureList in natures:
        if symbol in natureList:
            #the variable name retriever is by a cool guy on github
            nam = retrieve_name(natureList)[0]
            return eval(str(nam).upper())


#valency
#9 means ?
valency = [1,0,1,2,3,4,3,2,1,0,1,2,3,4,3,2,1,0,1,2]

#neutrons
neutrons = [0,2,4,5,6,6,7,8,10,10,12,12,14,14,16,16,18,22,
            20,20,24,26,28,28,30,30,32,31,35,35,39,41,42,
            45,45,48,48,50,50,51,52,54,55,57,58,60,61,64,
            66,69,71,76,74,77,78,81,82,82,82,84,84,88,89,
            93,94,97,98,99,100,103,104,106,108,110,111,
            114,115,117,118,121,123,125,126,125,125,136,
            136,138,138,142,140,146,144,150,148,151,150,
            153,153,157,157,157]

#alchemy
from functools import lru_cache
#from chems import *

HE = "1s2"
NE = HE + " 2s2 2p6"
AR = NE + " 3s2 3p6"
KR = AR + " 3d10 4s2 4p6"
XE = KR + " 4d10 5s2 5p6"
RN = XE + " 4f14 5d10 6s2 6p6"

shellsMaxes = {
    'K':2,'L':8,'M':18,'N':32,'O':50
}

maxVals = [8,18-8, 32-18, 50-32,72-50,98-72,128-98]
shellex = [2,8,18,32,50]


@lru_cache
def handleConfig(config):
    config = config.split(" ")
    electrons = {}
    for shell in config:
        #print(shell)
        if shell[0] == "[":
            for i in eval(str(shell[1:-1]).upper()).split(" "):
                config.append(i)
            continue
        if not (shell[0] in electrons):
            electrons[shell[0]] = int(shell[2:])
        else:
            electrons[shell[0]] += int(shell[2:])
    return dict(sorted(electrons.items()))

def SD(val, maxVal):
    if val <= maxVal//2:
        return (val,0)
    elif val == maxVal:
        return (0,val//2)
    else:
        return (val - 2*(val%(maxVal//2)), val%(maxVal//2))

def getSD(val, maxVal):
    index = maxVal - 2
    if index == -1:
        return SD(val, maxVal*2)
    output = SD(val - maxVals[index] + (index+1)*index + 8, maxVals[index])
    return output
    

@lru_cache
def getShellsVal(elemName):
    shellOutput = ""
    shellTuples = sorted(handleConfig(configs[elemName]).items())
    for shellTuple in shellTuples:
        #print(shellTuple)
        try:
            shellOutput += '(' + sorted(shellsMaxes.keys())[int(shellTuple[0])-1] + ')'
        except IndexError:
            shellOutput += '(O)'
        shellOutput += str(shellTuple[1])
    val = shellTuples[-1][-1]
    '''print(val)
    print(shellTuples[-1])
    try:
        print(getSD(val,-1+shellex.index(sorted(shellsMaxes.items())[int(shellTuples[-1][0])][-1])))
        print()
    except ZeroDivisionError:
        print(getSD(val,-1))'''
    return (shellOutput, getSD(val, int(shellTuples[-1][0])))






#print(configs)
names = list(configs.items())
#print(names)

n = 19


if __name__ == "__main__":
    for i in range(len(names)):
        print(i+1,elems[i],names[i][0])
        print(getShellsVal(names[i][0])[0])
        valInfo = getShellsVal(names[i][0])
        print('Electrons de valence:', valInfo[0][-1])
        print("Num d'électrons célibataires:", valInfo[-1][0], 'Num de couples:', valInfo[-1][-1])
        input()


'''if __name__ == "__main__":
    app.mainloop()'''

#print(getShells('Sodium'))
