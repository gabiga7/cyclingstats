from ast import arg
from sys import stdout
import numpy as np
from bleak import BleakClient
import asyncio
from tkinter import Tk, Label, Entry, Button, Radiobutton, IntVar
import os
from pycycling.cycling_power_service import CyclingPowerService
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import asyncio
from bleak import BleakScanner


devices=[]

def ajustement_depense_bj(puissance,depense, cyclist):
    return depense*(1-1/(np.exp(duree_tenable(puissance,cyclist)/(1.5*cyclist.ftp))))




def puissance_tenable(temps,cyclist):
    (profile,facteur)=function_chooser(cyclist)
    if profile=="polyvalent":
        return 1900/np.log(temps)+15*np.log(temps)+cyclist.ftp-354.858
    if profile=="rouleur":
        return (1900-(facteur*2.5))/np.log(temps)+(15+(facteur*0.5))*np.log(temps)+cyclist.ftp-354.858
    if profile=="puncher":
        return (1900+(facteur*50))/np.log(temps)+(15-(facteur))*np.log(temps)+cyclist.ftp-354.858





def duree_tenable(puissance, cyclist):
    prec=puissance_tenable(2, cyclist)
    for i in range(3,7200):
        act=puissance_tenable(i, cyclist)
        if act>prec:
            break
        if act<=puissance:
            return i
    return i



def depense_puissance_duree_bj(puissance,temps, cyclist):
    if puissance<=0.55*cyclist.ftp:
         return -temps*0.02
    if puissance<=0.75*cyclist.ftp:
        return temps*0.00035
    if puissance<=0.89*cyclist.ftp:
        return temps*0.007
    depense=(temps*puissance/(duree_tenable(puissance, cyclist)*puissance_tenable(duree_tenable(puissance, cyclist),cyclist)))*100
    if puissance>=1.1*cyclist.ftp:
        return temps*ajustement_depense_bj(puissance,depense,cyclist)
    return depense

def depense_puissance_duree_br(puissance,temps, cyclist):
    if puissance<=0.9*cyclist.ftp:
        return -temps*0.083
    if puissance>=1.1*cyclist.ftp:
        return (temps*puissance/(duree_tenable(puissance, cyclist)*puissance_tenable(duree_tenable(puissance, cyclist), cyclist)))*100
    return 0

    
def get_power(filename="tmp_power.txt"):
    """this function gets the power from the csv file"""
    with open(filename, "r") as file:
        data = file.read()
        data = data.split(",")
    if data==[] or data==['']:
        return 0
    return int(data[-1])


    


class Cyclist:
    """this class is used to create a cyclist object"""
    def __init__(self, ftp, fthr, pma, age, imc, profile, bj, br, device):
        self.ftp = int(ftp)
        self.fthr = int(fthr)
        self.pma = int(pma)
        self.age = int(age)
        self.imc = float(imc)
        self.profile = int(profile)
        self.bj = float(bj)
        self.br = float(br)
        self.device = str(device)
    
    def update_bj(self):
        power=get_power("tmp_power.txt")
        depense=depense_puissance_duree_bj(power,1,self)
        if self.bj-depense>100:
            self.bj=100
        if self.bj-depense<=0:
            self.bj=0
        self.bj=self.bj-depense

    def update_br(self):
        power=get_power("tmp_power.txt")
        depense=depense_puissance_duree_br(power,1,self)
        if self.br-depense>100:
            self.br=100
        if self.br-depense<=0:
            self.br=0
        self.br=self.br-depense






def gui():
    """this is a function that creates a gui with 5 entry fields and a button"""
    from tkinter import Tk, Label, Entry, Button, Radiobutton, ttk , StringVar, Scale, HORIZONTAL
    global devices
    root = Tk()
    root.title("Auto")
    root.geometry("600x200")
    root.resizable(False, False)
    root.configure(bg="white")
    device= StringVar()
    def update_devices():
        Combo["values"]=devices
    Combo = ttk.Combobox(root, values = devices, textvariable=device,postcommand=update_devices)
    Combo.set("Select your BLE power meter / home trainer")
    Combo.grid(row=0, column= 2)
    global status
    status=Label(root, bg='white', fg='black', width=20, text='No device selected')
    status.grid(row=1, column=2)
    
    def discover():
        status.config(text="Updating device list ...")
        root.update()
        async def discover_async():
            devices = await BleakScanner.discover()
            return devices
        global devices
        devices = asyncio.run(discover_async())
        status.config(text="Device list updated")

    Button(root, text="Search device", command=lambda: discover()).grid(row=0, column=3)

    Label(root, text="ftp", bg="white").grid(row=0, column=0)
    Label(root, text="fthr", bg="white").grid(row=1, column=0)
    Label(root, text="pma", bg="white").grid(row=2, column=0)
    Label(root, text="age", bg="white").grid(row=3, column=0)
    Label(root, text="imc", bg="white").grid(row=4, column=0)
    ftp = Entry(root)
    fthr = Entry(root)
    pma = Entry(root)
    age = Entry(root)
    imc = Entry(root)
    ftp.grid(row=0, column=1)
    fthr.grid(row=1, column=1)
    pma.grid(row=2, column=1)
    age.grid(row=3, column=1)
    imc.grid(row=4, column=1)
    profile=IntVar()
    Label(root, text="Profil", bg="white").grid(row=5, column=1)
    Label(root, bg='white', fg='black', width=20, text='Plutot rouleur').grid(row=6, column=0)
    Label(root, bg='white', fg='black', width=20, text='Plutot puncheur').grid(row=6, column=2)
    sl=Scale(root, from_=0, to=10, orient=HORIZONTAL, length=200, resolution=1, showvalue=0)
    sl.grid(row=6, column=1)
    Button(root, text="Submit", command=lambda: start1(ftp.get(), fthr.get(), pma.get(), age.get(), imc.get(), sl.get(),device.get())).grid(row=7, column=1)
    root.mainloop()


def start1(ftp, fthr, pma, age, imc, profile, device):
    """this function adds the data to a csv file"""
    with open("auto.csv", "a") as file:
        file.write(f"{ftp},{fthr},{pma},{age},{imc},{profile},{device}\n")
    device=device.split(" ")[0][0:len(device.split(" ")[0])-1]
    cyclist=Cyclist(ftp, fthr, pma, age, imc, profile, 100, 100,device)
    start(cyclist)  


def function_chooser(cyclist):
    if cyclist.profile<5:
        return ("rouleur",5-cyclist.profile)
    if cyclist.profile==5:
        return ("polyvalent",0)
    if cyclist.profile>5:
        return ("puncheur",cyclist.profile-5)
    



async def run(address, cyclist):
    print("11111111111")

    async with BleakClient(address) as client:
        def my_measurement_handler(data):
            print(data[0])
            cyclist.update_bj()
            cyclist.update_br()
            f = open("tmp_power.txt", "a")
            f.write(","+str(data[0]))
            f.close()

        await client.is_connected()
        print("22222222222")
        trainer = CyclingPowerService(client)
        print("3333333333333")

        trainer.set_cycling_power_measurement_handler(my_measurement_handler)
        print("444444444444")

        
        await trainer.enable_cycling_power_measurement_notifications()
        await asyncio.sleep(300.0)
        await trainer.disable_cycling_power_measurement_notifications()



def start_ble(cyclist):
    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    device_address = cyclist.device
    global status
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError as e:
        if str(e).startswith('There is no current event loop in thread'):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        else:
            raise

    try:
        print("000000")
        loop.run_until_complete(run(device_address,cyclist))
    except RuntimeError as e:
        status.config(text="Device Error : "+str(e))
        return

# creating the dataset
def update(i, cyclist):
    y=cyclist.bj
    r=cyclist.br
    p=get_power()

    data1 = {'yellow':y}
    courses1 = list(data1.keys())
    values1 = list(data1.values())

    data2 = {'red':r}
    courses2 = list(data2.keys())
    values2 = list(data2.values())
    
    
    # creating the bar plot
    plt.clf()


    data11 = {'yellow':100-y}

    courses11 = list(data11.keys())
    values11 = list(data11.values())


    data12 = {'red':100-r}
    courses12 = list(data12.keys())
    values12 = list(data12.values())
   
    plt.bar(courses1, values1, color ='gold',
            width = 0.5)
        
    plt.bar(courses2, values2, color ='brown',
            width = 0.5)

    plt.bar(courses11, values11, bottom=values1, color='grey',
            width = 0.5)

    plt.bar(courses12, values12, bottom=values2, color='grey',
            width = 0.5)
    
    plt.xlabel("Energy bars")
    plt.ylabel("Value")
    plt.title("Power = "+str(p)+" W")
    plt.yticks(np.arange(0, 101, 10))

def start_vizu(cyclist,):
    fig = plt.figure(figsize = (5, 5))
    ani = animation.FuncAnimation(fig, update, interval=1000 ,fargs=(cyclist,))
    plt.show()



def start(cyclist):
    th1=threading.Thread(target=start_vizu,args=(cyclist,))
    th2=threading.Thread(target=start_ble,args=(cyclist,))

    th1.start()
    th2.start()

    th1.join()
    # exit th2
    os._exit(1)

def main():

    f = open("tmp_power.txt", "w")
    f.write("0")
    f.close()

    gui()
    print("Program terminated")


if __name__ == "__main__":
    main()