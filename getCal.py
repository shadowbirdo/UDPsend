import socket
from datetime import datetime

sock = socket.socket(socket.AF_INET, socket.sock)
UDP_IP = "192.164.4.1"
UDP_PORT = "12345"

class Calendario:
    mesAño = "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "CA", "CB", "CC"
    diaSemana = "L", "M", "X", "J", "V", "S", "D"
    fest = {"2024-01-01": "F", "2024-12-25": "F"}

    def __init__(self, año, mes):
        self.año = año
        self.mes = mes

    def convMes(self):
        return self.mesAño[self.mes - 1]  # Ajuste del índice para acceder al mes correcto

    def send(self):
        __udpCal = self.convMes()  # Inicializar la cadena con el nombre del mes

        for dia in range(1, 32):
            try:
                fecha = datetime(self.año, self.mes, dia)
                __diaSemana = self.diaSemana[fecha.weekday()]
                # Comprobar si es festivo
                if fecha.strftime("%Y-%m-%d") in self.fest:
                    __udpCal += self.fest[fecha.strftime("%Y-%m-%d")]
                else:
                    __udpCal += __diaSemana
            except ValueError:
                # Si el día no existe en el mes, rellenar con "-"
                __udpCal += "-"
        if len(__udpCal) != 33:
            raise Exception("LengthError")
        else:            
            sock.sendto(bytes(__udpCal, "utf-8"), (UDP_IP, UDP_PORT))
            return __udpCal  # Asegurarse de que la cadena tiene exactamente 31 caracteres

def main():
    año = int(input("¿Qué año es? "))
    mes = int(input("¿Qué mes es? "))
    cal = Calendario(año, mes)
    print(cal.send())

if __name__ == "__main__":
    main()
