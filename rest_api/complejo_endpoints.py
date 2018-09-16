from flask import request
from flask_restful import Resource

from services import complejo_service


class GuardarComplejo(Resource):
    def post(self):
        data = request.get_json()

        usuario_propietario = data['usuario_propietario']
        nombre = data['nombre']
        direccion = data['direccion']
        telefonos = data['telefonos']
        latitud = data['latitud']
        longitud = data['longitud']

        complejo = complejo_service.agregar(usuario_propietario=usuario_propietario,
                                            nombre=nombre,
                                            direccion=direccion,
                                            telefonos=telefonos,
                                            latitud=latitud,
                                            longitud=longitud)

        complejo = complejo_service.obtener_complejo_por_id(complejo.id)

        return complejo.to_dict()


class ObtenerComplejos(Resource):
    def get(self):
        usuario_propietario = str(request.args.get('usuario_propietario'))
        complejos_obj = complejo_service.obtener_complejos_por_propietario(usuario_propietario=usuario_propietario)
        complejos = [
            complejo.to_dict() for complejo in complejos_obj
        ]
        return complejos


class ObtenerComplejoPorId(Resource):
    def get(self, complejo_id):
        complejo = complejo_service.obtener_complejo_por_id(complejo_id)
        return complejo.to_dict()


class BorrarComplejoPorId(Resource):
    def delete(self, complejo_id):
        return complejo_service.borrar_complejo_por_id(complejo_id)
