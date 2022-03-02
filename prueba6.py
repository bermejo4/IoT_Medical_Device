import random

import matplotlib.pyplot as plt
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
from random import randrange

plt.style.use('seaborn-notebook')
x_data = []
y_data = []

x_data1 = []
y_data1 = []

figure1 = pyplot.figure(1)
line, = pyplot.plot(x_data, y_data, '-')
figure2 = pyplot.figure(2)
line1, = pyplot.plot(x_data1, y_data1, '-')

def grafica3(frame):
    # asfasdfasfaf
    # asfasfasf
    # temperatura
    #print(frame)
    if len(x_data)>10:
        x_data.pop(0)
        y_data.pop(0)
    x_data.append(frame)
    y_data.append(int(input()))
    #y_data_temp_plot.append(randrange(0, 100))
    line.set_data(x_data, y_data)
    figure1.gca().relim()
    figure1.gca().autoscale_view()
    return line,

def grafica2(frame):
    # asfasdfasfaf
    # asfasfasf
    # temperatura
    #print(frame)
    if len(x_data)>10:
        x_data1.pop(0)
        y_data1.pop(0)
    x_data1.append(frame)
    y_data1.append(randrange(0, 100))
    #y_data_temp_plot.append(randrange(0, 100))
    line1.set_data(x_data1, y_data1)
    figure2.gca().relim()
    figure2.gca().autoscale_view()
    return line1,


animacion4 = FuncAnimation(figure2, grafica2, interval=1000)
animacion3 = FuncAnimation(figure1, grafica3, interval=1000)
pyplot.show()