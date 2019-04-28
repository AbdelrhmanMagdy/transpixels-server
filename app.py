from flask import Flask, request
import os
import ocr
import mapLogic as ml
from os import environ
from flask import jsonify

app = Flask(__name__)


@app.route('/mark', methods = ['GET', 'POST'])
def mark():
    if request.method == 'POST':
        f = request.files['img']
        f.save('sora.jpg')
        res = ocr.run('sora.jpg')
        if res != '':
            return jsonify({
                "src": ml.mark(res),
                "location": res 
            })
    return 'Service Failed!', 400

@app.route('/locate', methods = ['GET', 'POST'])
def locate():
    if request.method == 'GET':
        src = request.args.get('src')
        dst = request.args.get('dst')
        return jsonify({
            "src":ml.locate(src, dst)
        })
    return 'Service Failed!', 400

@app.route('/dummyMark', methods = ['GET', 'POST'])
def dummyAPI():
    if request.method == 'POST':
        # f = request.files['img']
        # f.save('sora.jpg')
        res = '344'# ocr.run('sora.jpg')
        if res != '':
            return jsonify({
                "src": ml.mark(res),
                "location": res 
            })
    return 'Service Failed!', 400

if __name__ == '__main__':
    app.run(debug=False, port=environ.get("PORT", 5000), host='0.0.0.0')