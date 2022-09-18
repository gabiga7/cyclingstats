import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure(figsize = (5, 5))


def get_last_data_yellow():
    graph_data = open('tmp_bj.txt','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
    return (xs[-1],ys[-1])

def get_last_data_red():
    graph_data = open('tmp_br.txt','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
    return (xs[-1],ys[-1])

# creating the dataset
def update(i):
    y=get_last_data_yellow()[1]
    r=get_last_data_red()[1]

    data1 = {'yellow':y}
    courses1 = list(data1.keys())
    values1 = list(data1.values())

    data2 = {'red':r}
    courses2 = list(data2.keys())
    values2 = list(data2.values())
    
    
    # creating the bar plot
    plt.bar(courses1, values1, color ='gold',
            width = 0.5)
        
    plt.bar(courses2, values2, color ='brown',
            width = 0.5)
    
    plt.xlabel("Energy bars")
    plt.ylabel("Value")
    plt.title("Energy bars value")


ani = animation.FuncAnimation(fig, update, interval=1000)
plt.show()