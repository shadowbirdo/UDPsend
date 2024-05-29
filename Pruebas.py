'''
try:
    bucle for que hace los meses desde n
except IndexError:
    año += 1
    bucle for que hace los meses desde 0 hasta n
'''


import socket
from datetime import datetime

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

UDP_IP = '192.164.4.1'
UDP_PORT = 12345

monthList = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'CA', 'CB', 'CC']
dayList = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
fest = {'2024-01-01': 'F', '2024-12-25': 'F'}


def main():
    month_start = int(input("Introduce un valor de 1 a 12: "))
    year = 2024
    generate_calendars(year, month_start)


def month_from_(n):
    n = (n - 1) % len(monthList)  # Asegura que n esté en el rango válido
    return monthList[n:] + monthList[:n]


def udp_send(msg):
    sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))


def gen_cal(year, month):
    _monthList = month_from_(month)
    month_name = _monthList[0]
    _udpCal = month_name  # Inicializa el str con el nombre del primer mes
    for day in range(1, 32):
        try:
            fecha = datetime(year, month, day)
            __dayList = dayList[fecha.weekday()]
            # Comprobar si es festivo
            if fecha.strftime('%Y-%m-%d') in fest:
                _udpCal += fest[fecha.strftime('%Y-%m-%d')]
            else:
                _udpCal += __dayList
        except ValueError:
            # Si el día no existe en el mes, rellenar con '-'
            _udpCal += '-'
    if len(_udpCal) != 33:
        raise Exception('LengthError')
    udp_send(_udpCal)
    return _udpCal


def generate_calendars(year, month_start):
    for i in range(12):
        month = (month_start + i - 1) % 12 + 1  # Calcula el mes correcto
        cal = gen_cal(year, month)
        print(cal)


if __name__ == '__main__':
    main()
