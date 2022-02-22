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

class Servidor:

    def __init__(self):
        self.IP_ADDRESS='0.0.0.0'
        self.PORT_ADDRESS=9999
        self.SERVER_ADDRESS=(self.IP_ADDRESS, self.PORT_ADDRESS)
        self.fecha=str(date.today().day)+'/'+str(date.today().month)+'/'+str(date.today().year)
        self.hora=str(datetime.now().hour)+':'+str(datetime.now().minute)

server=Servidor()
socketTCP=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketTCP.bind(server.SERVER_ADDRESS)
socketTCP.listen(2)

solicitud = ''
print('Servidor escuchando en el puerto: ' + str(server.PORT_ADDRESS))
conexion, CLIENT_ADDRESS = socketTCP.accept()

while True:
    solicitud=''
    # ____________________________________________________________________________________
    #| Esto de aqui abajo era el problema, cada vez que intentaba volver a conectarse se  |
    #| bloqueaba el socket.                                                               |
    # -------------------------------------------------------------------------------------
    #print('Servidor escuchando en el puerto: '+str(server.PORT_ADDRESS))
    #conexion, CLIENT_ADDRESS=socketTCP.accept()
    solicitud=conexion.recv(20)
    data_from_pico=solicitud.decode()
    data_json=json.loads(data_from_pico)
    print('RECIBOO:'+str(data_from_pico))

    print('Temperature: '+data_json["Temp"]+"ºC")
    print('Temperature from mcu: '+data_json["TempMcu"]+"ºC")
    print('Pulse signal: ' + data_json["PulseSig"] + " Volts")
    print('Acelerometer: (' + data_json["Acel_x"] + ","+data_json["Acel_y"]+","+data_json["Acel_z"]+")")


    #if solicitud.decode()=='FECHA':
        #print('He recibido FECHA')
        #print('Voy a enviar: '+str(server.fecha))
        #conexion.sendall(server.fecha.encode('utf8'))
    #elif solicitud.decode()=='HORA':
        #print('He recibido HORA')
        #print('Voy a enviar: '+str(server.hora))
        #conexion.sendall(server.hora.encode('utf8'))
    #else:
        #print('ERROR')
        #conexion.sendall('ERROR'.encode('utf8'))
