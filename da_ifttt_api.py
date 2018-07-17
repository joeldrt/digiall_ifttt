from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import datetime
import logging

app_ifttt_channel_key = 'dV8XXrIUIoBe9jK04jlXA0hkzf1El4wBjbaW9VezxnCxZAINw7bnoFxfej-9fWBk'

app = Flask(__name__, static_url_path='/static')
handler = logging.FileHandler('da_ifttt_api.log')
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

CORS(app)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


parser = reqparse.RequestParser()
parser.add_argument('actionFields', type=dict, required=True)
parser.add_argument('ifttt_source', type=dict, required=True)
parser.add_argument('user', type=dict)


class TestAction(Resource):
    def post(self):
        for key, value in request.headers:
            logging.debug('Headers-------------------')
            logging.debug('{}: {}'.format(key, value))

        data = parser.parse_args()

        for key, value in data['actionFields']:
            logging.debug('Action fields ------------')
            logging.debug('{}: {}'.format(key, value))

        for key, value in data['ifttt_source']:
            logging.debug('Ifttt source -------------')
            logging.debug('{}: {}'.format(key, value))

        response = {'id': datetime.datetime.now,
                    'url': 'http://www.digiall.mx'}

        reasponse_data = list()
        reasponse_data.append(response)

        return {'data': reasponse_data}


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

        return {'data': {'test_past': True}}


api.add_resource(HelloWorld, '/api/helloworld')
api.add_resource(TestAction, '/api/ifttt/v1/actions/testaction')
api.add_resource(StatusEndPoint, '/api/ifttt/v1/status')

if __name__ == '__main__':
    app.run(debug=True)
