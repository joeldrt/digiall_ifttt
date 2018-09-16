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


from rest_api.ifttt_endpoints import HelloWorld, SensorActivado, SensorNormal, StatusEndPoint, TestSetupEndPoint
from rest_api.complejo_endpoints import GuardarComplejo, ObtenerComplejos, ObtenerComplejoPorId, BorrarComplejoPorId
from rest_api.habitacion_endpoints import GuardarHabitacion, ObtenerHabitaciones, ObtenerHabitacionPorId, \
    GuardarExtrasHabitacion

# ifttt
api.add_resource(HelloWorld, '/api/helloworld')
api.add_resource(SensorActivado, '/api/ifttt/v1/actions/sensoractivado')
api.add_resource(SensorNormal, '/api/ifttt/v1/actions/sensornormal')
api.add_resource(StatusEndPoint, '/api/ifttt/v1/status')
api.add_resource(TestSetupEndPoint, '/api/ifttt/v1/test/setup')

# complejos
api.add_resource(GuardarComplejo, '/api/app/user/complejos')
api.add_resource(ObtenerComplejos, '/api/app/user/complejos')
api.add_resource(ObtenerComplejoPorId, '/api/app/user/complejos/<string:complejo_id>')
api.add_resource(BorrarComplejoPorId, '/api/app/user/complejos/<string:complejo_id>')

# habitaciones
api.add_resource(GuardarHabitacion, '/api/app/user/habitaciones')
api.add_resource(ObtenerHabitaciones, '/api/app/user/habitaciones')
api.add_resource(ObtenerHabitacionPorId, '/api/app/user/habitaciones/<string:habitacion_id>')
api.add_resource(GuardarExtrasHabitacion, '/api/app/user/habitaciones/<string:habitacion_id>/extras')
