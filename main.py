import socket
from datetime import datetime

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

UDP_IP = '192.164.4.1'
UDP_PORT = 12345

monthList = 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'CA', 'CB', 'CC'
dayList = 'L', 'M', 'X', 'J', 'V', 'S', 'D'
fest = {'2024-01-01': 'F', '2024-12-25': 'F'}


def main():
    print(gen_cal(2024, 7))


def month_from_(n):
    n = (n - 1) % len(monthList)  # Asegura que n esté en el rango válido
    return monthList[n:] + monthList[:n]


def udp_send(msg):
    sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))


def gen_cal(year, month):
    _monthList = month_from_(month)
    for month in range(len(_monthList)):
        _udpCal = _monthList[month - 1]  # Ajusta index para acceder al mes correcto e inicializar el str con su nombre
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
        else:
            return _udpCal  # Asegurarse de que la cadena tiene exactamente 31 caracteres


if __name__ == '__main__':
    main()
    