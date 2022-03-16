# Paper:
## Development of a medical monitoring system based on the internet of things

[posibles títulos]:
Desarrollo de un sistema de monitorización médica basado en internet de las cosas. 

-------
### Introduction:

The Internet of Things (IoT) term refers to the collective network of connected devices and the technology that facilitates communication between devices and the cloud, as well as between the devices themselves [1]. Nowadays everything is connected to the Internet from a computer or server to a fridge or a house, going through different industries and work environments to places of leisure or our own homes. In [2], Cisco, one of the huge networks company in the world, says that according to their analysis, IoT devices will account for 50 percent (14.7 billion) of all global networked devices by 2023. 

There is no doubt that this technology is growing unstoppably and everyday more companies and sectors incorporate it. One of the industries that will have to face this change will be the medical instrumentation industry to connect all its medical devices to the Internet, which, whatever their function, are ultimately intended to obtain very useful physiological data for later analysis and according to them an adequate decision making.

There are abundance of propietary IoT healthcare platforms nowadays, for example, Apple Watch Series 3 [3] combined with "Health" App [4] can overwatch the ECG, the oximetry, steps or sleep. And the same its competitors like Samsung (Samsung Galaxy Watch 4 and "Samsung Health" App). But these systems and devices are very expensive together, with prices above 1000$, if you thing about smartwathes can't work propertly without a smartphone. In many cases, these products are not scalable or modifiable because don't provide open-source software or hardware features.

Also there are specialized healthcare monitoring IoT hardware platforms like Mysignals [5], property of Libelium, a IoT dedicated company. This product based on arduino can collect a lot of physiological signals from sensors like Temperature, glucometer, ECG, EMG, SP02... And all open source, so it is more scalable than previous ones, or it was, because today MySignals is no longer available.

In the work [6] authors cover the posible design of efficient medical IoT sensor nodes in terms of low-cost, low power-consumption, and increased data accuracy based on open-source platforms. It is performed with a Arduino Uno attached to a Raspberry Pi, but the cost of this elements (together more than 60$ nowadays) is still high compared to my proporsal. And in [7] they create a generic clothing technology to measure SPO2, electro dermal activity, and body temperature implemented with a Arduino Lily-pad, although they don't send data through a wireless model, ideed it's one of their future enhancement. A wearable sensor-based human physical activity recognition is shown in the article [8] using MetaMotion Metawear as a sensor [9] and connecting it through bluetooth to a smart-phone to send the data over the Internet to a Web Server. The problem with this is that two connections must be established as opposed to a single connection in my proposed model, and with each connection the probabilities of failures increase, so the architecture can be minimized using only one device, to transfer data to the cloud.

Within the context discussed above, this article tackle the next objectives, apart from the design of an IoT platform to monitorize patients in real time:
- First, a wearable small size device with a wireless connection to transmit the data collected from its sensors, focusing in a TCP/IP model to that purpose.
- Second, a low cost system, less than 18$, using components easy to buy nowadays in the Internet and cheap comparated with others actual models.
- Third, a scalable IoT project. It is used for a medical purpose, with 3 main sensors, but some others could replace them or be added depending on pins availables and the protocol connection used for medical field too or for other that we want, or ideed combined them, with only a few changes. 




~~It is expected that in the future most everyday objects will be connected to the Internet, for this the global industry will have to face the challenge of developing millions of devices that can connect to the Internet in an efficient way.~~

~~Many of the industries until now were only specialized in the creation of their product but now, in most cases, they must face the development and incorporation of a technology unknown to them that consists of the connectivity of their devices to the Internet, and for this they will have to allocate resources and money to this work, from specialized personnel to the purchase of material such as microcontrollers or network modules.~~

Today, thanks to advances in technology, it is possible to manufacture small IoT devices with ease because the size of the chips with which the network modules are manufactured are only a few centimeters in size and the cost is less than $2 per module, therefore manufacturing from scratch, or transforming a normal object into an IoT one, is quite affordable, making this new sector of technology grow unstoppably.

~~One of the industries that will have to face this change will be the medical instrumentation industry to connect all its medical devices to the Internet, which, whatever their function, are ultimately intended to obtain very useful physiological data for later analysis and according to them an adequate decision making.~~

There are some reasons about why is interesant to send data that are generated or collected by medical devices over the Internet. One of them is because many of the medical devices are usually small in size and to store all the data they collect they would need a memory built into the device, although the dimensions of the memory would not be much of a problem, the additional cost of this would be, depending on its capacity, and the subsequent inconvenience of having to dump all the data to a software running on a computer or server, therefore, moving to one of the following reasons, the data would not be seen in real time. Something that allows the Internet of Things is to monitor in real time, since the information as it is obtained is sent to the Internet instantly.
Regarding the issue of storage, thanks to the internet of things, we do not have to worry about having a memory in our device, since we can have a remote database, to which, thanks to the internet, we are sending all the data taken by our medical system.

Until now, the Internet of Things has only been discussed as a channel of reading and sending data, "monitoring", but the direction can be changed, and an external host, over the Internet of Things, can make responses accordingly to that data, and send it to our devices. It is true that if the device has a programmable microcontroller, these responses could be programmed without the need to incorporate the Internet of Things, but let's think bigger, let's think about how this device could be connected, for example, to an artificial intelligence located in a remote server or to a doctor, and that could offer answers according to a data pattern, for example the pulse of a person and a possible attack.

------- 
### Proporsal-platform system:
As mentioned before, with today’s technology it is quite simple to develop a system based on the Internet of Things. With this in mind I have developed a low cost system based on the internet of things and whose main function is to monitor the temperature, pulse and movements of a patient; and send it all to an external server where it will be represented graphically for the future supervision of a professional or an artificial intelligence. 
We can distinguish several phases that comprise in the operation of the system:

1. Sensorization:  A sensor is a device that produces an output signal from a physical phenomenon perceived. One of the purposes of IoT is to transform all the real world phenomena into digital data to understand the world from a different point of view and for this task sensors are indispensable, helping humanity to perceive phenomena that sometimes they can not perceive on their on. 
We can distinguish two classes of sensor in IoT; one is external sensor that helps the IoT device to develop its function, and the other is internal sensor that helps the IoT device to control how is everything about itself to care that it can develop its function without problems, and very often one kind of sensor is as important as the other.
This device works with the following sensors:
    - 3 external sensors:
        - Temperature sensor. 
        - Pulse sensor.
        - Accelerometer.
    - 1 internal sensor:
        - Internal mcu temperature.
     
2. Data Collection:
The sensors send all physics phenomena which collect to a microcontroller in form of anolog signal (many of the physiological signals are signals of this kind), that sample and cuantificate  

The sensors send all the physical phenomenona which have been collected to a microcontroller in the form of an analog signal (the majority of physiological signals are signals of this type) that will be responsible for sampling and quantifying (assign numerical values to the input signal) to transform it into manageable digital data. In some cases the signal already comes digitalized from the sensors, in this case the microcontroller only has to collect it following the communication protocol used by the sensor in question.(SPI, I2C, UART, or one of its own).

{Los sensores envían todos los fenomenos físicos que recopilan a un microcontrolador en forma de señal analógica (la gran mayoría de las señales fisiológicas son señales de este tipo) que se encargará de muestrear y cuantificar (asignar valores numéricos a la señal que llega) para así transformarla en datos digitales manejables. En algunos casos la señal ya viene de los sensores digitalizada, en este caso el microcontrolador solo tiene que recogerla siguiendo el protocolo de comunicación que utilice el sensor en cuestión.(SPI, I2C, UART, o uno propio)}

3. Formatting and Transfer.
Once the microcontroller has the data for a specific time, it must prepare them for shipment. It is important to detail a format for the shipment that is distinguishable later in the reception, clearly marking the distinction between data collected from different sensors. For this I chose to send them formatted by JSON, a text format for sending data, widely used, easy to handle both at source and destination.
The TCP/IP communication model is used to transfer the data.

{Una vez que el microcontrolador ya dispone de los datos correspondientes a un tiempo concreto, los debe preparar para el envío. Es importante detallar un formato para el envío que sea distinguible posteriormente en la recepción, marcando claramente la distinción entre datos recopilados de sensores diferentes. Para ello opté por enviarlos formateados mediante JSON, un formato de texto para el envío de datos ampliamente utilizado, fácil de manejar tanto en el origen como en el destino.
Para transferir los datos se utiliza el modelo de comunicación de redes TCP/IP. }

4. Reception and Decision making.

At the destination the data is unformat and stored depending on the sensor to which they belong, and depending, if there is more than one, on the microcontroller from where they come. Subsequently, these data can be represented in many ways, using an array, a graph... To facilitate the final work, which will be decision making. Depending on what the data set means, a decision will be made according to them, either by a medical entity or by an artificial intelligence


{En el destino los datos son desformateados y almacenados dependiendo del sensor al que pertenezcan, y dependiendo, si hubiera más de uno, del microcontrolador de donde provengan. Posteriormente esos datos se pueden representar de muchas maneras, mediante un array, una gráfica... Para facilitar así la labor final, que será la toma de decisión. Dependiendo de lo que signifique el conjunto de los datos se tomará una decisión acorde a ellos, ya sea por parte de una entidad médica o por una inteligencia artificial}

-------
### Implementation & configuration:
Materials and connections.
- Temperature Sensor: to measure the temperature I use a sensor called ds18b20 connected to the microcontroler throught a resistence of 4,7 kOhms to the pin gpio X of the Raspberry Pi Pico. (Figure 2.1)
- Pulse Sensor: to obtain the pulse signal I use a module without a specific name connected directly to the pin gpio X of the Raspberry Pi Pico. It sends an analogical signal to it.(Figure 2.2)
- Accelerometer: To obtain the movements of the patient I use a accelerometer called mpu5060. It uses a I2C communication protocol so it needs two i2c pins. The Slave Data Address pin (SDA) is connected to the pin X, and the Slave Clock pin (SCL) is connected to the pin X.

- Microcontroler: Raspberry Pi Pico: this is the brain of the hole system. 
- Wi-Fi Module: esp8266.


-------
### Test and Results:

-------
### Conclusion & Future Improvements.

-------  






-------
-------
## Paper español:

#### Intro:


{Se prevee que en un futuro la mayoría de los objetos cotidianos estén conectados a internet, para ello la industria global deberá afrontar el reto de desarrollar millones de dispositivos que puedan conectarse a internet de una forma eficaz. 

Muchas de las industrias hasta el momento solo estaban especializadas en la creación de su producto pero ahora, en la mayoría de los casos,  deben hacer frente al desarrollo e incorporación de una tecnología desconocida para ellos que consiste en la conectividad de sus aparatos a internet, y para ello tendrán que destinar recursos y dinero a esta labor, desde personal especializado hasta las compra de material como microcontroladores o módulos de red.  

Hoy en día, gracias a los avances de la tecnología es posible fabricar pequeños dispositivos IoT con facilidad debido a que el tamaño de los chips con los que se fabrican los modulos de red son de apenas unos centímetros de tamaño y el coste es de menos de 2$ por modulo, por lo tanto fabricar de cero, o transformar un objeto normal en uno IoT, es bastante asequible haciendo que este nuevo sector de la tecnología crezca imparablemnte. 

Una de las industrias que deberán hacer frente a este cambio será la industria de la instrumentación médica para conectar a internet todos sus aparatos médicos, que sea cual sea su función en última instancia están destinados a la obtención de datos fisiológicos muy útiles para su posterior análisis y acorde a ellos una toma de decisión adecuada.

Hay algunas razones por las que es interesante enviar datos generados o recopilados por dispositivos médicos a través de Internet. Una de ellas es porque muchos de los dispositivos médicos suelen ser de pequeño tamaño y para almacenar todos los datos que recopilan necesitarían una memoria incorporada al aparato, si bien las dimensiones de la memoría no serían mucho problema, si que lo sería el coste adicional de esta dependiendo de su capacidad y la posterior molestia de tener que volcar todos los datos a un software corriendo en un ordenador o servidor, por lo tanto, pasando a uno de las siguientes motivos, los datos ya no serían en tiempo real. Algo que permite internet de las cosas es monitorear en tiempo real, ya que la información según se obtiene se envía a internet en el instante. 
Con respecto al tema del almacenamiento gracias a internet de las cosas no tenemos que preocuparnos en tener una memoria en nuestro aparato ya que podemos tener una base de datos remota a la que gracias a internet estemos enviando todos los datos tomados por nuestro sistema médico.

Hasta el momento solo se ha hablado del internet de las cosas como un medio de lectura y envío de datos, "monitoreo", pero se puede cambiar el sentido, y que un equipo externo, a través de internet de las cosas, efectue respuestas acorde a esos datos y las envíe a nuestro aparato. Es verdad, que si el aparato dispone de un microcontrolador programable esas respuestas se podrían programar sin la necesidad de incorporar internet de las cosas, pero pensemos más a lo grande, pensemos como ese aparato se podría conectar por ejemplo a una inteligencia artificial ubicada en un servidor remoto , y que pudiese ofrecer respuestas acorde a un patron de datos, por ejemplo el pulso de una persona y un posible ataque.
}

#### Propuesta:

{Como se ha mencionado antes, con la tecnología de hoy en día es bastante sencillo desarrollar un sistema basado en internet de las cosas. ~~para monitorear parametros fisiológicos de un paciente y así ayudar en el diagnisto o control de él~~. Teniendo esto en cuenta he desarrollado un sistema de bajo coste basado en internet de las cosas y cuya función principal es monitorear la temperatura, pulso y movimientos de un paciente; y enviar todo ello a un servidor externo donde será representado graficamente para la futura supervisión de un profesional o de una inteligencia artificial. 
Podemos distinguir varias fases que comprenden en el funcionamiento del sistema:}

-------
-------

1. Introducción.
    - ¿Qué sería?
        - Plataforma educativa.
        - IOT.
        - IA.
        - Señales fisiológicas.
        - Modulo de control, seguimiento, control de patologías.
    - ¿Que hay ya hoy en día?
    - Propuesta.

2. Propuesta-plataforma.
3. Implementación.
4. Pruebas/resultados.
    - Técnico:
        - Latencia.
        - Información.
        - TCP/UDP.
    - Usabilidad:
        - Caminar con ello puesto.

5. Conclusión/Trabajos futuros.
6. +ANEXOS (código servidores y placa)


----

Bibliografía:


referencias:
[1] https://aws.amazon.com/es/what-is/iot/ 
[2] "Cisco Annual Internet Report (2018–2023) White Paper": https://www.cisco.com/c/en/us/solutions/collateral/executive-perspectives/annual-internet-report/white-paper-c11-741490.html
[3] https://www.apple.com/es/healthcare/apple-watch/
[4] https://www.apple.com/es/ios/health/
[5] http://www.my-signals.com/ 
[6] https://www.mdpi.com/2079-9292/8/2/178
[7] Application of Arduino Based Platform for Wearable Health Monitoring System.
[8] Wearable Internet-of-Things platform for human activity recognition and health care.
[9] https://mbientlab.com/metamotionr/