import time
import numpy as np



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



def depense_puissance_duree(ftp,puissance,temps):
    if puissance<=0.55*ftp:
         return -temps*0.02
    if puissance<=0.75*ftp:
        return temps*0.007
    if puissance<=0.89*ftp:
        return temps*0.014
    return (temps*puissance/(duree_tenable(ftp,puissance)*puissance_tenable(ftp,duree_tenable(ftp,puissance))))*100

pt=puissance_tenable(ftp=300,temps=3600)
dt=duree_tenable(ftp=300,puissance=300)
dpd=depense_puissance_duree(ftp=350,puissance=270,temps=1)


print("puissance tenable sur 1h =",pt,"w")
print("duree tenable avec 300w =",dt,"sec")
print("depense avec 300w sur 60min =",dpd,"pv depenses sur 100")
print("~~~~~~~~~~~~")
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


def ajustement_energie(energie,depense):
    if energie-depense>100:
        return 100
    if energie-depense<=0:
        return 0
    return energie-depense




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

    energie=100
    print(len(gpx),"sec")
    sec=0
    for i in gpx:
        energie=ajustement_energie(energie,depense_puissance_duree(ftp=277,puissance=i,temps=1))
        if energie==0:
            print("Ne pas craquer")
        print(sec,"sec ",i,"w ",energie,"pv")
        sec+=1
        time.sleep(0.1)

main()