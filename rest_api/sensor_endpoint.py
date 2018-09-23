from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required,
                                get_jwt_identity)

from services import sensor_service


guardar_sensor_parser = reqparse.RequestParser(bundle_errors=True)
guardar_sensor_parser.add_argument('dispositivo_id', type=str, required=True)
guardar_sensor_parser.add_argument('nombre', type=str, required=True)
guardar_sensor_parser.add_argument('tipo_sensor', type=str, required=True)


class GuardarSensor(Resource):
    @jwt_required
    def post(self):
        usuario_propietario = get_jwt_identity()

        data = guardar_sensor_parser.parse_args()

        dispositivo_id = data['dispositivo_id']
        nombre = data['nombre']
        tipo_sensor = data['tipo_sensor']

        try:
            sensor = sensor_service.agregar(usuario_propietario=usuario_propietario,
                                            dispositivo_id=dispositivo_id,
                                            nombre=nombre,
                                            tipo_sensor=tipo_sensor)
        except Exception as exception:
            return {'message': 'Error del servidor al tratar de guardar el sensor'}, 500

        return sensor.to_dict()


editar_sensor_parser = reqparse.RequestParser(bundle_errors=True)
editar_sensor_parser.add_argument('habitacion_id', type=str)
editar_sensor_parser.add_argument('dispositivo_id', type=str, required=True)
editar_sensor_parser.add_argument('nombre', type=str, required=True)
editar_sensor_parser.add_argument('tipo_sensor', type=str, required=True)
editar_sensor_parser.add_argument('contribuye_servicio', type=bool)


class EditarSensor(Resource):
    @jwt_required
    def put(self, sensor_id):
        usuario_propietario = get_jwt_identity()

        data = editar_sensor_parser.parse_args()
        habitacion_id = data['habitacion_id']
        dispositivo_id = data['dispositivo_id']
        nombre = data['nombre']
        tipo_sensor = data['tipo_sensor']
        contribuye_servicio = data['contribuye_servicio']

        if not sensor_service.sensor_le_pertenece_a_propietario(usuario_propietario=usuario_propietario,
                                                                sensor_id=sensor_id):
            return {'message': 'El sensor no le pertenece al propietario'}, 403

        try:
            sensor = sensor_service.editar(sensor_id=sensor_id,
                                           habitacion_id=habitacion_id,
                                           dispositivo_id=dispositivo_id,
                                           nombre=nombre,
                                           tipo_sensor=tipo_sensor,
                                           contribuye_servicio=contribuye_servicio)
        except Exception as exception:
            return {'message': 'Error del servidor al editar el registro'}, 500

        return sensor.to_dict()


class ObtenerSensores(Resource):
    @jwt_required
    def get(self):
        usuario_propietario = get_jwt_identity()

        try:
            sensores_objs = sensor_service.sensores_por_usuario_propietario(usuario_propietario=usuario_propietario)

            sensores = [
                sensor.to_dict() for sensor in sensores_objs
            ]
        except Exception as exception:
            return {'message': 'Error del servidor al recuperar los sensores'}, 500

        return sensores


class ObtenerSensorPorId(Resource):
    @jwt_required
    def get(self, sensor_id):
        usuario_propietario = get_jwt_identity()

        if not sensor_service.sensor_le_pertenece_a_propietario(usuario_propietario=usuario_propietario,
                                                                sensor_id=sensor_id):
            return {'message': 'El sensor no le pertenece al propietario'}, 403

        try:
            sensor = sensor_service.obtener_sensor_por_id(sensor_id=sensor_id)
        except Exception as exception:
            return {'message': 'Error del servidor al obtener el sensor'}, 500

        return sensor.to_dict()


class ObtenerSensoresPorIds(Resource):
    @jwt_required
    def get(self):
        usuario_propietario = get_jwt_identity()

        sensores_ids_string = str(request.args.get('sensores_ids'))
        sensores_ids = sensores_ids_string.split(',')

        try:
            sensores_objs = sensor_service.obtener_sensores_por_ids(usuario_propietario=usuario_propietario,
                                                                    sensores_ids=sensores_ids)
            sensores = [
                sensor.to_dict() for sensor in sensores_objs
            ]
        except Exception as exception:
            return {'message': 'Error del servidor al obtener los sensores'}, 500

        return sensores


class BorrarSensor(Resource):
    @jwt_required
    def delete(self, sensor_id):
        usuario_propietario = get_jwt_identity()

        if not sensor_service.sensor_le_pertenece_a_propietario(usuario_propietario=usuario_propietario,
                                                                sensor_id=sensor_id):
            return {'message': 'El sensor no le pertenece al propietario'}, 403

        try:
            respuesta = sensor_service.borrar_sensor_por_id(sensor_id=sensor_id)
        except Exception as exception:
            return {'message': 'Error del servidor al borrar el sensor'}, 500

        return {'message': respuesta}, 200


class DispositivosSinRegistrar(Resource):
    @jwt_required
    def get(self):
        usuario_propietario = get_jwt_identity()

        try:
            dispositivos_sin_registrar = sensor_service.dispositivos_id_sin_registrar_por_usuario_propietario(
                usuario_propietario=usuario_propietario)

        except Exception as exception:
            return {'message': 'Error del servidor al obtener los dispositivos'}, 500

        return dispositivos_sin_registrar


class ObtenerSensoresPorHabitacion(Resource):
    @jwt_required
    def get(self, habitacion_id):
        usuario_propietario = get_jwt_identity()

        try:
            sensores_por_habitacion_obj = sensor_service.sensores_por_habitacion_id(usuario_propietario=usuario_propietario,
                                                                                    habitacion_id=habitacion_id)

            sensores_por_habitacion = [
                sensor.to_dict() for sensor in sensores_por_habitacion_obj
            ]
        except Exception as exception:
            return {'message': 'Error del servidor al recuperar los sensores por habitacion'}, 500

        return sensores_por_habitacion


class ObtenerSensoresSinVincular(Resource):
    @jwt_required
    def get(self):
        usuario_propietario = get_jwt_identity()

        try:
            sensores_sin_vincular_obj = sensor_service.sensores_sin_vincular(usuario_propietario=usuario_propietario)

            sensores_sin_vincular = [
                sensor.to_dict() for sensor in sensores_sin_vincular_obj
            ]

        except Exception as exception:
            return {'message': 'Error del servidor al obtener los sensores'}, 500

        return sensores_sin_vincular


class AgregarSensorListaServicio(Resource):
    @jwt_required
    def put(self, sensor_id):
        usuario_propietario = get_jwt_identity()

        try:
            if not sensor_service.sensor_le_pertenece_a_propietario(usuario_propietario=usuario_propietario,
                                                                    sensor_id=sensor_id):
                return {'message': 'El sensor no le pertence al propietario'}, 403

        except Exception as exception:
            return {'message': 'Error del servidor al agregar un sensor a la lista de servicio'}, 500

        try:
            if not sensor_service.activar_sensor_contribuye_servicio(sensor_id=sensor_id):
                return {'message': 'Error al activar el switch de contribuye servicio'}, 500

        except Exception as exception:
            return {'message': 'Error del servidor al agregar un sensor a la lista de servicio'}, 500

        return {'message': 'Sensor agregado a la lista de servicio'}, 200


class QuitarSensorListaServicio(Resource):
    @jwt_required
    def put(self, sensor_id):
        usuario_propietario = get_jwt_identity()

        try:
            if not sensor_service.sensor_le_pertenece_a_propietario(usuario_propietario=usuario_propietario,
                                                                    sensor_id=sensor_id):
                return {'message': 'El sensor no le pertence al propietario'}, 403

        except Exception as exception:
            return {'message': 'Error del servidor al quitar un sensor a la lista de servicio'}, 500

        try:
            if not sensor_service.desactivar_sensor_contribuye_servicio(sensor_id=sensor_id):
                return {'message': 'Error al desactivar el switch de contribuye servicio'}, 500

        except Exception as exception:
            return {'message': 'Error del servidor al quitar un sensor a la lista de servicio'}, 500

        return {'message': 'Sensor borrado de la lista de servicio'}, 200