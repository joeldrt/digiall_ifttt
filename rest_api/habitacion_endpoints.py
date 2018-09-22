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
guardar_habitacion_parser.add_argument('dispositivos_ids_servicio_doble', action='append')
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
        usa_servicio_doble_sensor = data['usa_servicio_doble_sensor']
        dispositivos_ids_servicio_doble = data['dispositivos_ids_servicio_doble']
        hora_extra = data['hora_extra']
        persona_extra = data['persona_extra']

        try:
            habitacion = habitacion_service.agregar(usuario_propietario=usuario_propietario,
                                                    complejo_id=complejo_id,
                                                    nombre=nombre,
                                                    tipo=tipo,
                                                    precio_base=precio_base,
                                                    usa_servicio_doble_sensor=usa_servicio_doble_sensor,
                                                    dispositivos_ids_servicio_doble=dispositivos_ids_servicio_doble,
                                                    hora_extra=hora_extra,
                                                    persona_extra=persona_extra)

        except Exception as exception:
            return {'message': 'Error al guardar en la base de datos'}, 500

        return habitacion.to_dict()


editar_habitacion_parser = reqparse.RequestParser(bundle_errors=True)
editar_habitacion_parser.add_argument('complejo_id', type=str, required=True)
editar_habitacion_parser.add_argument('nombre', type=str, required=True)
editar_habitacion_parser.add_argument('tipo', type=str)
editar_habitacion_parser.add_argument('precio_base', type=float)
editar_habitacion_parser.add_argument('usa_servicio_doble_sensor', type=bool)
editar_habitacion_parser.add_argument('dispositivos_ids_servicio_doble', action='append')
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
        usa_servicio_doble_sensor = data['usa_servicio_doble_sensor']
        dispositivos_ids_servicio_doble = data['dispositivos_ids_servicio_doble']
        hora_extra = data['hora_extra']
        persona_extra = data['persona_extra']

        try:
            habitacion = habitacion_service.editar(habitacion_id=habitacion_id,
                                                   nombre=nombre,
                                                   tipo=tipo,
                                                   precio_base=precio_base,
                                                   usa_servicio_doble_sensor=usa_servicio_doble_sensor,
                                                   dispositivos_ids_servicio_doble=dispositivos_ids_servicio_doble,
                                                   hora_extra=hora_extra,
                                                   persona_extra=persona_extra)

        except Exception as exception:
            return {'message': exception}, 500

        return habitacion.to_dict()


class ObtenerHabitaciones(Resource):
    @jwt_required
    def get(self):
        usuario_propietario = get_jwt_identity()

        habitaciones_objs = habitacion_service.obtener_habitaciones_por_usuario_propietario(
            usuario_propietario=usuario_propietario)

        habitaciones = [
            habitacion.to_dict() for habitacion in habitaciones_objs
        ]

        return habitaciones


class ObtenerHabitacionPorId(Resource):
    @jwt_required
    def get(self, habitacion_id):
        usuario_propietario = get_jwt_identity()

        if not habitacion_service.habitacion_le_pertenece_a_propietario(usuario_propietario=usuario_propietario,
                                                                        habitacion_id=habitacion_id):
            return {'message': 'La habitación que se desea obtener no le pertenece al propietario'}, 403

        habitacion = habitacion_service.obtener_habitacion_por_id(usuario_propietario=usuario_propietario,
                                                                  habitacion_id=habitacion_id)
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
                return {'message': 'Error al borrar el complejo'}, 500
        except Exception as exception:
            return {'message': exception}, 500


class ObtenerHabitacionesPorComplejoId(Resource):
    @jwt_required
    def get(self, complejo_id):
        usuario_propietario = get_jwt_identity()

        if not complejo_service.complejo_le_pertenece_a_propietario(usuario_propietario=usuario_propietario,
                                                                    complejo_id=complejo_id):
            return {'message': 'El complejo no le pertenece al propietario'}, 403

        habitaciones_objs = habitacion_service.obtener_habitaciones_por_complejo(complejo_id=complejo_id)

        habitaciones = [
            habitacion.to_dict() for habitacion in habitaciones_objs
        ]

        return habitaciones
