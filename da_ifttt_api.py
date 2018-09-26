from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import logging

import data.mongo_setup as mongo_setup


app_ifttt_channel_key = 'dV8XXrIUIoBe9jK04jlXA0hkzf1El4wBjbaW9VezxnCxZAINw7bnoFxfej-9fWBk'

app = Flask(__name__, static_url_path='/static')
handler = logging.FileHandler('da_ifttt_api.log')
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

CORS(app)
api = Api(app)

# databases initiators both sql-lite and mongodb
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '0n3m0r371me'

db = SQLAlchemy(app)

from data_auth import init_database

init_database.init_database()

mongo_setup.global_init()
# end

# JWT support configuration
app.config['JWT_SECRET_KEY'] = '0n3m0r371me'
app.config['JWT_BLACKLIST_ENABLES'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

jwt = JWTManager(app)

from data_auth.models import RevokedTokenModel


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    authorities = [authority.authority_name for authority in user.authorities]
    return {'authorities': authorities}


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.email
# end


from rest_api.ifttt_endpoints import SensorActivado, SensorNormal, StatusEndPoint, TestSetupEndPoint
from rest_api.user_endpoints import UserLogin, Account
from rest_api.complejo_endpoints import GuardarComplejo, EditarComplejo, ObtenerComplejos, ObtenerComplejoPorId, \
    BorrarComplejoPorId
from rest_api.habitacion_endpoints import GuardarHabitacion, ObtenerHabitaciones, EditarHabitacion, \
    ObtenerHabitacionPorId, BorrarHabitacionPorId, ObtenerHabitacionesPorComplejoId, ObtenerServiciosPorHabitacion
from rest_api.sensor_endpoint import GuardarSensor, EditarSensor, ObtenerSensores, ObtenerSensorPorId, BorrarSensor, \
    DispositivosSinRegistrar, ObtenerSensoresPorIds, ObtenerSensoresPorHabitacion, ObtenerSensoresSinVincular, \
    AgregarSensorListaServicio, QuitarSensorListaServicio

# ifttt
api.add_resource(SensorActivado, '/api/ifttt/v1/actions/sensoractivado')
api.add_resource(SensorNormal, '/api/ifttt/v1/actions/sensornormal')
api.add_resource(StatusEndPoint, '/api/ifttt/v1/status')
api.add_resource(TestSetupEndPoint, '/api/ifttt/v1/test/setup')

# user
api.add_resource(UserLogin, '/api/app/user/authenticate')
api.add_resource(Account, '/api/app/user/account')

# complejos
api.add_resource(GuardarComplejo, '/api/app/user/complejos')
api.add_resource(ObtenerComplejos, '/api/app/user/complejos')
api.add_resource(EditarComplejo, '/api/app/user/complejos/<string:complejo_id>')
api.add_resource(ObtenerComplejoPorId, '/api/app/user/complejos/<string:complejo_id>')
api.add_resource(BorrarComplejoPorId, '/api/app/user/complejos/<string:complejo_id>')

# habitaciones
api.add_resource(GuardarHabitacion, '/api/app/user/habitaciones')
api.add_resource(ObtenerHabitaciones, '/api/app/user/habitaciones')
api.add_resource(EditarHabitacion, '/api/app/user/habitaciones/<string:habitacion_id>')
api.add_resource(ObtenerHabitacionPorId, '/api/app/user/habitaciones/<string:habitacion_id>')
api.add_resource(BorrarHabitacionPorId, '/api/app/user/habitaciones/<string:habitacion_id>')
api.add_resource(ObtenerHabitacionesPorComplejoId, '/api/app/user/habitaciones_complejo/<string:complejo_id>')
api.add_resource(ObtenerServiciosPorHabitacion, '/api/app/user/habitaciones_servicios/<string:habitacion_id>')


# sensores
api.add_resource(GuardarSensor, '/api/app/user/sensores')
api.add_resource(ObtenerSensores, '/api/app/user/sensores')
api.add_resource(ObtenerSensorPorId, '/api/app/user/sensores/<string:sensor_id>')
api.add_resource(EditarSensor, '/api/app/user/sensores/<string:sensor_id>')
api.add_resource(BorrarSensor, '/api/app/user/sensores/<string:sensor_id>')
api.add_resource(ObtenerSensoresPorIds, '/api/app/user/sensores_batch')
api.add_resource(ObtenerSensoresSinVincular, '/api/app/user/sensores_sin_vincular')
api.add_resource(ObtenerSensoresPorHabitacion, '/api/app/user/sensores_por_habitacion/<string:habitacion_id>')
api.add_resource(AgregarSensorListaServicio, '/api/app/user/sensor_agregar_servicio/<string:sensor_id>')
api.add_resource(QuitarSensorListaServicio, '/api/app/user/sensor_quitar_servicio/<string:sensor_id>')

# dispositivos
api.add_resource(DispositivosSinRegistrar, '/api/app/user/dispositivos_sin_registrar')

