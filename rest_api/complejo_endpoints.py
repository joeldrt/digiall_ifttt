from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required,
                                get_jwt_identity)

from services import complejo_service

guardar_complejo_parser = reqparse.RequestParser(bundle_errors=True)
guardar_complejo_parser.add_argument('nombre', type=str, required=True)
guardar_complejo_parser.add_argument('direccion', type=str)
guardar_complejo_parser.add_argument('telefonos', action='append')
guardar_complejo_parser.add_argument('latitud', type=float)
guardar_complejo_parser.add_argument('longitud', type=float)


class GuardarComplejo(Resource):
    @jwt_required
    def post(self):
        email = get_jwt_identity()

        data = guardar_complejo_parser.parse_args()

        usuario_propietario = email
        nombre = data['nombre']
        direccion = data['direccion']
        telefonos = data['telefonos']
        latitud = data['latitud']
        longitud = data['longitud']

        try:
            complejo = complejo_service.agregar(usuario_propietario=usuario_propietario,
                                                nombre=nombre,
                                                direccion=direccion,
                                                telefonos=telefonos,
                                                latitud=latitud,
                                                longitud=longitud).to_dict()

            complejo = complejo_service.obtener_complejo_por_id(
                usuario_propietario=usuario_propietario, complejo_id=complejo['id'])

        except Exception as exception:
            return {'message': exception.message}, 500

        return complejo.to_dict()


editar_complejo_parser = reqparse.RequestParser(bundle_errors=True)
editar_complejo_parser.add_argument('id', type=str, required=True)
editar_complejo_parser.add_argument('nombre', type=str, required=True)
editar_complejo_parser.add_argument('direccion', type=str)
editar_complejo_parser.add_argument('telefonos', action='append')
editar_complejo_parser.add_argument('latitud', type=float)
editar_complejo_parser.add_argument('longitud', type=float)


class EditarComplejo(Resource):
    @jwt_required
    def put(self, complejo_id):
        usuario_propietario = get_jwt_identity()

        data = editar_complejo_parser.parse_args()

        if not complejo_id:
            return {'message': 'No se especificó ningún id de complejo'}, 400

        if not complejo_service.complejo_le_pertenece_a_propietario(usuario_propietario=usuario_propietario,
                                                                    complejo_id=complejo_id):
            return {'message': 'El complejo no le pertenece a este propietario'}, 403

        try:
            complejo = complejo_service.editar_complejo(complejo_id=data['id'],
                                                        nombre=data['nombre'],
                                                        direccion=data['direccion'],
                                                        telefonos=data['telefonos'],
                                                        latitud=data['latitud'],
                                                        longitud=data['longitud'])
        except Exception as exception:
            return {'message': exception}, 500

        return complejo.to_dict()


class ObtenerComplejos(Resource):
    @jwt_required
    def get(self):
        usuario_propietario = get_jwt_identity()
        complejos_obj = complejo_service.obtener_complejos_por_propietario(usuario_propietario=usuario_propietario)
        complejos = [
            complejo.to_dict() for complejo in complejos_obj
        ]
        return complejos


class ObtenerComplejoPorId(Resource):
    @jwt_required
    def get(self, complejo_id):
        usuario_propietario = get_jwt_identity()
        complejo = complejo_service.obtener_complejo_por_id(complejo_id=complejo_id)
        return complejo.to_dict()


class BorrarComplejoPorId(Resource):
    @jwt_required
    def delete(self, complejo_id):
        usuario_propietario = get_jwt_identity()
        try:
            if complejo_service.borrar_complejo_por_id(usuario_propietario=usuario_propietario,
                                                       complejo_id=complejo_id):
                return {'message': 'Complejo Borrado'}, 200
            else:
                return {'message': 'El complejo no le pertenece al propietario'}, 500
        except Exception as exception:
            return {'message': 'Error del servidor al borrar el complejo'}, 500


obtener_resumen_complejo_parser = reqparse.RequestParser(bundle_errors=True)
obtener_resumen_complejo_parser.add_argument('fecha_inicial', required=True, location='args')
obtener_resumen_complejo_parser.add_argument('fecha_final', required=True, location='args')


class ObtenerResumenPorComplejoEntreFechas(Resource):
    @jwt_required
    def get(self, complejo_id):
        usuario_propietario = get_jwt_identity()
        try:
            if not complejo_service.complejo_le_pertenece_a_propietario(usuario_propietario=usuario_propietario,
                                                                        complejo_id=complejo_id):
                return {'message': 'El complejo no le pertenece al propietario'}, 403
        except Exception as exception:
            return {'message': 'Error del servidor al verificar la propiedad del complejo'}, 500

        data = obtener_resumen_complejo_parser.parse_args()

        fecha_inicial = data['fecha_inicial']
        fecha_final = data['fecha_final']

        resumen_complejo = complejo_service.resumen_de_servicios_por_complejo(complejo_id=complejo_id,
                                                                              fecha_inicial=fecha_inicial,
                                                                              fecha_final=fecha_final)

        return resumen_complejo


obtener_resumen_general_parser = reqparse.RequestParser(bundle_errors=True)
obtener_resumen_general_parser.add_argument('fecha_inicial', required=True, location='args')
obtener_resumen_general_parser.add_argument('fecha_final', required=True, location='args')


class ObtenerResumenGeneralEntreFechas(Resource):
    @jwt_required
    def get(self):
        usuario_propietario = get_jwt_identity()

        data = obtener_resumen_general_parser.parse_args()

        fecha_inicial = data['fecha_inicial']
        fecha_final = data['fecha_final']

        resumen_general = complejo_service.resumen_servicios_general(usuario_propietario=usuario_propietario,
                                                                     fecha_inicial=fecha_inicial,
                                                                     fecha_final=fecha_final)

        return resumen_general
