# Principales Problemas durante el proyecto:

- Sensor de pulso mete mucho ruido. Y con excasas variaciones en el sensor se producen altas oscilaciones en la medida.
  - Solución: con sofware guardar una estimación de la media de los últimos 10 segundos y todo lo que la sobrepase es un pulso.

- Módulos normalmente usados para Arduino usan librerías de c y no usan micropython.

- Raspberry pico no soporta todas las librerías de micropython.

- Puertos analógicos insuficientes.

- No hay módulo de EMG en el mercado que sea barato.
  - Solución: Fabricar uno a partir de resistencias, amplificadores y condensadores.

- No hay modulo de oximetría en el mercado, el único que existe son todos malos y se ha dejado de fabricar.
  - Solución: Pedir uno por aliexpress.
