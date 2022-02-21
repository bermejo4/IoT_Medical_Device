
import utime
from machine import Pin, ADC, Signal
import uos
#import utime
import rp2
from rp2 import PIO, asm_pio
#from machine import Pin
from time import sleep
import onewire
from ds18x20 import DS18X20
import binascii

def sendCMD_waitResp(cmd, uart=machine.UART(0, baudrate=115200), timeout=2000):
    print("CMD: " + cmd)
    uart.write(cmd)
    waitResp(uart, timeout)
    print()
    
def waitResp(uart=machine.UART(0, baudrate=115200), timeout=2000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print("resp:")
    try:
        print(resp.decode())
    except UnicodeError:
        print(resp)
        
# send CMD to uart,
# wait and show response without return
def sendCMD_waitAndShow(cmd, uart=machine.UART(0, baudrate=115200)):
    print("CMD: " + cmd)
    uart.write(cmd)
    while True:
        print(uart.readline())
        
def espSend(text="test", uart=machine.UART(0, baudrate=115200)):
    sendCMD_waitResp('AT+CIPSEND=' + str(len(text)) + '\r\n')
    sendCMD_waitResp(text)


        
def pulse_sensor():
    #pulse_sensor = Pin(26, Pin.IN, Pin.PULL_UP)        # Pulse Sensor PURPLE WIRE connected to ANALOG PIN 0
    #LED_on_board = machine.Pin(25, machine.Pin.OUT)
    #signal=machine.ADC(pulse_sensor) # holds the incoming raw data. Signal value can range from 0-1024
    #signal.atten(machine.ADC.ATTN_11DB)
    pulse_sensor=machine.ADC(2)
    conversion_factor = 3.3 / (65535)
    
    
    while True:
      signal_value = pulse_sensor.read_u16()*conversion_factor
    
      print(signal_value)
      utime.sleep(0.05)
      

def temperature2():
    ow = onewire.OneWire(Pin(14)) #Prepara GPIO4 para usar con OneWire
    sensor = DS18X20(ow) #define un sensor en ese pin
    direcciones = sensor.scan()  #Lee el ID del sensor conectado
    id=direcciones[0]
    #Pasa el ID a formato de texto e imprime
    idHex = binascii.hexlify(bytearray(id))
    print ("ID=",idHex)
    #Lee e imprime la temperatura cada 1 segundo
    while (True):
        sensor.convert_temp ()
        sleep (1)
        temperatura = sensor.read_temp (id)
        print (temperatura)

def temperature():
    ds_pin = machine.Pin(16)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    roms = ds_sensor.scan()
    print('Found DS devices: ', roms)
    while True:
        ds_sensor.convert_temp()
        utime.sleep_ms(750)
        for rom in roms:
            print(rom)
            print(ds_sensor.read_temp(rom))
        utime.sleep(1)
        
def ad8232():
    ecg_pin_output=machine.ADC(0)
    lo_plus=machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP).value()
    lo_minus=machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP).value()
    
    while True:
        #print('lo+: '+str(lo_plus))
        #if lo_plus==1 or lo_minus==1:
           # print("!")
       # else:
        signal_value_ecg = ecg_pin_output.read_u16()
        if signal_value_ecg>64000 and signal_value_ecg<65000:
            if signal_value_ecg>64500 and signal_value_ecg<65000:
                print(signal_value_ecg)
                utime.sleep(0.04)
            else:
                print(signal_value_ecg)
                utime.sleep(0.04)
                

        
if __name__ == "__main__":
#    from machine import Pin
#     from DHT22 import DHT22
#    import utime
    #dht_data = Pin(15,Pin.IN,Pin.PULL_UP)
    #dht_sensor=DHT22(dht_data,Pin(14,Pin.OUT),dht11=True)

    #--------------
    #pulse_sensor()
    #--------------
    #temperature2()
    #--------------
    ad8232()
    #--------------
    
    server_ip="192.168.23.227"
    server_port=9999

    print()
    print("Machine: \t" + uos.uname()[4])
    print("MicroPython: \t" + uos.uname()[3])

    #indicate program started visually
    led_onboard = machine.Pin(25, machine.Pin.OUT)
    led_onboard.value(0)     # onboard LED OFF/ON for 0.5/1.0 sec
    utime.sleep(0.5)
    led_onboard.value(1)
    utime.sleep(1.0)
    led_onboard.value(0)

    uart0 = machine.UART(0, baudrate=115200)
    print(uart0)
    
    sendCMD_waitResp('AT\r\n')          #Test AT startup
    sendCMD_waitResp('AT+CWLAP\r\n', timeout=10000) #List available APs
    sendCMD_waitResp('AT+CWJAP="Rivendel","jeronimo"\r\n', timeout=5000) #Connect to AP
    sendCMD_waitResp('AT+CIFSR\r\n')    #Obtain the Local IP Address
    #sendCMD_waitResp('AT+CIPSTART="TCP","192.168.12.147",9999\r\n')
    sendCMD_waitResp('AT+CIPSTART="TCP","' +
                 server_ip +
                 '",' +
                 str(server_port) +
                 '\r\n')
    espSend()
    
    
    while True:
        T,H = dht_sensor.read()
        if T is None:
            print(" sensor error")
        else:
            print("{:3.1f}'C  {:3.1f}%".format(T,H))
            cadena="{"+"\"T\":\""+str(T)+"\","+"\"H\":\""+str(H)+"\"}"
        #DHT22 not responsive if delay to short
        utime.sleep_ms(500)
        #print('Enter something:')
        #msg = input()
        #sendCMD_waitResp('AT+CIPSTART="TCP","192.168.12.147",9999\r\n')
        sendCMD_waitResp('AT+CIPSTART="TCP","' +
                     server_ip +
                     '",' +
                     str(server_port) +
                     '\r\n')
        espSend(cadena)