from datetime import datetime

monthList = 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'CA', 'CB', 'CC'
dayList = 'L', 'M', 'X', 'J', 'V', 'S', 'D'
fest = {'2024-01-01': 'F', '2024-12-25': 'F'}


def main():
    """
    Función principal.
    """
    year = int(input("Año: "))
    start_month = int(input("Mes: "))
    [print(cal) for cal in get_cal(year, start_month)]


def get_cal(year, start_month):
    """
    Genera una lista de 12 meses en el formato adecuado, comenzando desde un mes y año específicos.

    Args:
        year (int): Año de inicio.
        start_month (int): Mes de inicio (1-12).

    Returns:
        List[str]: Lista de 12 cadenas de caracteres, cada una representando un mes.
    """
    _udpCalY = []
    for i in range(12):
        month_index = (start_month + i - 1) % 12
        current_year = year + (start_month + i - 1) // 12
        _udpCalM = monthList[month_index]

        for day in range(1, 32):  # Siempre hasta 31 días
            try:
                _date = datetime(current_year, month_index + 1, day)
                _day = dayList[_date.weekday()]
                if _date.strftime('%Y-%m-%d') in fest:
                    _udpCalM += fest[_date.strftime('%Y-%m-%d')]
                else:
                    _udpCalM += _day
            except ValueError:
                _udpCalM += '-'

        _udpCalY.append(_udpCalM.ljust(33, '-'))  # Asegurarse de que el string tenga 33 caracteres

    return _udpCalY


if __name__ == '__main__':
    main()
