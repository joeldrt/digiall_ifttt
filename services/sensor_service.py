from data.sensor import Sensor
from datetime import datetime
from services import registro_sensor_service


def agregar(usuario_propietario: str, dispositivo_id: str, nombre: str, tipo_sensor: str) -> Sensor:
    sensor = Sensor()
    sensor.fecha_creacion = datetime.now()
    sensor.usuario_propietario = usuario_propietario
    sensor.dispositivo_id = dispositivo_id
    sensor.nombre = nombre
    sensor.tipo_sensor = tipo_sensor

    sensor.save()

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


def sensores_por_usuario_propietario(usuario_propietario: str) -> [Sensor]:
    sensores = [
        sensor for sensor in Sensor.objects(usuario_propietario=usuario_propietario)
    ]
    return sensores


def borrar_sensor_por_id(sensor_id: str) -> bool:
    sensor = Sensor.objects().get(sensor_id=sensor_id)
    return sensor.delete()
