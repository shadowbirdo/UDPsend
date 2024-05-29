
from datetime import datetime

# Obtener horario de cambio de clase
def obtener_horario_cambio_clase():
    return "H0830-0840-0850-0930-1030-1125-1205-1300-1400-1440-1450-1500-1545-1645-1745-1845-1900-2000-2100-2145-2200"

# Enviar horario de cambio de clase por UDP_formatting
def enviar_horario_cambio_clase(horario):
    sock.sendto(horario.encode(), (UDP_IP, UDP_PORT))
    print(f"Enviado: {horario}")

# Obtener tiempo de reproducción de cada canción
def obtener_tiempo_reproduccion():
    return "T120-045-045-045-045-120-120-045-045-045-045-120-045-045-045-045-045-045-045-045-045"

# Enviar tiempo de reproducción por UDP_formatting
def enviar_tiempo_reproduccion(tiempo):
    sock.sendto(tiempo.encode(), (UDP_IP, UDP_PORT))
    print(f"Enviado: {tiempo}")

# Obtener volumen de tramos horarios
def obtener_volumen_tramos():
    return "V25-18-18-25-25-25-25-25-25-18-18-25-25-25-25-25-25-25-25-25-25"

# Enviar volumen de tramos horarios por UDP_formatting
def enviar_volumen_tramos(volumen):
    sock.sendto(volumen.encode(), (UDP_IP, UDP_PORT))
    print(f"Enviado: {volumen}")

# Obtener número de tramos horarios habilitados
def obtener_numero_tramos_habilitados():
    return "N17"

# Enviar número de tramos horarios habilitados por UDP_formatting
def enviar_numero_tramos_habilitados(numero_tramos):
    sock.sendto(numero_tramos.encode(), (UDP_IP, UDP_PORT))
    print(f"Enviado: {numero_tramos}")

# Obtener número de carpeta donde situar las canciones
def obtener_numero_carpeta():
    return "F01"

# Enviar número de carpeta por UDP_formatting
def enviar_numero_carpeta(numero_carpeta):
    sock.sendto(numero_carpeta.encode(), (UDP_IP, UDP_PORT))
    print(f"Enviado: {numero_carpeta}")

# Obtener fecha y hora actual en formato DS3132
def obtener_fecha_hora():
    ahora = datetime.now()
    return f"D-{ahora.strftime('%Y/%m/%d/%H/%M/%S')}"

# Enviar fecha y hora por UDP_formatting
def enviar_fecha_hora(fecha_hora):
    sock.sendto(fecha_hora.encode(), (UDP_IP, UDP_PORT))
    print(f"Enviado: {fecha_hora}")

