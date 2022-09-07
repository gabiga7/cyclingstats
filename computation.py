import numpy as np


def puissance_tenable(ftp,temps):
    return 1800/np.log(temps)+15*np.log(temps)+ftp-342

def duree_tenable(ftp,puissance):
    return np.exp((-ftp+342+puissance-np.sqrt(np.power(puissance,2)+84*puissance-106236))/30)

def depense_puissance_duree(ftp,puissance,temps):
    return ((temps*ftp/duree_tenable(ftp,puissance))/puissance_tenable(ftp,duree_tenable(ftp,puissance)))*100

ftp=300
pt=puissance_tenable(ftp,3600)
dt=duree_tenable(ftp,300)
dpd=depense_puissance_duree(ftp,300,1200)


print("puissance tenable sur 1h =",pt)
print("duree tenable avec 300w =",dt)
print("depense avec 300w sur 20min =",dpd)
