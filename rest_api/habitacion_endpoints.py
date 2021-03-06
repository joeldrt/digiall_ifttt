from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required,
                                get_jwt_identity)

from services import habitacion_service
from services import complejo_service

guardar_habitacion_parser = reqparse.RequestParser(bundle_errors=True)
guardar_habitacion_parser.add_argument('complejo_id', type=str, required=True)
guardar_habitacion_parser.add_argument('nombre', type=str, required=True)
guardar_habitacion_parser.add_argument('tipo', type=str)
guardar_habitacion_parser.add_argument('precio_base', type=float)
guardar_habitacion_parser.add_argument('usa_servicio_doble_sensor', type=bool)
guardar_habitacion_parser.add_argument('hora_extra', type=float)
guardar_habitacion_parser.add_argument('persona_extra', type=float)


class GuardarHabitacion(Resource):
    @jwt_required
    def post(self):
        usuario_propietario = get_jwt_identity()
        data = guardar_habitacion_parser.parse_args()

        complejo_id = data['complejo_id']
        nombre = data['nombre']
        tipo = data['tipo']
        precio_base = data['precio_base']
        hora_extra = data['hora_extra']
        persona_extra = data['persona_extra']

        try:
            habitacion = habitacion_service.agregar(usuario_propietario=usuario_propietario,
                                                    complejo_id=complejo_id,
                                                    nombre=nombre,
                                                    tipo=tipo,
                                                    precio_base=precio_base,
                                                    hora_extra=hora_extra,
                                                    persona_extra=persona_extra)

        except Exception as exception:
            return {'message': 'Error del servidor al guardar la habitación'}, 500

        return habitacion.to_dict()


editar_habitacion_parser = reqparse.RequestParser(bundle_errors=True)
editar_habitacion_parser.add_argument('complejo_id', type=str, required=True)
editar_habitacion_parser.add_argument('nombre', type=str, required=True)
editar_habitacion_parser.add_argument('tipo', type=str)
editar_habitacion_parser.add_argument('precio_base', type=float)
editar_habitacion_parser.add_argument('hora_extra', type=float)
editar_habitacion_parser.add_argument('persona_extra', type=float)


class EditarHabitacion(Resource):
    @jwt_required
    def put(self, habitacion_id):
        usuario_propietario = get_jwt_identity()

        if not habitacion_service.habitacion_le_pertenece_a_propietario(usuario_propietario=usuario_propietario,
                                                                        habitacion_id=habitacion_id):
            return {'message': 'La habitación que se desea editar no le pertenece al propietario'}, 403

        data = editar_habitacion_parser.parse_args()

        nombre = data['nombre']
        tipo = data['tipo']
        precio_base = data['precio_base']
        hora_extra = data['hora_extra']
        persona_extra = data['persona_extra']

        try:
            habitacion = habitacion_service.editar(habitacion_id=habitacion_id,
                                                   nombre=nombre,
                                                   tipo=tipo,
                                                   precio_base=precio_base,
                                                   hora_extra=hora_extra,
                                                   persona_extra=persona_extra)

        except Exception as exception:
            return {'message': 'Error del servidor al editar la habitación'}, 500

        return habitacion.to_dict()


class ObtenerHabitaciones(Resource):
    @jwt_required
    def get(self):
        usuario_propietario = get_jwt_identity()

        try:
            habitaciones_objs = habitacion_service.obtener_habitaciones_por_usuario_propietario(
                usuario_propietario=usuario_propietario)

            habitaciones = [
                habitacion.to_dict() for habitacion in habitaciones_objs
            ]
        except Exception as exception:
            return {'message': 'Error al obtener habitaciones por propietario'}, 500

        return habitaciones


class ObtenerHabitacionPorId(Resource):
    @jwt_required
    def get(self, habitacion_id):
        usuario_propietario = get_jwt_identity()

        if not habitacion_service.habitacion_le_pertenece_a_propietario(usuario_propietario=usuario_propietario,
                                                                        habitacion_id=habitacion_id):
            return {'message': 'La habitación que se desea obtener no le pertenece al propietario'}, 403

        try:
            habitacion = habitacion_service.obtener_habitacion_por_id(habitacion_id=habitacion_id)
        except Exception as exception:
            return {'message': 'Error al obtener habitaciones por id'}, 500

        return habitacion.to_dict()


class BorrarHabitacionPorId(Resource):
    @jwt_required
    def delete(self, habitacion_id):
        usuario_propietario = get_jwt_identity()
        try:
            if habitacion_service.borrar_habitacion_por_id(usuario_propietario=usuario_propietario,
                                                           habitacion_id=habitacion_id):
                return {'message': 'Complejo Borrado'}, 200
            else:
                return {'message': 'Error al borrar la habitación'}, 500
        except Exception as exception:
            return {'message': 'Error al borrar la habitación'}, 500


class ObtenerHabitacionesPorComplejoId(Resource):
    @jwt_required
    def get(self, complejo_id):
        usuario_propietario = get_jwt_identity()

        if not complejo_service.complejo_le_pertenece_a_propietario(usuario_propietario=usuario_propietario,
                                                                    complejo_id=complejo_id):
            return {'message': 'El complejo no le pertenece al propietario'}, 403

        try:
            habitaciones_objs = habitacion_service.obtener_habitaciones_por_complejo(complejo_id=complejo_id)

            habitaciones = [
                habitacion.to_dict() for habitacion in habitaciones_objs
            ]
        except Exception as exception:
            return {'message': 'Error al recuperar las habitaciones por complejo'}, 500

        return habitaciones


obtener_servicios_por_habitacion_parser = reqparse.RequestParser(bundle_errors=True)
obtener_servicios_por_habitacion_parser.add_argument('fecha_inicial', type=str, required=True, location='args')
obtener_servicios_por_habitacion_parser.add_argument('fecha_final', type=str, required=True, location='args')


class ObtenerServiciosPorHabitacion(Resource):
    @jwt_required
    def get(self, habitacion_id):
        usuario_propietario = get_jwt_identity()

        data = obtener_servicios_por_habitacion_parser.parse_args()
        fecha_inicial = data['fecha_inicial']
        fecha_final = data['fecha_final']

        if not habitacion_service.habitacion_le_pertenece_a_propietario(usuario_propietario=usuario_propietario,
                                                                        habitacion_id=habitacion_id):
            return {'message': 'La habitación no le pertenece al propietario'}, 403

        try:
            servicios_habitacion = habitacion_service.obtener_servicios_por_habitacion(habitacion_id=habitacion_id,
                                                                                       fecha_inicial=fecha_inicial,
                                                                                       fecha_final=fecha_final)
        except Exception as exception:
            return {'message': 'Error al recuperar el numero de servicios por habitación'}, 500

        return servicios_habitacion


obtener_servicios_por_habitacion_parser = reqparse.RequestParser(bundle_errors=True)
obtener_servicios_por_habitacion_parser.add_argument('fecha_inicial', type=str, required=True, location='args')
obtener_servicios_por_habitacion_parser.add_argument('fecha_final', type=str, required=True, location='args')


class ObtenerRegistrosPorHabitacion(Resource):
    @jwt_required
    def get(self, habitacion_id):
        usuario_propietario = get_jwt_identity()

        data = obtener_servicios_por_habitacion_parser.parse_args()
        fecha_inicial = data['fecha_inicial']
        fecha_final = data['fecha_final']

        if not habitacion_service.habitacion_le_pertenece_a_propietario(usuario_propietario=usuario_propietario,
                                                                        habitacion_id=habitacion_id):
            return {'message': 'La habitación no le pertenece al propietario'}, 403

        try:
            registros_objs = habitacion_service.obtener_registros_por_habitacion(habitacion_id=habitacion_id,
                                                                                 fecha_inicial=fecha_inicial,
                                                                                 fecha_final=fecha_final)

            registros = [
                registro.to_dict() for registro in registros_objs
            ]

        except Exception as exception:
            return {'message': 'Error al recuperar el numero de servicios por habitación'}, 500

        return registros
