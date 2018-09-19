from data.complejo import Complejo
from datetime import datetime


def agregar(usuario_propietario: str, nombre: str, direccion: str, telefonos: [str], latitud: str, longitud: str) \
        -> Complejo:
    complejo = Complejo()
    complejo.fecha_creacion = datetime.now()
    complejo.usuario_propietario = usuario_propietario
    complejo.nombre = nombre
    complejo.direccion = direccion
    complejo.telefonos = telefonos
    if latitud:
        complejo.latitud = float(latitud)
    if longitud:
        complejo.longitud = float(longitud)
    if longitud and latitud:
        complejo.posicion_geografica = [longitud, latitud]

    complejo = complejo.save()

    return complejo


def obtener_complejos_por_propietario(usuario_propietario: str) -> [Complejo]:
    return Complejo.objects(usuario_propietario=usuario_propietario)


def obtener_complejo_por_id(usuario_propietario: str, complejo_id: str) -> Complejo:
    complejo = Complejo.objects(usuario_propietario=usuario_propietario).get(id=complejo_id)
    return complejo


def borrar_complejo_por_id(usuario_propietario: str, complejo_id: str) -> bool:
    complejo = Complejo.objects(usuario_propietario=usuario_propietario).get(id=complejo_id)
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
    if latitud:
        complejo.latitud = float(latitud)
    if longitud:
        complejo.longitud = float(longitud)
    if longitud and latitud:
        complejo.posicion_geografica = [longitud, latitud]
    complejo = complejo.save()
    return complejo
