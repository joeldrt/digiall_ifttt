from data.sensor import Sensor
from datetime import datetime
from services import registro_sensor_service

from mongoengine.queryset.visitor import Q


def agregar(usuario_propietario: str, dispositivo_id: str, nombre: str, tipo_sensor: str) -> Sensor:
    sensor = Sensor()
    sensor.fecha_creacion = datetime.now()
    sensor.usuario_propietario = usuario_propietario
    sensor.dispositivo_id = dispositivo_id
    sensor.nombre = nombre
    sensor.tipo_sensor = tipo_sensor

    sensor.save()

    return sensor


def editar(sensor_id: str, habitacion_id: str, dispositivo_id: str, nombre: str, tipo_sensor: str) -> Sensor:
    sensor = Sensor.objects().get(id=sensor_id)
    sensor.habitacion_id = habitacion_id
    sensor.dispositivo_id = dispositivo_id
    sensor.nombre = nombre
    sensor.tipo_sensor = tipo_sensor

    sensor.save()

    return sensor


def obtener_sensor_por_id(sensor_id: str) -> Sensor:
    sensor = Sensor.objects().get(id=sensor_id)
    return sensor


def dispositivos_id_registrados_por_usuario_propietario(usuario_propietario: str) -> [str]:
    dispositivos_ids = [
        sensor.dispositivo_id for sensor in Sensor.objects(usuario_propietario=usuario_propietario)
    ]
    return dispositivos_ids


def dispositivos_id_sin_registrar_por_usuario_propietario(usuario_propietario: str) -> [str]:
    dispositivos_ids_registrados = [
        sensor.dispositivo_id for sensor in Sensor.objects(usuario_propietario=usuario_propietario)
    ]
    dispositivos_ids_sin_registrar = registro_sensor_service.listar_dispositivos_por_usuario_propietario_no_enlistados(
        usuario_propietario=usuario_propietario,
        dispositivos_ids=dispositivos_ids_registrados
    )
    return dispositivos_ids_sin_registrar


def sensores_sin_vincular(usuario_propietario: str) -> [Sensor]:
    sensores = Sensor.objects(
        Q(usuario_propietario=usuario_propietario) &
        Q(habitacion_id__exists=False)
    )
    return sensores


def obtener_sensores_por_ids(usuario_propietario: str, sensores_ids: [str]) -> [Sensor]:
    sensores = Sensor.objects(
        Q(usuario_propietario=usuario_propietario) &
        Q(id__in=sensores_ids)
    )
    return sensores


def sensores_por_usuario_propietario(usuario_propietario: str) -> [Sensor]:
    sensores = Sensor.objects(usuario_propietario=usuario_propietario)
    return sensores


def sensores_por_habitacion_id(usuario_propietario: str, habitacion_id:str) -> [Sensor]:
    sensores = Sensor.objects(usuario_propietario=usuario_propietario,
                              habitacion_id=habitacion_id)
    return sensores


def sensor_le_pertenece_a_propietario(usuario_propietario: str, sensor_id: str) -> bool:
    sensor = Sensor.objects().get(id=sensor_id)
    return sensor.usuario_propietario == usuario_propietario


def borrar_sensor_por_id(sensor_id: str) -> bool:
    sensor = Sensor.objects().get(id=sensor_id)
    return sensor.delete()


def desvincular_sensores_batch(sensores: [Sensor]) -> bool:
    for sensor in sensores:
        try:
            sensor.habitacion_id = None
            sensor.save()
        except Exception as exception:
            continue

    return True


def borrar_sensores_batch(sensores_ids: [str]) -> bool:
    sensores = Sensor.objects(Q(id__in=sensores_ids))
    for sensor in sensores:
        try:
            sensor.delete()
        except Exception as exception:
            continue

    return True
