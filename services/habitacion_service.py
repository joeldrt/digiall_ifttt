from data.habitacion import Habitacion
from datetime import datetime

from services import sensor_service


def agregar(usuario_propietario: str, complejo_id: str, nombre: str, tipo: str, precio_base: str,
            usa_servicio_doble_sensor: bool, dispositivos_ids_servicio_doble: [str],
            hora_extra: str, persona_extra: str) -> Habitacion:
    habitacion = Habitacion()
    habitacion.fecha_creacion = datetime.now()
    habitacion.usuario_propietario = usuario_propietario
    habitacion.complejo_id = complejo_id
    habitacion.nombre = nombre
    habitacion.tipo = tipo
    habitacion.precio_base = float(precio_base) if precio_base else None
    habitacion.usa_servicio_doble_sensor = usa_servicio_doble_sensor
    habitacion.dispositivos_ids_servicio_doble = dispositivos_ids_servicio_doble
    habitacion.hora_extra = float(hora_extra) if hora_extra else None
    habitacion.persona_extra = float(persona_extra) if persona_extra else None

    habitacion = habitacion.save()

    return habitacion


def editar(habitacion_id: str, nombre: str, tipo: str, precio_base: str, usa_servicio_doble_sensor: bool,
           dispositivos_ids_servicio_doble: [str], hora_extra: str, persona_extra: str) -> Habitacion:
    habitacion = Habitacion.objects().get(id=habitacion_id)
    habitacion.nombre = nombre
    habitacion.tipo = tipo
    habitacion.precio_base = float(precio_base) if precio_base else None
    habitacion.usa_servicio_doble_sensor = usa_servicio_doble_sensor
    habitacion.dispositivos_ids_servicio_doble = dispositivos_ids_servicio_doble
    habitacion.hora_extra = float(hora_extra) if hora_extra else None
    habitacion.persona_extra = float(persona_extra) if persona_extra else None

    habitacion.save()

    return habitacion


def habitacion_le_pertenece_a_propietario(usuario_propietario: str, habitacion_id: str) -> bool:
    habitacion = Habitacion.objects().get(id=habitacion_id)
    return habitacion.usuario_propietario == usuario_propietario


def obtener_habitaciones_por_usuario_propietario(usuario_propietario: str) -> [Habitacion]:
    return Habitacion.objects(usuario_propietario=usuario_propietario)


def obtener_habitacion_por_id(usuario_propietario: str, habitacion_id: str) -> Habitacion:
    habitacion = Habitacion.objects(usuario_propietario=usuario_propietario).get(id=habitacion_id)
    return habitacion


def borrar_habitacion_por_id(usuario_propietario: str, habitacion_id: str) -> bool:
    habitacion = Habitacion.objects(usuario_propietario=usuario_propietario).get(id=habitacion_id)
    limpiar_habitacion_de_sensores(habitacion)
    habitacion.delete()
    return True


def obtener_habitaciones_por_complejo(complejo_id: str) -> [Habitacion]:
    return Habitacion.objects(complejo_id=complejo_id)


def limpiar_habitacion_de_sensores(habitacion: Habitacion) -> bool:
    sensores = sensor_service.sensores_por_habitacion_id(usuario_propietario=habitacion.usuario_propietario,
                                                         habitacion_id=str(habitacion.id))
    return sensor_service.desvincular_sensores_batch(sensores)


def borrar_habitaciones_por_complejo(complejo_id: str) -> bool:
    habitaciones = obtener_habitaciones_por_complejo(complejo_id=complejo_id)
    for habitacion in habitaciones:
        try:
            limpiar_habitacion_de_sensores(habitacion)
            habitacion.delete()
        except Exception as ex:
            continue
    return True
