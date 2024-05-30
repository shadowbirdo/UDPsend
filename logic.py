import socket
from datetime import datetime

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

UDP_IP = '192.168.4.1'
UDP_PORT = 12345

fest = {'2024-01-01': 'F', '2024-12-25': 'F'}


def main():
    """
    Función principal.
    """
    print(gen_now())
    year = int(input("Año: "))
    start_month = int(input("Mes: "))
    [print(cal) for cal in gen_cal(year, start_month)]
    [udp_send(cal) for cal in gen_cal(year, start_month)]


def udp_send(msg):
    """
    Manda mensaje UDP.

    Args:
        msg (str): The message to be sent.

    Returns:
        None
    """
    sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))


def gen_cal(year, start_month):
    """
    Genera una lista de 12 meses en el formato adecuado, comenzando desde un mes y año específicos.

    Args:
        year (int): Año de inicio.
        start_month (int): Mes de inicio (1-12).

    Returns:
        List[str]: Lista de 12 cadenas de caracteres, cada una representando un mes.
    """
    month_list = 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'CA', 'CB', 'CC'
    day_list = 'L', 'M', 'X', 'J', 'V', 'S', 'D'
    _udpCalY = []
    for i in range(12):
        month_index = (start_month + i - 1) % 12
        current_year = year + (start_month + i - 1) // 12
        _udpCalM = month_list[month_index]

        for day in range(1, 32):  # Siempre hasta 31 días
            try:
                _date = datetime(current_year, month_index + 1, day)
                _day = day_list[_date.weekday()]
                if _date.strftime('%Y-%m-%d') in fest:
                    _udpCalM += fest[_date.strftime('%Y-%m-%d')]
                else:
                    _udpCalM += _day
            except ValueError:
                _udpCalM += '-'

        _udpCalY.append(_udpCalM.ljust(33, '-'))  # Asegurarse de que el string tenga 33 caracteres

    return _udpCalY


def gen_fol(folder):
    """
    Genera una cadena con la carpeta de reproducción en el formato adecuado.

    Args:
        folder (str): Número de la carpeta como cadena.

    Returns:
        str: Nombre de la carpeta formateado con una "F" al inicio y con un cero a la izquierda si es necesario.
    """
    if len(f"{folder}") == 1:
        folder = "0" + folder
    return f"F{folder}"


def gen_now():
    """
    Genera una cadena con la fecha y hora actual en el formato adecuado.

    Returns:
        str: Cadena con el formato 'D-YYYY/MM/DD/HH/MM/SS' representando la fecha y hora actual.
    """
    return f"D-{datetime.now().strftime('%Y/%m/%d/%H/%M/%S')}"


if __name__ == '__main__':
    main()
    