import func
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# Test values, should be stored in a file with the appropriate retrieve method.
class FileSystem:
    festivosDataFile = [
        ["2024-05-11", "2024-05-13"],
        ["2024-06-03", "2024-06-18"],
        ["2024-11-10", "2024-11-10"]
    ]
    horariosDataFile = [
        ["9:30", "45s", "0.8", "1"],
        ["10:30", "45s", "1", "6"],
        ["11:30", "60s", "0.6", "3"]
    ]
    yearFile = 2025
    carpetaFile = 2


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
    festivosData = File.festivosDataFile
    year = File.yearFile
    carpeta = File.carpetaFile

    if request.method == 'GET':
        print("GET METHOD CALLED!")
    elif request.method == 'POST':
        if request.form.get("AddFestivoRow") is not None:
            festivosData.append(["", ""])
        elif request.form.get("AddHorarioRow") is not None:
            horariosData.append(["", "", "", ""])
        elif request.form.get("GoHome") is not None:
            return redirect(url_for('home'))
        elif request.form.get("Apply") is not None:
            carpeta = request.form.get("carpeta")
            year = int(request.form.get("year"))
            for i in range(0, len(festivosData)):
                festivosData[i][0] = request.form.get("festivosIni"+str(i))
                festivosData[i][1] = request.form.get("festivosFin"+str(i))
            print("NEW festivosData", festivosData)

            # Send Commands
            [func.udp_send(cal) for cal in func.gen_cal(year, 1)]
            [print(cal) for cal in func.gen_cal(year, 1)]
            # Save to file
            File.horariosDataFile = horariosData
            File.festivosDataFile = festivosData
            File.yearFile = year
            File.carpetaFile = carpeta
        elif request.form.get("Reload") is not None:
            print("DO THINGS")

    return render_template('editData.html', festivosData=festivosData, nFestivosData=len(festivosData),
                           horariosData=horariosData, nHorariosData=len(horariosData), year=year, carpeta=carpeta)


app.run(debug=True, port=5000)
