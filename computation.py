import time
import numpy as np


def ajustement_depense_bj(ftp,puissance,depense):
    #print(1-1/(np.exp(duree_tenable(ftp,puissance)/(ftp/3))))
    return depense*(1-1/(np.exp(duree_tenable(ftp,puissance)/(ftp/3))))


def puissance_tenable(ftp,temps):
    return 1900/np.log(temps)+15*np.log(temps)+ftp-354.858

def duree_tenable(ftp,puissance):
    prec=puissance_tenable(ftp,2)
    for i in range(3,7200):
        act=puissance_tenable(ftp,i)
        if act>prec:
            break
        if act<=puissance:
            return i
    return i



def depense_puissance_duree_bj(ftp,puissance,temps):
    if puissance<=0.55*ftp:
         return -temps*0.02
    if puissance<=0.75*ftp:
        return temps*0.007
    if puissance<=0.89*ftp:
        return temps*0.014
    depense=(temps*puissance/(duree_tenable(ftp,puissance)*puissance_tenable(ftp,duree_tenable(ftp,puissance))))*100
    #print("depense de base  : ",depense)
    if puissance>=1.1*ftp:
        return temps*ajustement_depense_bj(ftp,puissance,depense)
    return depense

def depense_puissance_duree_br(ftp,puissance,temps):
    if puissance<=0.9*ftp:
        return -temps*0.083
    if puissance>=1.1*ftp:
        return (temps*puissance/(duree_tenable(ftp,puissance)*puissance_tenable(ftp,duree_tenable(ftp,puissance))))*100
    return 0


pt=puissance_tenable(ftp=300,temps=300)
dt=duree_tenable(ftp=300,puissance=1050)

#dpd=depense_puissance_duree_bj(ftp=300,puissance=325,temps=1)
#print("depense avec =",dpd,"pv depenses sur 100")
#print("~~~~")
dpd=depense_puissance_duree_br(ftp=300,puissance=200,temps=1)
#print("depense avec =",dpd,"pv depenses sur 100")


#print("puissance tenable =",pt,"w")
#print("duree tenable =",dt,"sec")
#print("depense avec =",dpd,"pv depenses sur 100")
#print("~~~~~~~~~~~~")
print()


bloc_1=[150]*30
bloc_2=[350]*30
bloc_3=[300]*30
bloc_4=[200]*300
bloc_5=[400]*15
bloc_6=[200]*300
bloc_7=[400]*15
bloc_8=[200]*300
bloc_9=[400]*15
bloc_10=[200]*300
bloc_11=[250]*150
bloc_12=[275]*150
bloc_13=[300]*150
bloc_14=[350]*150
bloc_15=[400]*15
bloc_16=[800]*5
bloc_17=[1100]*3


def ajustement_energie_bj(energie_bj,depense):
    if energie_bj-depense>100:
        return 100
    if energie_bj-depense<=0:
        return 0
    return energie_bj-depense

def ajustement_energie_br(energie_br,depense):
    if energie_br-depense>100:
        return 100
    if energie_br-depense<=0:
        return 0
    return energie_br-depense




def main():
    gpx=[]

    gpx+=(bloc_1)
    gpx+(bloc_2)
    gpx+=(bloc_3)
    gpx+=(bloc_4)
    gpx+=(bloc_5)
    gpx+=(bloc_6)
    gpx+=(bloc_7)
    gpx+=(bloc_8)
    gpx+=(bloc_9)
    gpx+=(bloc_10)
    gpx+=(bloc_11)
    gpx+=(bloc_12)
    gpx+=(bloc_13)
    gpx+=(bloc_14)
    gpx+=(bloc_15)
    gpx+=(bloc_16)
    gpx+=(bloc_17)

    energie_bj=100
    energie_br=100
    print(len(gpx),"sec")
    sec=0
    for i in gpx:
        energie_bj=ajustement_energie_bj(energie_bj,depense_puissance_duree_bj(ftp=277,puissance=i,temps=1))
        energie_br=ajustement_energie_br(energie_br,depense_puissance_duree_br(ftp=277,puissance=i,temps=1))
        if energie_bj==0:
            print("Vous avez besoin de récupérer de la barre jaune")
        if energie_br==0:
            print("Vous avez besoin de récupérer de la barre rouge")
        print("~~")
        print(sec,"sec")
        print(i,"w")
        print("barre jaune : ",energie_bj,"pv")
        print("barre rouge : ",energie_br,"pv")

        sec+=1
        time.sleep(0.1)

main()
