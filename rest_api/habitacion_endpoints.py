from flask import request
from flask_restful import Resource

from services import  habitacion_service


class GuardarHabitacion(Resource):
    def post(self):
        data = request.get_json()

        complejo_id = data['complejo_id']
        nombre = data['nombre']
        tipo = data['tipo']
        precio_base = data['precio_base']

        habitacion = habitacion_service.agregar(complejo_id=complejo_id,
                                                nombre=nombre,
                                                tipo=tipo,
                                                precio_base=precio_base)

        return habitacion.to_dict()


class ObtenerHabitaciones(Resource):
    def get(self):
        complejo_id = str(request.args.get('complejo_id'))
        habitaciones_obj = habitacion_service.obtener_habitaciones_por_complejo(complejo_id=complejo_id)
        habitaciones = [
            habitacion.to_dict() for habitacion in habitaciones_obj
        ]
        return habitaciones


class ObtenerHabitacionPorId(Resource):
    def get(self, habitacion_id):
        habitacion = habitacion_service.obtener_habitacion_por_id(habitacion_id)
        return habitacion.to_dict()


class GuardarExtrasHabitacion(Resource):
    def post(self, habitacion_id):
        data = request.get_json()

        hora_extra = data['hora_extra']
        persona_extra = data['persona_extra']

        extras_habitacion = habitacion_service.generar_extras_habitacion(hora_extra=hora_extra,
                                                                         persona_extra=persona_extra)

        habitacion = habitacion_service.agregar_extras_habitacion(habitacion_id=habitacion_id,
                                                                  extras_habitacion=extras_habitacion)

        return habitacion.to_dict()
