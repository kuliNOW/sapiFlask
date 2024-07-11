from flask import Flask, request, jsonify

app = Flask(__name__)

alldata = {}

@app.route('/', methods=['GET'])
def get():
    if len(alldata) == 0:
        return jsonify({'Message': 'Belum ada data diinputkan'}), 404
    return jsonify(list(alldata.values()))

@app.route('/data', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        g1 = request.args.get('CODE')
        g2 = request.args.get('NPK')
        g3 = request.args.get('LINE')
        g5 = request.args.get('DATE')

        key = (g1, g2, g3, g5)
        if len(alldata) == 0:
            return jsonify({'Message': 'Belum ada data diinputkan'}), 404
        if key in alldata:
            return jsonify(alldata[key]), 201
        else:
            return jsonify({'Message': 'Data tidak ditemukan'}), 404

    elif request.method == 'POST':
        p1 = request.form.get('CODE')
        p2 = request.form.get('NPK')
        p3 = request.form.get('LINE')
        p4 = request.form.get('STATUS_JUDGEMENT')
        p5 = request.form.get('DATE')
        p6 = request.form.get('CREATED_AT')
        p7 = request.form.get('UPDATED_AT')
        p8 = request.form.get('STATUS_DEVICE')
        p9 = request.form.get('COUNTER')
        p10 = request.form.get('SPARE')

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
