from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import datetime
import logging

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


api.add_resource(HelloWorld, '/api/helloworld')
api.add_resource(TestAction, '/api/ifttt/v1/actions/testaction')

if __name__ == '__main__':
    app.run(debug=True)
