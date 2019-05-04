from flask import Flask, request
import os
import ocr
import mapLogic as ml
from os import environ
from flask import jsonify
import pytesseract as pts

app = Flask(__name__)


@app.route('/mark', methods = ['GET', 'POST'])
def mark():
    tempImg = '/home/abdelrhmanmagdy/Desktop/GP/temp.jpg'
    if request.method == 'POST':
        f = request.files.get('image')
        f.save(tempImg)
        try:
            ocrOut = ocr.run(tempImg)
        except:
            ocrOut = pts.image_to_string(tempImg)
        # Trying to find a valid 3 digit numbers from the ocr output string
        print('ocrOut',ocrOut)
        res = ocrOut if ocrOut else None
        validHall = ''
        if res:
            numsInStr = [int(s) for s in res.split() if s.isdigit()]
            for i in numsInStr:
                if len(str(i)) == 3:
                    validHall = str(i)
            
        try:
            # Get the map marked at certain valid hall
            src = ml.mark(validHall)
        except:
            src = None
        return jsonify({
            "src": src,
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

if __name__ == '__main__':
    app.run(debug=False, port=environ.get("PORT", 5000), host='0.0.0.0')