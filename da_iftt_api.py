from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
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


api.add_resource(HelloWorld, '/api/helloworld')

if __name__ == '__main__':
    app.run(debug=True)
