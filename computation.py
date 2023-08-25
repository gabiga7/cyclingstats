import os
import re
import sys
import numpy as np
import matplotlib.pyplot as plt

def get_extension(filename):
    """Get the file extension from the filename."""
    return os.path.splitext(filename)[1]

def get_power_list(filename):
    """Extract power data from a given file based on its extension."""
    extension = get_extension(filename)
    pattern = {
        '.tcx': r'\s+<ns3:Watts>(\d+.\d+)',
        '.gpx': r'\s+<power>(\d+.\d+)'
    }.get(extension, None)

    if not pattern:
        sys.exit("Invalid file extension. Please provide either .gpx or .tcx file.")

    power_list = []
    with open(filename, 'rt') as f:
        for line in f:
            match = re.match(pattern, line)
            if match:
                power_list.append(float(match.group(1)))

    return power_list

def readable_power_data(data):
    """Convert raw power data to a more readable form."""
    return [sum(data[i:i+60])/60 for i in range(0, len(data), 60)]

def create_line(array, line_type):
    """Plot a line with given data and line type."""
    plt.plot(array, "-b", color=line_type, linewidth=2)
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




def main():
    # Check command line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: script_name.py <path_to_gpx_or_tcx_file>")

    # Extract power data from the file
    gpx = get_power_list(sys.argv[1])

    energie_bj, energie_br = 100, 100
    histo_bj, histo_br = [], []

    for power in gpx:
        energie_bj = ajustement_energie_bj(energie_bj, depense_puissance_duree_bj(ftp=277, puissance=power, temps=1))
        energie_br = ajustement_energie_br(energie_br, depense_puissance_duree_br(ftp=277, puissance=power, temps=1))
        histo_bj.append(energie_bj)
        histo_br.append(energie_br)

    print("Computations ok, graphics in preparation.")
    main_plot(gpx, histo_bj, histo_br)

if __name__ == "__main__":
    main()
