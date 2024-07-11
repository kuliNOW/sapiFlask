from flask import Flask, request, jsonify
from datetime import datetime as dm
import re
import bleach

app = Flask(__name__)

alldata = {}

def xssClean(data):
    return bleach.clean(data)

def nullCheck(n):
    if n is None:
        return jsonify({'Message': 'Data tidak boleh kosong'}), 400

def filter(p):
    ptrn = r'^[A-Za-z0-9\s\.\-\+\*\?\/\|&;<>!@#$%^=\[\]{}()]+$'
    wrn = "Proses injeksi terdeteksi, silahkan isi dengan data yang benar"
    if not re.match(ptrn, p):
        return jsonify({'Message': wrn}), 400

def check(data):
    if not re.match(r'^[A-Za-z0-9_-]+$', data):
        return jsonify({'Message': 'Proses injeksi terdeteksi, silahkan isi dengan data yang benar'}), 400

def lendata(data):
    if len(data) == 0:
        return jsonify({'Message': 'Belum ada data diinputkan'}), 404

@app.route('/', methods=['GET'])
def get():
    response = lendata(alldata)
    if response:
        return response
    return jsonify(list(alldata.values()))

@app.route('/data', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        g1 = request.args.get('CODE')
        g2 = request.args.get('NPK')
        g3 = request.args.get('LINE')
        g5 = request.args.get('DATE')
        
        endpoint = [g1, g2, g3, g5]
        for i in endpoint:
            response = nullCheck(i)
            if response:
                return response
            response = check(i)
            if response:
                return response
            xssClean(i)
            response = filter(i)
            if response:
                return response

        key = (g1, g2, g3, g5)
        response = lendata(alldata)
        if response:
            return response
        if key in alldata:
            return jsonify(alldata[key]), 200
        else:
            return jsonify({'Message': 'Data tidak ditemukan'}), 404

    elif request.method == 'POST':
        post = ['CODE', 'NPK', 'LINE', 'STATUS_JUDGEMENT', 'DATE', 'CREATED_AT', 'STATUS_DEVICE', 'COUNTER', 'SPARE']
        p1 = request.form.get(post[0])
        p2 = request.form.get(post[1])
        p3 = request.form.get(post[2])
        p4 = request.form.get(post[3])
        p5 = request.form.get(post[4])
        p6 = request.form.get(post[5])
        p7 = dm.strftime(dm.now(), '%d/%m/%Y_%H:%M:%S')
        p8 = request.form.get(post[6])
        p9 = request.form.get(post[7])
        p10 = request.form.get(post[8])

        endpoint = [p1, p2, p3, p4, p8, p9, p10]
        for i in endpoint:
            response = nullCheck(i)
            if response:
                return response
            response = check(i)
            if response:
                return response
            xssClean(i)
            response = filter(i)
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

        alldata[key] = data
        return jsonify({'Message': 'Data berhasil ditambahkan'}), 201

if __name__ == '__main__':
    app.run(debug=True, port=1234)