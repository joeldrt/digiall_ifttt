from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import logging

import data.mongo_setup as mongo_setup

app_ifttt_channel_key = 'dV8XXrIUIoBe9jK04jlXA0hkzf1El4wBjbaW9VezxnCxZAINw7bnoFxfej-9fWBk'

app = Flask(__name__, static_url_path='/static')
handler = logging.FileHandler('da_ifttt_api.log')
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

CORS(app)
api = Api(app)

mongo_setup.global_init()


from rest_services.ifttt_endpoints import HelloWorld, SensorActivado, SensorNormal, StatusEndPoint, TestSetupEndPoint
from rest_services.app_endpoints import MostrarRegistros, CreateExcelFile

api.add_resource(HelloWorld, '/api/helloworld')
api.add_resource(SensorActivado, '/api/ifttt/v1/actions/sensoractivado')
api.add_resource(SensorNormal, '/api/ifttt/v1/actions/sensornormal')
api.add_resource(StatusEndPoint, '/api/ifttt/v1/status')
api.add_resource(TestSetupEndPoint, '/api/ifttt/v1/test/setup')

api.add_resource(MostrarRegistros, '/api/registros')
api.add_resource(CreateExcelFile, '/api/descargar_excel')
