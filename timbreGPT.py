import socket
from datetime import datetime

class Fecha:
    año = int(input("¿Qué año es? "))

# Dirección IP y puerto del servidor UDP
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Configuración del socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Obtener información del calendario
def obtener_calendario():
    # Crear una lista con los nombres de los meses en el formato requerido
    meses = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'CA', 'CB', 'CC']
    # Crear una lista para los días de la semana
    dias_semana = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
    # Definir los festivos manualmente
    festivos = {'2024-01-01': 'F', '2024-12-25': 'F'}
    calendario = []

    for mes in range(1, 13):
        # Añadir el prefijo del mes
        entrada_mes = meses[mes - 1]
        for dia in range(1, 32):
            try:
                fecha = datetime(Fecha.año, mes, dia)
                dia_semana = dias_semana[fecha.weekday()]
                # Comprobar si es festivo
                if fecha.strftime('%Y-%m-%d') in festivos:
                    entrada_mes += festivos[fecha.strftime('%Y-%m-%d')]
                else:
                    entrada_mes += dia_semana
            except ValueError:
                # Si el día no existe en el mes, rellenar con '-'
                entrada_mes += '-'
        calendario.append(entrada_mes)

    return calendario

# Enviar calendario por UDP
def enviar_calendario(calendario):
    for mes in calendario:
        sock.sendto(mes.encode(), (UDP_IP, UDP_PORT))
        print(f"Enviado: {mes}")

# Obtener horario de cambio de clase
def obtener_horario_cambio_clase():
    return "H0830-0840-0850-0930-1030-1125-1205-1300-1400-1440-1450-1500-1545-1645-1745-1845-1900-2000-2100-2145-2200"

# Enviar horario de cambio de clase por UDP
def enviar_horario_cambio_clase(horario):
    sock.sendto(horario.encode(), (UDP_IP, UDP_PORT))
    print(f"Enviado: {horario}")

# Obtener tiempo de reproducción de cada canción
def obtener_tiempo_reproduccion():
    return "T120-045-045-045-045-120-120-045-045-045-045-120-045-045-045-045-045-045-045-045-045"

# Enviar tiempo de reproducción por UDP
def enviar_tiempo_reproduccion(tiempo):
    sock.sendto(tiempo.encode(), (UDP_IP, UDP_PORT))
    print(f"Enviado: {tiempo}")

# Obtener volumen de tramos horarios
def obtener_volumen_tramos():
    return "V25-18-18-25-25-25-25-25-25-18-18-25-25-25-25-25-25-25-25-25-25"

# Enviar volumen de tramos horarios por UDP
def enviar_volumen_tramos(volumen):
    sock.sendto(volumen.encode(), (UDP_IP, UDP_PORT))
    print(f"Enviado: {volumen}")

# Obtener número de tramos horarios habilitados
def obtener_numero_tramos_habilitados():
    return "N17"

# Enviar número de tramos horarios habilitados por UDP
def enviar_numero_tramos_habilitados(numero_tramos):
    sock.sendto(numero_tramos.encode(), (UDP_IP, UDP_PORT))
    print(f"Enviado: {numero_tramos}")

# Obtener número de carpeta donde situar las canciones
def obtener_numero_carpeta():
    return "F01"

# Enviar número de carpeta por UDP
def enviar_numero_carpeta(numero_carpeta):
    sock.sendto(numero_carpeta.encode(), (UDP_IP, UDP_PORT))
    print(f"Enviado: {numero_carpeta}")

# Obtener fecha y hora actual en formato DS3132
def obtener_fecha_hora():
    ahora = datetime.now()
    return f"D-{ahora.strftime('%Y/%m/%d/%H/%M/%S')}"

# Enviar fecha y hora por UDP
def enviar_fecha_hora(fecha_hora):
    sock.sendto(fecha_hora.encode(), (UDP_IP, UDP_PORT))
    print(f"Enviado: {fecha_hora}")

# Ejecutar todas las funciones de envío
if __name__ == "__main__":
    calendario = obtener_calendario()
    enviar_calendario(calendario)
    
    horario_cambio_clase = obtener_horario_cambio_clase()
    enviar_horario_cambio_clase(horario_cambio_clase)
    
    tiempo_reproduccion = obtener_tiempo_reproduccion()
    enviar_tiempo_reproduccion(tiempo_reproduccion)
    
    volumen_tramos = obtener_volumen_tramos()
    enviar_volumen_tramos(volumen_tramos)
    
    numero_tramos = obtener_numero_tramos_habilitados()
    enviar_numero_tramos_habilitados(numero_tramos)
    
    numero_carpeta = obtener_numero_carpeta()
    enviar_numero_carpeta(numero_carpeta)
    
    fecha_hora = obtener_fecha_hora()
    enviar_fecha_hora(fecha_hora)
