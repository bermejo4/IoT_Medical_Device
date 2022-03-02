# This is a sample Python script.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
#def print_hi(name):
    # Use a breakpoint in the code line_temp below to debug your script.
    #print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
    #print_hi('PyCharm')
import socket
import sys
import threading
from datetime import date
from datetime import datetime
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as animation
import matplotlib; matplotlib.use("TkAgg")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation

class Servidor:
    def __init__(self):
        self.IP_ADDRESS='0.0.0.0'
        self.PORT_ADDRESS=9999
        self.SERVER_ADDRESS=(self.IP_ADDRESS, self.PORT_ADDRESS)
        self.fecha=str(date.today().day)+'/'+str(date.today().month)+'/'+str(date.today().year)
        self.hora=str(datetime.now().hour)+':'+str(datetime.now().minute)

class DataPico:
    def __init__(self):
        self.temp_array_y = []
        self.temp_array_x = []
        self.temp_mcu_array_y = []
        self.temp_mcu_array_x = []
        self.pulse_array_y=[]
        self.pulse_array_x = []
        self.x_acel_array_y=[]
        self.x_acel_array_x = []
        self.y_acel_array_y=[]
        self.y_acel_array_x=[]
        self.z_acel_array_y=[]
        self.z_acel_array_x = []

server=Servidor()
socketTCP=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketTCP.bind(server.SERVER_ADDRESS)
socketTCP.listen(2)
solicitud = ''
print('Servidor escuchando en el puerto: ' + str(server.PORT_ADDRESS))
conexion, CLIENT_ADDRESS = socketTCP.accept()

data_pico_saved=DataPico()
data_pico_saved.temp_array_y.append(20)
data_pico_saved.temp_mcu_array_y.append(20)
data_pico_saved.pulse_array_y.append(0)

plt.style.use('seaborn-notebook')
x_data_temp_plot = []
y_data_temp_plot = []

x_data_temp_mcu_plot = []
y_data_temp_mcu_plot = []

x_data_pulse_plot = []
y_data_pulse_plot = []

x_data_x_accel_plot = []
y_data_x_accel_plot = []

x_data_y_accel_plot = []
y_data_y_accel_plot = []

x_data_z_accel_plot = []
y_data_z_accel_plot = []

#Figure of Temperature:
figure_temp = pyplot.figure(1, figsize=(12,2))
figure_temp.suptitle('Temperature', fontsize=10)
figure_temp.canvas.manager.set_window_title('Temperature from sensor')
line_temp,= pyplot.plot(x_data_temp_plot, y_data_temp_plot, '-', color='orange')
#Figure of MCU Temperature:
figure_temp_mcu = pyplot.figure(2, figsize=(12,2))
figure_temp.canvas.manager.set_window_title('MCU Temperature')
figure_temp_mcu.suptitle('Temperature of the MCU RP2040')
line_temp_mcu, = pyplot.plot(x_data_temp_mcu_plot, y_data_temp_mcu_plot, '-', color='red')
#Figure of Pulse:
figure_pulse = pyplot.figure(3, figsize=(12,2))
figure_pulse.canvas.manager.set_window_title('Pulse')
figure_pulse.suptitle('Pulse signal from pulse sensor')
line_pulse, = pyplot.plot(x_data_pulse_plot, y_data_pulse_plot, '-', color='green')
#Figure of X component of the accelerometer:
figure_x_accel = pyplot.figure(4, figsize=(4,2))
line_x_accel, = pyplot.plot(x_data_x_accel_plot, y_data_x_accel_plot, '-')
#Figure of Y component of the accelerometer:
figure_y_accel = pyplot.figure(5, figsize=(4,2))
line_y_accel, = pyplot.plot(x_data_y_accel_plot, y_data_y_accel_plot, '-')
#Figure of Z component of the accelerometer:
figure_z_accel = pyplot.figure(6, figsize=(4,2))
line_z_accel, = pyplot.plot(x_data_z_accel_plot, y_data_z_accel_plot, '-')

def graph_temp(frame):
    if len(x_data_temp_plot)>10:
        x_data_temp_plot.pop(0)
        y_data_temp_plot.pop(0)
    x_data_temp_plot.append(frame)
    y_data_temp_plot.append(float(data_pico_saved.temp_array_y[(len(data_pico_saved.temp_array_y) - 1)]))
    line_temp.set_data(x_data_temp_plot, y_data_temp_plot)
    figure_temp.gca().relim()
    figure_temp.gca().autoscale_view()
    return line_temp,

def graph_temp_mcu(frame):
    if len(x_data_temp_mcu_plot)>10:
        x_data_temp_mcu_plot.pop(0)
        y_data_temp_mcu_plot.pop(0)
    x_data_temp_mcu_plot.append(frame)
    y_data_temp_mcu_plot.append(float(data_pico_saved.temp_mcu_array_y[(len(data_pico_saved.temp_array_y) - 1)]))
    line_temp_mcu.set_data(x_data_temp_mcu_plot, y_data_temp_mcu_plot)
    figure_temp_mcu.gca().relim()
    figure_temp_mcu.gca().autoscale_view()
    return line_temp_mcu,

def graph_pulse(frame):
    if len(x_data_pulse_plot)>10:
        x_data_pulse_plot.pop(0)
        y_data_pulse_plot.pop(0)
    x_data_pulse_plot.append(frame)
    y_data_pulse_plot.append(float(data_pico_saved.pulse_array_y[(len(data_pico_saved.pulse_array_y) - 1)]))
    line_temp.set_data(x_data_pulse_plot, y_data_pulse_plot)
    figure_pulse.gca().relim()
    figure_pulse.gca().autoscale_view()
    return line_pulse,


def collector():
    while True:
        solicitud = ''
        # ____________________________________________________________________________________
        # | Esto de aqui abajo era el problema, cada vez que intentaba volver a conectarse se  |
        # | bloqueaba el socket.                                                               |
        # -------------------------------------------------------------------------------------
        # print('Servidor escuchando en el puerto: '+str(server.PORT_ADDRESS))
        # conexion, CLIENT_ADDRESS=socketTCP.accept()
        solicitud = conexion.recv(400)
        print("solicitud:" + str(solicitud))
        print("\n")
        data_from_pico = solicitud.decode()
        # print(data_from_pico)
        # data_json=json.loads(data_from_pico)
        # print('RECIBOO:'+str(data_from_pico))
        # data_pico_saved.temp_array[counter]=data_json["Temp"]
        # print(data_pico_saved)
        # print('Temperature: '+data_json["Temp"]+"ºC")
        # print('Temperature from mcu: '+data_json["TempMcu"]+"ºC")
        # print('Pulse signal: ' + data_json["PulseSig"] + " Volts")
        # print('Acelerometer: (' + data_json["Acel_x"] + ","+data_json["Acel_y"]+","+data_json["Acel_z"]+")")
        if "{" in data_from_pico:
            data_json = json.loads(data_from_pico)
            print('RECIBOO:' + str(data_from_pico))
            data_pico_saved.temp_array_y.append(float(data_json["Temp"]))
            data_pico_saved.temp_mcu_array_y.append(float(data_json["TempMcu"]))
            data_pico_saved.pulse_array_y.append(float(data_json["PulseSig"]))
            data_pico_saved.x_acel_array_y.append(float(data_json["Acel_x"]))
            data_pico_saved.y_acel_array_y.append(float(data_json["Acel_y"]))
            data_pico_saved.z_acel_array_y.append(float(data_json["Acel_z"]))
            print("\n")
            print("Temp:")
            print(data_pico_saved.temp_array_y)
            print("temp_mcu:")
            print(data_pico_saved.temp_mcu_array_y)
            print("pulse:")
            print(data_pico_saved.pulse_array_y)
            print("x_accel:")
            print(data_pico_saved.x_acel_array_y)
            print("y_accel:")
            print(data_pico_saved.y_acel_array_y)
            print("z_accel:")
            print(data_pico_saved.z_acel_array_y)
            # print('Temperature: '+data_json["Temp"]+"ºC")
            # print('Temperature from mcu: '+data_json["TempMcu"]+"ºC")
            # print('Pulse signal: ' + data_json["PulseSig"] + " Volts")
            # print('Acelerometer: (' + data_json["Acel_x"] + ","+data_json["Acel_y"]+","+data_json["Acel_z"]+")")

collecting_data=threading.Thread(target=collector)
collecting_data.start()

temp_mcu_plot = FuncAnimation(figure_temp_mcu, graph_temp_mcu, interval=1000)
temp_plot = FuncAnimation(figure_temp, graph_temp, interval=1000)
pulse_plot=FuncAnimation(figure_pulse, graph_pulse, interval=1000)
pyplot.show()