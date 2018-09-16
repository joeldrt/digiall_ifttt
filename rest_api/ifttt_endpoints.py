from flask import request, Response
from flask_restful import Resource
from datetime import datetime
import json

import logging

# data services
from services import registro_sensor_service as registro_service

from da_ifttt_api import app_ifttt_channel_key

ABIERTO = 'ABIERTO'
CERRADO = 'CERRADO'


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class SensorActivado(Resource):
    def post(self):

        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()

        errors_array = list()

        channel_key = request.headers['IFTTT-Channel-Key']
        if channel_key != app_ifttt_channel_key:
            error = {'message': 'INVALID IFTTT-Channel-Key'}
            errors_array.append(error)
            error_object = {'errors': errors_array}

            resp = Response(json.dumps(error_object, ensure_ascii=False, default=myconverter),
                            mimetype='application/json; charset=utf-8', status=401)

            return resp

        data = request.get_json()

        print("{} SENSOR ACTIVADO ----------------".format(datetime.now()))

        if 'actionFields' not in dict(data).keys():
            error = {'message': 'actionFields key is missing'}
            errors_array.append(error)
            error_object = {'errors': errors_array}
            resp = Response(json.dumps(error_object, ensure_ascii=False, default=myconverter),
                            mimetype='application/json; charset=utf-8', status=400)
            return resp

        if 'sensor_id' not in dict(data['actionFields']).keys():
            error = {'message': 'missing sensor_id value'}
            errors_array.append(error)
            error_object = {'errors': errors_array}
            resp = Response(json.dumps(error_object, ensure_ascii=False, default=myconverter),
                            mimetype='application/json; charset=utf-8', status=400)
            return resp

        dispositivo_id = data['actionFields']['sensor_id']
        print("dispositivo_id: {}".format(dispositivo_id))

        if 'SENSOR-CUARTO-SKIP' == dispositivo_id:
            error = {'message': 'Sensor Id not registered'}
            errors_array.append(error)
            error2 = {'status': 'SKIP', 'message': 'ID_not accepted'}
            errors_array.append(error2)
            error_object = {'errors': errors_array}
            resp = Response(json.dumps(error_object, ensure_ascii=False, default=myconverter),
                            mimetype='application/json; charset=utf-8', status=400)
            return resp

        if 'reported_at' not in dict(data['actionFields']).keys():
            error = {'message': 'missing reported_at value'}
            errors_array.append(error)
            error_object = {'errors': errors_array}
            resp = Response(json.dumps(error_object, ensure_ascii=False, default=myconverter),
                            mimetype='application/json; charset=utf-8', status=400)
            return resp

        reported_at = data['actionFields']['reported_at']

        print("reported_at: {}".format(reported_at))

        registro_sensor = registro_service.registrar_apertura(dispositivo_id, reported_at)

        response = {'id': str(registro_sensor.id),
                    'url': 'http://www.digiall.mx'}

        response_data = list()
        response_data.append(response)

        last_object = {'data': response_data}

        resp = Response(json.dumps(last_object, ensure_ascii=False, default=myconverter),
                        mimetype='application/json; charset=utf-8')

        return resp


class SensorNormal(Resource):
    def post(self):

        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()

        errors_array = list()

        channel_key = request.headers['IFTTT-Channel-Key']
        if channel_key != app_ifttt_channel_key:
            error = {'message': 'INVALID IFTTT-Channel-Key'}
            errors_array.append(error)
            error_object = {'errors': errors_array}

            resp = Response(json.dumps(error_object, ensure_ascii=False, default=myconverter),
                            mimetype='application/json; charset=utf-8', status=401)

            return resp

        data = request.get_json()

        print("{} SENSOR REGRESANDO A LA NORMALIDAD ----------------".format(datetime.now()))

        if 'actionFields' not in dict(data).keys():
            error = {'message': 'actionFields key is missing'}
            errors_array.append(error)
            error_object = {'errors': errors_array}
            resp = Response(json.dumps(error_object, ensure_ascii=False, default=myconverter),
                            mimetype='application/json; charset=utf-8', status=400)
            return resp

        if 'sensor_id' not in dict(data['actionFields']).keys():
            error = {'message': 'missing sensor_id value'}
            errors_array.append(error)
            error_object = {'errors': errors_array}
            resp = Response(json.dumps(error_object, ensure_ascii=False, default=myconverter),
                            mimetype='application/json; charset=utf-8', status=400)
            return resp

        dispositivo_id = data['actionFields']['sensor_id']
        print("sensor_id: {}".format(dispositivo_id))

        if 'SENSOR-CUARTO-SKIP' == dispositivo_id:
            error = {'message': 'Sensor Id not registered'}
            errors_array.append(error)
            error2 = {'status': 'SKIP', 'message': 'ID_not accepted'}
            errors_array.append(error2)
            error_object = {'errors': errors_array}
            resp = Response(json.dumps(error_object, ensure_ascii=False, default=myconverter),
                            mimetype='application/json; charset=utf-8', status=400)
            return resp

        if 'reported_at' not in dict(data['actionFields']).keys():
            error = {'message': 'missing reported_at value'}
            errors_array.append(error)
            error_object = {'errors': errors_array}
            resp = Response(json.dumps(error_object, ensure_ascii=False, default=myconverter),
                            mimetype='application/json; charset=utf-8', status=400)
            return resp

        reported_at = data['actionFields']['reported_at']

        print("reported_at: {}".format(reported_at))

        registro_sensor = registro_service.registrar_cerrado(dispositivo_id, reported_at)

        response = {'id': str(registro_sensor.id),
                    'url': 'http://www.digiall.mx'}

        response_data = list()
        response_data.append(response)

        last_object = {'data': response_data}

        resp = Response(json.dumps(last_object, ensure_ascii=False, default=myconverter),
                        mimetype='application/json; charset=utf-8')

        return resp


class StatusEndPoint(Resource):
    def get(self):
        for key, value in request.headers:
            logging.debug('Headers-------------------')
            logging.debug('{}: {}'.format(key, value))

        errors_array = list()

        if not request.headers['IFTTT-Channel-Key']:
            error = {'message': 'no IFTTT-Channel-Key header'}
            errors_array.append(error)
            return {'errors': errors_array}, 401

        channel_key = request.headers['IFTTT-Channel-Key']
        if channel_key != app_ifttt_channel_key:
            error = {'message': 'INVALID IFTTT-Channel-Key'}
            errors_array.append(error)
            return {'errors': errors_array}, 401

        logging.debug('IFTTT-Channel-Key: {}'.format(channel_key))

        return {'data': {
            'test_pass': True
        }
        }


class TestSetupEndPoint(Resource):
    def post(self):
        for key, value in request.headers:
            logging.debug('Headers-------------------')
            logging.debug('{}: {}'.format(key, value))

        errors_array = list()

        if not request.headers['IFTTT-Channel-Key']:
            error = {'message': 'no IFTTT-Channel-Key header'}
            errors_array.append(error)
            return {'errors': errors_array}, 401

        channel_key = request.headers['IFTTT-Channel-Key']
        if channel_key != app_ifttt_channel_key:
            error = {'message': 'INVALID IFTTT-Channel-Key'}
            errors_array.append(error)
            return {'errors': errors_array}, 401

        logging.debug('IFTTT-Channel-Key: {}'.format(channel_key))

        response_data = {
            "data": {
                "samples": {
                    "actions": {
                        "sensoractivado": {
                            "sensor_id": "SENSOR-CUARTO1",
                            "reported_at": "EDIFICIO1"
                        },
                        "sensornormal": {
                            "sensor_id": "SENSOR-CUARTO1",
                            "reported_at": "EDIFICIO1"
                        }
                    },
                    "actionRecordSkipping": {
                        "testaction": {
                            "sensor_id": "SENSOR-CUARTO-SKIP",
                            "reported_at": "EDIFICIO-SKIP"
                        }
                    }
                }
            }
        }

        resp = Response(json.dumps(response_data, ensure_ascii=False), mimetype='application/json; charset=utf-8')

        return resp
