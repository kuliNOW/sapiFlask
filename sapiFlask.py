from flask import Flask, request, jsonify
from datetime import datetime as dm
import re
import bleach
import os
import json
import sys
import shutil

app = Flask(__name__)
nameapp = os.path.basename(sys.argv[0])
warning = "Proses injeksi terdeteksi, silahkan isi dengan data yang benar"
notfound = "Data tidak ditemukan"
null = "Data tidak boleh kosong"
success = "Data berhasil ditambahkan"
notable = "Belum ada data diinputkan"
database = os.path.dirname(os.path.abspath(__file__)) + "\\Traceability.json"
bath = os.path.dirname(os.path.abspath(__file__)) + f"\\{nameapp[:-2]}bat"
appPath = os.path.dirname(os.path.abspath(__file__)) + f"\\{nameapp}"
pyPath = sys.path[4]

def createBatch(nfile):
    with open(nfile, 'w') as f:
        f.write(f"""@echo off
set PYPATH={pyPath}\\python.exe
set SCRPATH={appPath}
start /B \"%PYPATH%\" \"%SCRPATH%\"""")

def cpstartup(f):
    startup = 'Microsoft\\Windows\\Start Menu\\Programs\\Startup'
    startupPath = os.path.join(
        os.environ['APPDATA'], 
        startup+'\\'+f"{nameapp[:-2]}bat"
    )
    if os.path.exists(bath) and not os.path.exists(startupPath):
        shutil.copy(f, startupPath)

def createDB(db):
    global alldata
    with open(db, 'w') as f:
        f.write('{}')
    alldata = {}
    
def readDB(db):
    global alldata
    with open(db, 'r') as f:
        try:
            alldata = json.load(f)
            if not isinstance(alldata, dict):
                alldata = {}
        except json.JSONDecodeError:
            alldata = {}

if os.path.exists(bath):
    os.remove(bath)
else:
    createBatch(bath)
    cpstartup(bath)
    os.remove(bath)

if os.path.exists(database):
    readDB(database)
else:
    createDB(database)

def saveDB(db, data):
    with open(db, 'w') as f:
        json.dump(data, f, indent=4)

def xssClean(data):
    return bleach.clean(data)

def nullCheck(n, info):
    if n is None:
        return jsonify({'Message': info}), 400

def createdAT(p, wrn):
    ptrn = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
    if not re.match(ptrn, p):
        return jsonify({'Message': wrn}), 400

def isdate(p, wrn):
    ptrn = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(ptrn, p):
        return jsonify({'Message': wrn}), 400

def filter(p, wrn):
    ptrn = r'^[A-Za-z0-9\s\.\-\+\*\?\/\|&;<>!@#$%^=\[\]{}()]+$'
    if not re.match(ptrn, p):
        return jsonify({'Message': wrn}), 400

def check(data, wrn):
    if not re.match(r'^[A-Za-z0-9_-]+$', data):
        return jsonify({'Message': wrn}), 400

def lendata(data):
    if len(data) == 0:
        return jsonify({'Message': notable}), 404

@app.route('/', methods=['GET'])
def get():
    response = lendata(alldata)
    if response:
        return response
    return jsonify(list(alldata.values())), 200

@app.route('/data', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        get = ['CODE', 'NPK', 'LINE', 'DATE']
        g1 = request.args.get(get[0])
        g2 = request.args.get(get[1])
        g3 = request.args.get(get[2])
        g5 = request.args.get(get[3])
        
        endpoint = [g1, g2, g3]
        for i in endpoint:
            response = nullCheck(i, null)
            if response:
                return response
            response = check(i, warning)
            if response:
                return response
            xssClean(i)
            response = filter(i, warning)
            if response:
                return response

        if g5:
            response = isdate(g5, warning)
            if response:
                return response
        
        key = (g1, g2, g3, g5)
        response = lendata(alldata)
        if response:
            return response
        values = alldata.get(str(key))
        if values:
            return jsonify(values), 200
        else:
            return jsonify({'Message': notfound}), 404

    elif request.method == 'POST':
        post = ['CODE', 'NPK', 'LINE', 'STATUS_JUDGEMENT', 'DATE', 'CREATED_AT', 'STATUS_DEVICE', 'COUNTER', 'SPARE']
        p1 = request.form.get(post[0])
        p2 = request.form.get(post[1])
        p3 = request.form.get(post[2])
        p4 = request.form.get(post[3])
        p5 = request.form.get(post[4])
        p6 = request.form.get(post[5])
        p7 = dm.strftime(dm.now(), '%Y-%m-%d %H:%M:%S')
        p8 = request.form.get(post[6])
        p9 = request.form.get(post[7])
        p10 = request.form.get(post[8])

        endpoint = [p1, p2, p3, p4, p8, p9, p10]
        for i in endpoint:
            response = nullCheck(i, null)
            if response:
                return response
            response = check(i, warning)
            if response:
                return response
            xssClean(i)
            response = filter(i, warning)
            if response:
                return response

        if p5:
            response = isdate(p5, warning)
            if response:
                return response
            
        if p6:
            response = createdAT(p6, warning)
            if response:
                return response

        key = (p1, p2, p3, p5)
        data = {
            'CODE': p1,
            'NPK': p2,
            'LINE': p3,
            'STATUS_JUDGEMENT': p4,
            'DATE': p5,
            'CREATED_AT': p6,
            'UPDATED_AT': p7,
            'STATUS_DEVICE': p8,
            'COUNTER': p9,
            'SPARE': p10
        }

        alldata[str(key)] = data
        saveDB(database, alldata)
        return jsonify({'Message': success}), 201

if __name__ == '__main__':
    app.run(debug=True, port=1234)