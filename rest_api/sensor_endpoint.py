from flask import request
from flask_restful import Resource

from services import sensor_service


class GuardarSensor(Resource):
    def post(self):
        data = request.get_json()

        usuario_propietario = data['usuario_propietario']
        dispositivo_id = data['dispositivo_id']
        nombre = data['nombre']
        tipo_sensor = data['tipo_sensor']

        sensor = sensor_service.agregar(usuario_propietario=usuario_propietario,
                                        dispositivo_id=dispositivo_id,
                                        nombre=nombre,
                                        tipo_sensor=tipo_sensor)

        return sensor.to_dict()


class BorrarSensor(Resource):
    def delete(self, sensor_id):
        return sensor_service.borrar_sensor_por_id(sensor_id)


class DispositivosSinRegistrar(Resource):
    def get(self):
        usuario_propietario = request.args.get('usuario_propietario')

        dispositivos_registrados = sensor_service\
            .dispositivos_id_sin_registrar_por_usuario_propietario(usuario_propietario=usuario_propietario)

        return dispositivos_registrados

