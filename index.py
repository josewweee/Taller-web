#install flask
from flask import Flask, jsonify, request
#install cors
from flask_cors import CORS
#import data time
from datetime import datetime
#import median
from statistics import mode

app = Flask(__name__)
CORS(app)

tipo_medicion = {'sensor': 'HC-SR04', 'variable': 'Distancia', 'unidades': 'centimetros'}

mediciones = [
    {'fecha': '2019-08-22 14:55:00', **tipo_medicion, 'valor': 5},
    {'fecha': '2019-08-21 13:54:00', **tipo_medicion, 'valor': 6},
    {'fecha': '2019-08-20 12:53:00', **tipo_medicion, 'valor': 5},
    {'fecha': '2019-08-19 11:52:00', **tipo_medicion, 'valor': 3},
    {'fecha': '2019-08-18 10:51:00', **tipo_medicion, 'valor': 7},
]

#GET TIPO MEDICION
@app.route('/')
def get():
    return jsonify(tipo_medicion)

#GET 
@app.route('/mediciones/mode', methods=['GET'])
def getMediana():
    valores = [medicion['valor'] for medicion in mediciones]
    mediana = mode(valores)
    return jsonify(mediana)

#GETALL
@app.route('/mediciones', methods=['GET'])
def getAll():
    return jsonify(mediciones)

#POST
@app.route('/mediciones', methods=['POST'])
def postOne():
    now = datetime.now()
    body = request.json
    body['fecha'] = datetime.strftime(now,'%Y %m %d %H:%M:%S')
    mediciones.append({**body, **tipo_medicion})
    return jsonify(mediciones)

#PUT
@app.route('/mediciones/<string:fecha>', methods=['PUT'])
def putOne(fecha):
    body = request.json
    for medicion in mediciones:
        if (fecha == medicion['fecha']):
            medicion['valor'] = body['valor']
            valorModificado = medicion
    return valorModificado

#DELETE
@app.route('/mediciones/<string:fecha>', methods=['DELETE'])
def deleteOne(fecha):
    for medicion in mediciones:
        if(fecha == medicion['fecha']):
            mediciones.remove(medicion)
    return jsonify(mediciones)


#PUERTO Y AUTORUN
app.run(port=5000,debug=True)