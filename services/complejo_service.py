from data.complejo import Complejo
from datetime import datetime

from services import habitacion_service


def agregar(usuario_propietario: str, nombre: str, direccion: str, telefonos: [str], latitud: str, longitud: str) \
        -> Complejo:
    complejo = Complejo()
    complejo.usuario_propietario = usuario_propietario
    complejo.nombre = nombre
    complejo.direccion = direccion
    complejo.telefonos = telefonos
    complejo.latitud = float(latitud) if latitud else None
    complejo.longitud = float(longitud) if longitud else None
    if longitud and latitud:
        complejo.posicion_geografica = [longitud, latitud]

    complejo = complejo.save()

    return complejo


def obtener_complejos_por_propietario(usuario_propietario: str) -> [Complejo]:
    return Complejo.objects(usuario_propietario=usuario_propietario)


def obtener_complejo_por_id(complejo_id: str) -> Complejo:
    complejo = Complejo.objects().get(id=complejo_id)
    return complejo


def borrar_complejo_por_id(usuario_propietario: str, complejo_id: str) -> bool:
    complejo = Complejo.objects(usuario_propietario=usuario_propietario).get(id=complejo_id)
    habitacion_service.borrar_habitaciones_por_complejo(complejo_id=str(complejo.id))
    complejo.delete()
    return True


def complejo_le_pertenece_a_propietario(usuario_propietario: str,complejo_id: str) -> bool:
    complejo = Complejo.objects().get(id=complejo_id)
    return complejo.usuario_propietario == usuario_propietario


def editar_complejo(complejo_id: str, nombre: str, direccion: str, telefonos: [str],
                    latitud: str, longitud: str) -> Complejo:
    complejo = Complejo.objects().get(id=complejo_id)
    complejo.nombre = nombre
    complejo.direccion = direccion
    complejo.telefonos = telefonos
    complejo.latitud = float(latitud) if latitud else None
    complejo.longitud = float(longitud) if longitud else None
    if longitud and latitud:
        complejo.posicion_geografica = [longitud, latitud]
    complejo = complejo.save()
    return complejo


def resumen_de_servicios_por_complejo(complejo_id: str, fecha_inicial: str, fecha_final: str) -> dict:

    complejo = obtener_complejo_por_id(complejo_id=complejo_id)

    habitaciones_complejo = habitacion_service.obtener_habitaciones_por_complejo(complejo_id=complejo_id)

    resultado_dict = {}

    resumenes_habitaciones = []

    total_servicios = 0

    ganancia_total = 0.0

    for habitacion in habitaciones_complejo:
        resumen_habitacion = habitacion_service.obtener_servicios_por_habitacion(habitacion_id=str(habitacion.id),
                                                                                 fecha_inicial=fecha_inicial,
                                                                                 fecha_final=fecha_final)

        total_servicios += resumen_habitacion['numero_servicios'] if resumen_habitacion['numero_servicios'] else 0
        ganancia_total += resumen_habitacion['ganancia'] if resumen_habitacion['ganancia'] else 0.0
        resumenes_habitaciones.append(resumen_habitacion)

    resultado_dict['complejo'] = complejo.to_dict()
    resultado_dict['fecha_inicial'] = fecha_inicial
    resultado_dict['fecha_final'] = fecha_final
    resultado_dict['resumen_habitaciones'] = resumenes_habitaciones
    resultado_dict['total_servicios'] = total_servicios
    resultado_dict['ganancia_total'] = ganancia_total

    return resultado_dict


def resumen_servicios_general(usuario_propietario: str, fecha_inicial: str, fecha_final: str) -> dict:

    complejos = obtener_complejos_por_propietario(usuario_propietario=usuario_propietario)

    resumen_dict = {}

    resumen_complejos = []

    total_servicios = 0

    ganancia_total = 0.0

    for complejo in complejos:
        resumen = resumen_de_servicios_por_complejo(complejo_id=str(complejo.id),
                                                    fecha_inicial=fecha_inicial,
                                                    fecha_final=fecha_final)

        total_servicios += resumen['total_servicios'] if resumen['total_servicios'] else 0
        ganancia_total += resumen['ganancia_total'] if resumen['ganancia_total'] else 0.0

        resumen_complejos.append(resumen)

    resumen_dict['fecha_inicial'] = fecha_inicial
    resumen_dict['fecha_final'] = fecha_final
    resumen_dict['total_servicios'] = total_servicios
    resumen_dict['ganancia_total'] = ganancia_total
    resumen_dict['resumen_complejos'] = resumen_complejos

    return resumen_dict

