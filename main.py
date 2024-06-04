import os

import logic
import json
import time
import flask
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PARALELEPIPEDO'
sendTime = 0


class ActionEnum:
    RemoveFestivo = 0
    AddFestivo = 1
    RemoveHorario = 2
    AddHorario = 3
    Apply = 4
    Nothing = 5


# Test values, should be stored in a file with the appropriate retrieve method.
class FileSystem:
    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        with open('data.json', 'r') as file:
            return json.load(file)

    def save_data(self):
        with open('data.json', 'w') as file:
            json.dump(self.data, file, indent=4)

    @property
    def festDataFile(self):
        return self.data['festDataFile']

    @festDataFile.setter
    def festDataFile(self, value):
        self.data['festDataFile'] = value

    @property
    def horariosDataFile(self):
        return self.data['horariosDataFile']

    @horariosDataFile.setter
    def horariosDataFile(self, value):
        self.data['horariosDataFile'] = value

    @property
    def yearFile(self):
        return self.data['yearFile']

    @yearFile.setter
    def yearFile(self, value):
        self.data['yearFile'] = value

    @property
    def monthFile(self):
        return self.data['monthFile']

    @monthFile.setter
    def monthFile(self, value):
        self.data['monthFile'] = value

    @property
    def folderFile(self):
        return self.data['folderFile']

    @folderFile.setter
    def folderFile(self, value):
        self.data['folderFile'] = value


File = FileSystem()


def GetData(mRequest):
    year = int(mRequest.form.get("year"))
    month = int(mRequest.form.get("month")) + 1
    folder = int(mRequest.form.get("folder"))

    festInis = mRequest.form.getlist("festIni")
    festFins = mRequest.form.getlist("festFin")
    festData = []
    for i in range(len(festInis)):
        festData.append({"st": festInis[i], "ed": festFins[i]})

    times = mRequest.form.getlist("time")
    reps = mRequest.form.getlist("rep")
    vols = mRequest.form.getlist("vol")
    horariosData = []
    for i in range(len(times)):
        horariosData.append({"time": times[i], "rep": reps[i], "vol": vols[i]})

    if mRequest.form.get("AddFestivoRow") is not None:
        action = ActionEnum.AddFestivo
    elif mRequest.form.get("PopFestivoRow") is not None:
        action = ActionEnum.RemoveFestivo
    elif mRequest.form.get("AddHorarioRow") is not None:
        action = ActionEnum.AddHorario
    elif mRequest.form.get("PopHorarioRow") is not None:
        action = ActionEnum.RemoveHorario
    elif mRequest.form.get("Apply") is not None:
        action = ActionEnum.Apply
    else:
        action = ActionEnum.Nothing

    return action, horariosData, festData, year, month, folder


def ValidateData(horariosData, festData, year, month, folder, isSending):
    errorMessages = []
    notificationMessages = []

    # Ensure valid folder
    if not 0 < folder < 100:
        errorMessages.append("La carpeta debe estar en 0 y 100. Se ha asignado automáticamente el valor más alto.")
        folder = 99

    # Fix Horarios None fields
    for i in range(len(horariosData)):
        if horariosData[i]["time"] != '':
            horariosData[i]["rep"] = horariosData[i]["rep"] if horariosData[i]["rep"] is not None else ""
            horariosData[i]["vol"] = horariosData[i]["vol"] if horariosData[i]["vol"] is not None else "5"

    # Fix Festivos empty fields
    for festPair in festData:
        if festPair['st'] == '' and festPair['ed'] != '':
            festPair['st'] = festPair['ed']
            notificationMessages.append("Te puse el inicio como el final weon")
        elif festPair['ed'] == '' and festPair['st'] != '':
            festPair['ed'] = festPair['st']
            notificationMessages.append("Te puse el final como el inicio bobo")

    # Only execute this validation when we are about to send UDP
    if isSending:
        # Delete empty Horarios
        nHorRem = 0
        tmpHorariosData = []
        for i in range(len(horariosData)):
            if horariosData[i]["time"] != '':
                tmpHorariosData.append(
                    {"time": horariosData[i]["time"], "rep": horariosData[i]["rep"], "vol": horariosData[i]["vol"]})
            else:
                nHorRem += 1
        horariosData = tmpHorariosData

        if nHorRem > 0:
            errorMessages.append(
                f'Se ha{"n" if nHorRem > 1 else ""} eliminado {nHorRem} {"filas" if nHorRem > 1 else " fila"} de tramos horarios vacía{"s" if nHorRem > 1 else ""}.')

        # Delete empty Festivos
        nFestRem = 0
        tmpFestData = []
        for i in range(0, len(festData)):
            if festData[i]["st"] != "" and festData[i]["ed"] != "":
                tmpFestData.append({"st": festData[i]["st"], "ed": festData[i]["ed"]})
            else:
                nFestRem += 1
        festData = tmpFestData

        if nFestRem > 0:
            errorMessages.append(
                f'Se ha{"n" if nFestRem > 1 else ""} eliminado {nFestRem} {"filas" if nFestRem > 1 else " fila"} de festivos vacía{"s" if nFestRem > 1 else ""}.')

    return errorMessages, notificationMessages, horariosData, festData, year, month, folder


@app.route("/", methods=['GET', 'POST'])
def editData():
    print("EditData Route")

    if request.method == 'GET':
        print("GET METHOD CALLED!")
        # Grab file version
        horariosData = File.horariosDataFile
        festData = File.festDataFile
        year = File.yearFile
        month = File.monthFile - 1
        folder = File.folderFile
        return render_template('editData.html', festData=festData, nFestivosData=len(festData),
                               horariosData=horariosData, nHorariosData=len(horariosData), year=year,
                               month=month, folder=folder)
    elif request.method == 'POST':
        action, horariosData, festData, year, month, folder = GetData(request)

        isSendingUDP = action == ActionEnum.Apply
        errorMessages, notificationMessages, horariosData, festData, year, month, folder = ValidateData(horariosData,
                                                                                                        festData, year,
                                                                                                        month,
                                                                                                        folder,
                                                                                                        isSendingUDP)

        if action == ActionEnum.AddFestivo:
            festData.append({"st": "", "ed": ""})
        elif action == ActionEnum.RemoveFestivo:
            if len(festData) < 1:
                errorMessages.append("La lista de festivos ya esta vacía")
            else:
                festData.pop()
        elif action == ActionEnum.AddHorario:
            if len(horariosData) < 20:
                horariosData.append({"time": "", "rep": "", "vol": "5"})
            else:
                errorMessages.append('Número de tramos horarios máximo alcanzado.')
        elif action == ActionEnum.RemoveHorario:
            if len(horariosData) < 1:
                errorMessages.append("La lista de tramos horarios ya esta vacía")
            else:
                horariosData.pop()
        elif action == ActionEnum.Apply:
            # Send Commands
            logic.udp_send(logic.gen_now())
            print(f"UDP enviado: {logic.gen_now()}")
            time.sleep(sendTime)

            logic.udp_send(logic.gen_fol(folder))
            print(f"UDP enviado: {logic.gen_fol(folder)}")
            time.sleep(sendTime)

            for tim in logic.gen_time(horariosData):
                logic.udp_send(tim)
                print(f"UDP enviado: {tim}")
                time.sleep(sendTime)

            logic.udp_send(logic.gen_rep(horariosData))
            print(f"UDP enviado: {logic.gen_rep(horariosData)}")
            time.sleep(sendTime)

            logic.udp_send(logic.gen_vol(horariosData))
            print(f"UDP enviado: {logic.gen_vol(horariosData)}")
            time.sleep(sendTime)

            for cal in logic.gen_cal(year, month, festData):
                logic.udp_send(cal)
                print(f"UDP enviado: {cal}")
                time.sleep(sendTime)

            print(len(horariosData))

        # Update data
        File.horariosDataFile = horariosData
        File.festDataFile = festData
        File.yearFile = year
        File.monthFile = month
        File.folderFile = folder

        # Save data to JSON (disk)
        File.save_data()

        # Flash messages
        for notificationMessage in notificationMessages:
            flash(notificationMessage, 'info')

        if len(errorMessages) != 0:
            for errorMessage in errorMessages:
                flash(errorMessage, 'warning')
        elif request.form.get('Apply') is not None:
            flash('Mensajes UDP enviados.', 'success')

        return redirect(url_for('editData'))


@app.route('/favicon.ico')
def favicon():
    basePath, unused = os.path.split(app.root_path)
    return flask.send_from_directory(os.path.join(basePath, 'favicon_io'), 'favicon.ico')


@app.route('/apple-touch-icon.ico')
def apple_icon():
    basePath, unused = os.path.split(app.root_path)
    return flask.send_from_directory(os.path.join(basePath, 'static', 'favicon_io'), 'apple-touch-icon.png')


@app.route('/icon')
def icon():
    basePath, unused = os.path.split(app.root_path)
    return flask.send_from_directory(os.path.join(basePath, 'static', 'favicon_io'), 'favicon-32x32.png')


@app.route('/manifest')
def manifest():
    basePath, unused = os.path.split(app.root_path)
    return redirect(os.path.join(basePath, 'favicon_io', 'static', 'site.webmanifest'))


app.run(debug=True, port=5000)
