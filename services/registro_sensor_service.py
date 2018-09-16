from data.registro_sensor import RegistroSensor
from datetime import datetime, timedelta

from mongoengine.queryset.visitor import Q


def registrar(tipo_evento: str, dispositivo_id: str, reported_at: str) -> RegistroSensor:
    registro_sensor = RegistroSensor()
    registro_sensor.fecha_creacion = datetime.now()
    registro_sensor.tipo_evento = tipo_evento
    registro_sensor.dispositivo_id = dispositivo_id
    registro_sensor.reported_at = reported_at

    registro_sensor.save()
    return registro_sensor


def registrar_apertura(dispositivo_id: str, reported_at: str) -> RegistroSensor:
    return registrar(RegistroSensor.ABIERTO, dispositivo_id, reported_at)


def registrar_cerrado(dispositivo_id: str, reported_at: str) -> RegistroSensor:
    return registrar(RegistroSensor.CERRADO, dispositivo_id, reported_at)


def obtener_todos_entre_fechas_por_dispositivos_id(fecha_inicial: str, fecha_final: str, dispositivos_ids: [str]) -> [dict]:
    fecha_inicial_date = datetime.strptime(fecha_inicial, '%Y-%m-%d')
    fecha_final_date = datetime.strptime(fecha_final, '%Y-%m-%d') + timedelta(days=1)

    objetos = RegistroSensor.objects(
        Q(dispositivo_id__in=dispositivos_ids) &
        Q(fecha_creacion__gte=fecha_inicial_date) &
        Q(fecha_creacion__lte=fecha_final_date)
    )

    registros = [
        registro.to_dict for registro in objetos
    ]
    return registros


def obtener_todos_entre_fechas(fecha_inicial: str, fecha_final: str) -> [dict]:
    fecha_inicial_date = datetime.strptime(fecha_inicial, '%Y-%m-%d')
    fecha_final_date = datetime.strptime(fecha_final, '%Y-%m-%d') + timedelta(days=1)

    objetos = RegistroSensor.objects(
        Q(fecha_creacion__gte=fecha_inicial_date) &
        Q(fecha_creacion__lte=fecha_final_date)
    )

    registros = [
        registro.to_dict for registro in objetos
    ]
    return registros
