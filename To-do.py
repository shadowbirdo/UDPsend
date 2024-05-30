class Horario:
    def __init__(self):
        self.horario = input("Introduzca a continuación las horas a las que deberá sonar la campana (separadas por comas): ").split(",")
        self.generar_directrices()

    def generar_directrices(self):
        # Directriz 1
        direc1 = "H" + "-".join([hora.strip().zfill(5).replace(":", "") for hora in self.horario])
        
        # Directriz 2
        numero_tramos = len(self.horario)
        direc2 = f"N{numero_tramos:02}"
        
        print(direc1)
        print(direc2)

def main():
    hor2425 = Horario()

if __name__ == "__main__":
    main()
