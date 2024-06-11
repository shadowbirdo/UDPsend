Si es la primera vez que se usa el programa, se deberá ejecutar primero "Install_Python+Flask.bat" y luego "UDPsend.bat".
Esto instalará las dependencias necesarias para ejecutar el programa. En el resto de los casos, se ejecutará directamente
"USPsend.bat".

Los mensajes UDP enviados se mandan también por la terminal para poder comprobarlos.

Los datos del programa se almacenan en "data.json" entre sesión y sesión.

"main.py" contiene la variable "sendTime_delay". Esta variable determina el tiempo que espera el programa entre cada
mensaje UDP enviado.

Los mensajes UDP se condifican siguiendo el siguiente conjunto de reglas:

Formato para enviar y grabar calendario en EEPROM

C1(Enero),  C2(Febrero) ………….. CA(Octubre), CB(Noviembre), CC(Diciembre)
LMXJVSD(Día de la semana), F(Fiesta), -(Completar mes hasta 31 caracteres)

Meses 2021 (hay que adaptar cada año)
C1FFFFFFFFSDLMXJVSDLMXJVSDLMXJVSD
C2LMXJVSDLMXJVSDLMXJVSDLMXJVSD---
C3FMXJVSDLMXJVSDLMXJVSDLMXJVSDFFF
C4FFSDLMXJVSDLMXJVSDLMXJVSDLMXJV-
C5SDFMXJVSDLMXJVSDLMXJVSDLMXJVSDL
C6MXJVSDLMXJVSDLMXJVSDLMXJVSDLMX-
C7JVSDLMXJVSDLMXJVSDLMXJVSDLMXJVS
C8DLMXJVSDLMXJVSDLMXJVSDLMXJVSDLM

Meses 2020 (hay que adaptar cada año)
C9MXJVSDLMXJVSDLMXJVSDLMXJVSDLMX-
CAJVSDLMXJVSDFMXJVSDLMXJVSDLMXJVS
CBDFMXJVSDLMXJVSDLMXJVSDLMXJVSDL- 
CCMXJVSDFFXJVSDLMXJVSDLMXFFFFFFFF



Formato para enviar horario de cambio de clase (399 posición en EEP)

(21 tramos posibles, se pueden completar todos, aunque solo serán efectivos los primeros que coincidan con el número de tramos horarios habilitados)

H0830-0840-0850-0930-1030-1125-1205-1300-1400-1440-1450-1500-1545-1645-1745-1845-1900-2000-2100-2145-2200



Formato para enviar tiempo de reproducción de cada canción (pos 800 en EEPROM) 

(21 valores posibles, se pueden completar todos, aunque solo serán efectivos los primeros que coincidan con el número de tramos horarios habilitados)

Tiempo de Reproducción en segundos (060 ->  60 segundos,   120 ->  120 segundos)

T120-045-045-045-045-120-120-045-045-045-045-120-045-045-045-045-045-045-045-045-045



Volumen  Tramos horarios  (pos 670 en EEPROM)- valores entre 5 y 30

V25-18-18-25-25-25-25-25-25-18-18-25-25-25-25-25-25-25-25-25-25

(21 valores posibles, se pueden completar todos, aunque solo serán efectivos los primeros que coincidan con el número de tramos horarios habilitados)



Número de Tramos horarios  habilitados  (pos 650 en EEPROM)

NXX    (XX Numero de toques de timbre  00 hasta 21). Debe ser igual a los cambios de clase programados anteriormente.   

N17



Número de carpeta donde situar las canciones  (pos 625 en EEPROM)
FXX    (XX Numero de carpeta  00 hasta 99). 
F01



Formato para poner DS3132 en hora
D-aaaa/mm/dd/hh/mm/ss
