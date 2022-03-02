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

class Servidor:
    def __init__(self):
        self.IP_ADDRESS='0.0.0.0'
        self.PORT_ADDRESS=9999
        self.SERVER_ADDRESS=(self.IP_ADDRESS, self.PORT_ADDRESS)
        self.fecha=str(date.today().day)+'/'+str(date.today().month)+'/'+str(date.today().year)
        self.hora=str(datetime.now().hour)+':'+str(datetime.now().minute)

class DataPico:
    def __init__(self):
        self.temp_array=[]
        self.temp_mcu_array=[]
        self.pulse_array=[]
        self.x_acel_array=[]
        self.y_acel_array=[]
        self.z_acel_array=[]

server=Servidor()
socketTCP=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketTCP.bind(server.SERVER_ADDRESS)
socketTCP.listen(2)
solicitud = ''
print('Servidor escuchando en el puerto: ' + str(server.PORT_ADDRESS))
conexion, CLIENT_ADDRESS = socketTCP.accept()

data_pico_saved=DataPico()

while True:
    solicitud=''
    # ____________________________________________________________________________________
    #| Esto de aqui abajo era el problema, cada vez que intentaba volver a conectarse se  |
    #| bloqueaba el socket.                                                               |
    # -------------------------------------------------------------------------------------
    #print('Servidor escuchando en el puerto: '+str(server.PORT_ADDRESS))
    #conexion, CLIENT_ADDRESS=socketTCP.accept()
    solicitud=conexion.recv(400)
    print(solicitud)
    data_from_pico=solicitud.decode()
    #print(data_from_pico)
    #data_json=json.loads(data_from_pico)
    #print('RECIBOO:'+str(data_from_pico))
    #data_pico_saved.temp_array[counter]=data_json["Temp"]
    #print(data_pico_saved)
    #print('Temperature: '+data_json["Temp"]+"ºC")
    #print('Temperature from mcu: '+data_json["TempMcu"]+"ºC")
    #print('Pulse signal: ' + data_json["PulseSig"] + " Volts")
    #print('Acelerometer: (' + data_json["Acel_x"] + ","+data_json["Acel_y"]+","+data_json["Acel_z"]+")")
    if "{" in data_from_pico:
        data_json=json.loads(data_from_pico)
        print('RECIBOO:'+str(data_from_pico))
        data_pico_saved.temp_array.append(data_json["Temp"])
        data_pico_saved.temp_mcu_array.append(data_json["TempMcu"])
        data_pico_saved.pulse_array.append(data_json["PulseSig"])
        data_pico_saved.x_acel_array.append(data_json["Acel_x"])
        data_pico_saved.y_acel_array.append(data_json["Acel_y"])
        data_pico_saved.z_acel_array.append(data_json["Acel_z"])
        print("Temp:")
        print(data_pico_saved.temp_array)
        print("temp_mcu:")
        print(data_pico_saved.temp_mcu_array)
        print("pulse:")
        print(data_pico_saved.pulse_array)
        print("x_accel:")
        print(data_pico_saved.x_acel_array)
        print("y_accel:")
        print(data_pico_saved.y_acel_array)
        print("z_accel:")
        print(data_pico_saved.z_acel_array)
        #print('Temperature: '+data_json["Temp"]+"ºC")
        #print('Temperature from mcu: '+data_json["TempMcu"]+"ºC")
        #print('Pulse signal: ' + data_json["PulseSig"] + " Volts")
        #print('Acelerometer: (' + data_json["Acel_x"] + ","+data_json["Acel_y"]+","+data_json["Acel_z"]+")")
