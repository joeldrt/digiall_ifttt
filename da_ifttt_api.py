from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse
import datetime
import logging
import json

app_ifttt_channel_key = 'dV8XXrIUIoBe9jK04jlXA0hkzf1El4wBjbaW9VezxnCxZAINw7bnoFxfej-9fWBk'

app = Flask(__name__, static_url_path='/static')
handler = logging.FileHandler('da_ifttt_api.log')
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('actionFields', type=dict, required=True)
parser.add_argument('ifttt_source', type=dict)
parser.add_argument('user', type=dict)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class TestAction(Resource):
    def post(self):
        for key, value in request.headers:
            logging.debug('Headers-------------------')
            logging.debug('{}: {}'.format(key, value))

        def myconverter(o):
            if isinstance(o, datetime.datetime):
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

        data = parser.parse_args()

        for key in dict(data['actionFields']).keys():
            logging.debug('Action fields ------------')
            logging.debug('{}: {}'.format(key, dict(data['actionFields']).get(key)))

        if data['ifttt_source']:
            for key in dict(data['ifttt_source']).keys():
                logging.debug('Ifttt source -------------')
                logging.debug('{}: {}'.format(key, dict(data['actionFields']).get(key)))

        response = {'id': datetime.datetime.now(),
                    'url': 'http://www.digiall.mx'}

        response_data = list()
        response_data.append(response)

        last_object = {'data': response_data}

        resp = Response(json.dumps(last_object, ensure_ascii=False, default=myconverter), mimetype='application/json; charset=utf-8')

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

        return {'data': {'test_pass': True}}


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

        response_data = {'data': {'test_pass': 'lastname is Davila'}}

        resp = Response(json.dumps(response_data, ensure_ascii=False), mimetype='application/json; charset=utf-8')

        return resp


api.add_resource(HelloWorld, '/api/helloworld')
api.add_resource(TestAction, '/api/ifttt/v1/actions/testaction')
api.add_resource(StatusEndPoint, '/api/ifttt/v1/status')
api.add_resource(TestSetupEndPoint, '/api/ifttt/v1/test/setup')

if __name__ == '__main__':
    app.run(debug=True)
