# Principales Problemas durante el proyecto:

- Sensor de pulso mete mucho ruido. Y con excasas variaciones en el sensor se producen altas oscilaciones en la medida.
  - Solución: con sofware guardar una estimación de la media de los últimos 10 segundos y todo lo que la sobrepase es un pulso.

- Módulos normalmente usados para Arduino usan librerías de c y no usan micropython.
  - Solución: (muy costosa), intentar traducir de c a micropython la librería. 

- Raspberry pico no soporta todas las librerías de micropython.
  - Solución: leer bien la documentación e investigar que función puede sustituir a la que se usa en esa librería.

- Puertos analógicos insuficientes en un futuro posiblemente.
  - Posible problema si uso todos los sensores que inicialmente pensé. Todavía no he llegado a ese punto. No doy un sensor como definitivo hasta que no se demuestra funcionar correctamente.

- No hay módulo de EMG en el mercado que sea barato.
  - Solución: Fabricar uno a partir de resistencias, amplificadores y condensadores.

- No hay modulo de oximetría en el mercado, el único que existe son todos malos y se ha dejado de fabricar.
  - Solución: Pedir uno por aliexpress.

- No funciona el módulo MPU6050 que hace de acelerometro. Funcionó un día, pero luego ya no funcionaba. Probé a cambiar de modulo mpu6050, pero daba el mismo error, probé a cambiar de placa raspberry pi pico, pero igualmente daba el mismo error, probé a cambiar el mpu5060 a Arduino y funcionó, por lo tanto concluí que el error estaba en el código. 
  - Solución: Encontré otro código compatible tanto con raspberry pi pico como con el módulo MPU6050.

- El servidor no podía decodificar la información que le llegaba. Los pines tx y rx de la pico y del esp8266 estaban mal emparejados. La conexion estre ellos debe ser de tx-rx y rx-tx, ;y no tx-tx y rx-rx. Solución: cambiar los cables emparejados.
