# This is a sample Python script.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
#def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
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

plt.style.use('seaborn-notebook')
x_data = []
y_data = []

x_data1 = []
y_data1 = []

figure1 = pyplot.figure(1)
line, = pyplot.plot(x_data, y_data, '-')
figure2 = pyplot.figure(2)
line1, = pyplot.plot(x_data1, y_data1, '-')

def graph_temp(frame):
    if len(x_data)>10:
        x_data.pop(0)
        y_data.pop(0)
    print('frame:'+str(frame)+', temp_array_y:'+str(data_pico_saved.temp_array_y))
    print("\n")
    x_data.append(frame)
    y_data.append(float(data_pico_saved.temp_array_y[(len(data_pico_saved.temp_array_y)-1)]))
    line.set_data(x_data, y_data)
    figure1.gca().relim()
    figure1.gca().autoscale_view()
    return line,

def graph_temp_mcu(frame):
    if len(x_data1)>10:
        x_data1.pop(0)
        y_data1.pop(0)
    x_data1.append(frame)
    y_data1.append(float(data_pico_saved.temp_mcu_array_y[(len(data_pico_saved.temp_array_y)-1)]))
    line1.set_data(x_data1, y_data1)
    figure2.gca().relim()
    figure2.gca().autoscale_view()
    return line1,

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

animacion4 = FuncAnimation(figure2, graph_temp_mcu, interval=1000)
animacion3 = FuncAnimation(figure1, graph_temp, interval=1000)
pyplot.show()