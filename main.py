import logic
import json
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PARALELEPIPEDO'


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
                               horariosData=horariosData, nHorariosData=len(horariosData), year=year, month=month,
                               folder=folder)
    elif request.method == 'POST':
        if request.form.get("AddFestivoRow") is not None:
            festData.append({"st": "", "ed": ""})
        elif request.form.get("PopFestivoRow") is not None:
            festData.pop()
        elif request.form.get("AddHorarioRow") is not None:
            horariosData.append({"time": "", "rep": "", "vol": ""})
        elif request.form.get("PopHorarioRow") is not None:
            horariosData.pop()
        elif request.form.get("Apply") is not None:
            folder = int(request.form.get("folder"))
            year = int(request.form.get("year"))
            month = int(request.form.get("month"))
            for i in range(0, len(horariosData)):
                horariosData[i]["time"] = request.form.get("time" + str(i))
                horariosData[i]["rep"] = request.form.get("rep" + str(i))
                horariosData[i]["vol"] = request.form.get("vol" + str(i))
            for i in range(0, len(festData)):
                festData[i]["st"] = request.form.get("festIni" + str(i))
                festData[i]["ed"] = request.form.get("festFin" + str(i))

            # Flash Messages
            if 0 <= folder <= 100:
                flash('Operation completed successfully!', 'success')
            else:
                flash('Error', 'danger')

            # Send Commands
            logic.udp_send(logic.gen_now())
            print(f"UDP enviado: {logic.gen_now()}")

            logic.udp_send(logic.gen_fol(folder))
            print(f"UDP enviado: {logic.gen_fol(folder)}")

            [logic.udp_send(tim) for tim in logic.gen_time(horariosData)]
            [print(f"UDP enviado: {tim}") for tim in logic.gen_time(horariosData)]

            logic.udp_send(logic.gen_rep(horariosData))
            print(f"UDP enviado: {logic.gen_rep(horariosData)}")

            logic.udp_send(logic.gen_vol(horariosData))
            print(f"UDP enviado: {logic.gen_vol(horariosData)}")

            [logic.udp_send(cal) for cal in logic.gen_cal(year, month, festData)]
            [print(f"UDP enviado: {cal}") for cal in logic.gen_cal(year, month, festData)]

            # Save to file
            File.horariosDataFile = horariosData
            File.festDataFile = festData
            File.yearFile = year
            File.monthFile = month + 1
            File.folderFile = folder

            # Save data to JSON
            File.save_data()

        return redirect(url_for('editData'))


app.run(debug=True, port=5000)
