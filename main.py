import logic
import json
import time
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PARALELEPIPEDO'
sendTime = 0


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


@app.route("/", methods=['GET', 'POST'])
def editData():
    print("EditData Route")

    # Grab file version
    horariosData = File.horariosDataFile
    festData = File.festDataFile
    year = File.yearFile
    month = File.monthFile - 1
    folder = File.folderFile

    if request.method == 'GET':
        print("GET METHOD CALLED!")
        return render_template('editData.html', festData=festData, nFestivosData=len(festData),
                                       horariosData=horariosData, nHorariosData=len(horariosData), year=year,
                                       month=month, folder=folder)
    elif request.method == 'POST':
        if request.form.get("AddFestivoRow") is not None:
            festData.append({"st": "", "ed": ""})
            for i in range(0, len(festData)):
                festData[i]["st"] = request.form.get("festIni" + str(i))
                festData[i]["ed"] = request.form.get("festFin" + str(i))
        elif request.form.get("PopFestivoRow") is not None:
            festData.pop()
            festData[i]["st"] = request.form.get("festIni" + str(i))
            festData[i]["ed"] = request.form.get("festFin" + str(i))
        elif request.form.get("AddHorarioRow") is not None:
            print(len(horariosData))
            if len(horariosData) < 21:
                horariosData.append({"time": "", "rep": "", "vol": ""})
                for i in range(len(horariosData)):
                    horariosData[i]["time"] = request.form.get("time" + str(i))
                    horariosData[i]["rep"] = request.form.get("rep" + str(i)) if request.form.get("rep" + str(i)) is not None else ""
                    horariosData[i]["vol"] = request.form.get("vol" + str(i)) if request.form.get("vol" + str(i)) is not None else "0"
            else:
                flash('Número de tramos horarios máximo alcanzado.', 'warning')
        elif request.form.get("PopHorarioRow") is not None:
            horariosData.pop()
        elif request.form.get("Apply") is not None:
            if 0 < int(request.form.get("folder")) < 100:
                folder = int(request.form.get("folder"))
            else:
                flash('El número de carpeta introducido no es válido. Se ha autocompletado con el número más alto.', 'warning')
                folder = 99
            year = int(request.form.get("year"))
            month = int(request.form.get("month")) + 1
            for i in range(len(horariosData)):
                if not request.form.get("time" + str(i)) == request.form.get("rep" + str(i)) == "":
                    horariosData[i]["time"] = request.form.get("time" + str(i))
                    horariosData[i]["rep"] = request.form.get("rep" + str(i))
                    horariosData[i]["vol"] = request.form.get("vol" + str(i))
                elif request.form.get("time" + str(i)) == request.form.get("rep" + str(i)) == "":
                    horariosData.pop()
            for i in range(0, len(festData)):
                if request.form.get("festIni" + str(i)) and request.form.get("festFin" + str(i)) is not None:
                    festData[i]["st"] = request.form.get("festIni" + str(i))
                    festData[i]["ed"] = request.form.get("festFin" + str(i))
                else:
                    festData.pop()

            # Validation


            # Flash Messages
            if True:
                flash('Mensajes UDP enviados.', 'success')

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

            # Save to file
            File.horariosDataFile = horariosData
            File.festDataFile = festData
            File.yearFile = year
            File.monthFile = month
            File.folderFile = folder

            # Save data to JSON
            File.save_data()

        return redirect(url_for('editData'))


app.run(debug=True, port=5000)
