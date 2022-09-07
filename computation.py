import numpy as np



def puissance_tenable(ftp,temps):
    return 1800/np.log(temps)+15*np.log(temps)+ftp-342

def duree_tenable(ftp,puissance):
    tab=[]
    prec=puissance_tenable(ftp,2)
    for i in range(3,5000):
        act=puissance_tenable(ftp,i)
        if act>prec:
            break
        tab.append(act)
    return np.argmin(np.abs(np.array(tab)-puissance))


def depense_puissance_duree(ftp,puissance,temps):
    return ((temps*ftp/duree_tenable(ftp,puissance))/puissance_tenable(ftp,duree_tenable(ftp,puissance)))*100

ftp=300
pt=puissance_tenable(ftp,3600)
dt=duree_tenable(ftp,200)
#dpd=depense_puissance_duree(ftp,400,240)


print("puissance tenable sur 1h =",pt,"w")
print("duree tenable avec 300w =",dt,"sec")
#print("depense avec 400w sur 3min =",dpd,"pv depenses sur 100")
