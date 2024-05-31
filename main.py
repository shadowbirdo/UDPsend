import logic
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# Test values, should be stored in a file with the appropriate retrieve method.
class FileSystem:
    festDataFile = [
        {"st": "2024-05-11", "ed": "2024-05-13"},
        {"st": "2024-06-03", "ed": "2024-06-18"},
        {"st": "2024-11-10", "ed": "2024-11-10"}
    ]
    horariosDataFile = [
        {"time": "09:30", "rep": "45s", "vol": "5"},
        {"time": "10:30", "rep": "45s", "vol": "10"},
        {"time": "11:30", "rep": "60s", "vol": "5"}
    ]
    yearFile = 2025
    monthFile = 1
    folderFile = 2


File = FileSystem()


@app.route("/", methods=['GET'])
def home():
    print("Home Route with method: " + request.method)
    if request.method == 'GET':
        if request.args.get("GoToEditData") is not None:
            return redirect(url_for('editData'))
        else:
            return render_template('home.html')


@app.route("/editData", methods=['GET', 'POST'])
def editData():
    print("EditData Route")

    # Grab file version
    horariosData = File.horariosDataFile
    festData = File.festDataFile
    year = File.yearFile
    month = File.monthFile
    folder = File.folderFile

    if request.method == 'GET':
        print("GET METHOD CALLED!")
    elif request.method == 'POST':
        if request.form.get("AddFestivoRow") is not None:
            festData.append({"st": "", "ed": ""})
        elif request.form.get("AddHorarioRow") is not None:
            horariosData.append({"time": "", "rep": "", "vol": ""})
        elif request.form.get("GoHome") is not None:
            return redirect(url_for('home'))
        elif request.form.get("Apply") is not None:
            folder = request.form.get("folder")
            year = int(request.form.get("year"))
            month = int(request.form.get("month"))
            for i in range(0, len(horariosData)):
                horariosData[i]["time"] = request.form.get("time"+str(i))
                horariosData[i]["rep"] = request.form.get("rep"+str(i))
                horariosData[i]["vol"] = request.form.get("vol"+str(i))
            for i in range(0, len(festData)):
                festData[i]["st"] = request.form.get("festIni"+str(i))
                festData[i]["ed"] = request.form.get("festFin"+str(i))
            print("NEW festData", festData)

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

            [logic.udp_send(cal) for cal in logic.gen_cal(year, month)]
            [print(f"UDP enviado: {cal}") for cal in logic.gen_cal(year, month)]

            # Save to file
            File.horariosDataFile = horariosData
            File.festDataFile = festData
            File.yearFile = year
            File.monthFile = month
            File.folderFile = folder
        elif request.form.get("Reload") is not None:
            print("DO THINGS")

    return render_template('editData.html', festData=festData, nFestivosData=len(festData),
                           horariosData=horariosData, nHorariosData=len(horariosData), year=year, folder=folder)


app.run(debug=True, port=5000)
