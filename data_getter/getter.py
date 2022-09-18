import asyncio
from bleak import BleakClient

from pycycling.cycling_power_service import CyclingPowerService






from cProfile import label
import time
from tkinter.ttk import Style
from turtle import width
import numpy as np

import sys



from ast import main
import matplotlib.pyplot as plt

import re

import os


def get_extension(filename):
    split_tup = os.path.splitext(filename)
    return split_tup[1]


def get_power_list(filename,extension):
    list=[]
    print(extension)
    if extension==".tcx":
        balise='\s+<ns3:Watts>(\d+.\d+)'
    elif extension==".gpx":
        balise='\s+<power>(\d+.\d+)'
    else:
        exit(-1)
    print("test")
    with open(filename, 'rt') as f:
        for line in f:
            #print(line),
            match = re.match(balise,line)
            if match:
                power_in_watt = float(match.group(1))
                #print (power_in_watt)
                list.append(power_in_watt)      
    return list

def readable_power_data(data):
    to_add=0
    readable=[]
    for i in range(len(data)):
        to_add+=data[i]
        if i%60==0:
            for i in range(60):
                readable.append(to_add/60)
            to_add=0
    return readable





def create_line(array,line_type):

    plt.plot(array, "-b",color=line_type,linewidth=2)
    plt.xticks(rotation=60)



def main_plot(power_data,bj_data,br_data):
    
    
    plt.figure(200)
    #power_points=create_points(power_data)
    #power_line=create_line(power_points,"blue")
    create_line(power_data,"blue")
    

    
    plt.xlabel('power history(w)',color="blue")
    plt.ylabel('temps (s)', color="blue")
    plt.legend()
    plt.grid()
    plt.axis([0,len(power_data),0,max(power_data)])
    plt.title('power history')
    
    

    plt.figure(250)
    #power_points=create_points(power_data)
    #power_line=create_line(power_points,"blue")
    readable=readable_power_data(power_data)
    create_line(readable,"black")
    

    plt.xlabel('readable power history(w)',color="black")
    plt.ylabel('temps (s)', color="black")
    plt.legend()
    plt.grid()
    plt.axis([0,len(readable),0,max(readable)])
    plt.title('readable power history')



    
    plt.figure(300)

    create_line(bj_data,"yellow")
    create_line(br_data,"red")
    
    plt.xlabel('energy bars (%)',color="orange")
    plt.xlabel('red bar (%)',color="red")

    plt.ylabel('temps (s)', color="blue")
    plt.legend()
    plt.grid()
    plt.axis([0,len(power_data),0,100])
    plt.title('two lines')
    plt.show()






def ajustement_depense_bj(ftp,puissance,depense):
    #print(1-1/(np.exp(duree_tenable(ftp,puissance)/(ftp/3))))
    return depense*(1-1/(np.exp(duree_tenable(ftp,puissance)/(1.5*ftp))))


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
        return temps*0.00035
    if puissance<=0.89*ftp:
        return temps*0.007
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




    








energie_bj=100

async def run(address):
    async with BleakClient(address) as client:
        def my_measurement_handler(data):
            print(data[0])
            global energie_bj
            energie_bj=ajustement_energie_bj(energie_bj,depense_puissance_duree_bj(ftp=150,puissance=data[0],temps=1))
            num_lines = len(open("tmp_bj.txt").readlines(  ))
            f = open("tmp_bj.txt", "a")
            f.write(str(num_lines)+","+str(energie_bj)+"\n")
            f.close()
            global energie_br
            energie_br=ajustement_energie_br(energie_br,depense_puissance_duree_br(ftp=150,puissance=data[0],temps=1))
            num_lines = len(open("tmp_br.txt").readlines(  ))
            f = open("tmp_br.txt", "a")
            f.write(str(num_lines)+","+str(energie_br)+"\n")
            f.close()


        await client.is_connected()
        trainer = CyclingPowerService(client)
        trainer.set_cycling_power_measurement_handler(my_measurement_handler)
        await trainer.enable_cycling_power_measurement_notifications()
        await asyncio.sleep(300.0)
        await trainer.disable_cycling_power_measurement_notifications()


if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)

    device_address = "7D:06:39:34:D8:21"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(device_address))
