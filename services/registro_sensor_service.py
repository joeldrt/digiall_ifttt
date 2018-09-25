from data.registro_sensor import RegistroSensor
from datetime import datetime, timedelta

from mongoengine.queryset.visitor import Q


def registrar(usuario_propietario: str, tipo_evento: str, dispositivo_id: str, reported_at: str) -> RegistroSensor:
    registro_sensor = RegistroSensor()
    registro_sensor.fecha_creacion = datetime.now()
    registro_sensor.tipo_evento = tipo_evento
    registro_sensor.dispositivo_id = dispositivo_id
    registro_sensor.reported_at = reported_at
    registro_sensor.usuario_propietario = usuario_propietario

    registro_sensor.save()
    return registro_sensor


def registrar_apertura(usuario_propietario: str, dispositivo_id: str, reported_at: str) -> RegistroSensor:
    return registrar(usuario_propietario=usuario_propietario,
                     tipo_evento=RegistroSensor.ABIERTO,
                     dispositivo_id=dispositivo_id,
                     reported_at=reported_at)


def registrar_cerrado(usuario_propietario: str, dispositivo_id: str, reported_at: str) -> RegistroSensor:
    return registrar(usuario_propietario=usuario_propietario,
                     tipo_evento=RegistroSensor.CERRADO,
                     dispositivo_id=dispositivo_id,
                     reported_at=reported_at)


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


def listar_dispositivos_id_por_usuario_propietario(usuario_propietario: str) -> [str]:
    sensores_ids = [
        registro.dispositivo_id for registro in RegistroSensor.objects(
            usuario_propietario=usuario_propietario).distinct(field="dispositivo_id")
    ]
    return sensores_ids


def listar_dispositivos_por_usuario_propietario_no_enlistados(usuario_propietario: str, dispositivos_ids: [str]) -> [str]:
    sensores_ids = [
        registro for registro in RegistroSensor.objects(
            Q(usuario_propietario=usuario_propietario) &
            Q(dispositivo_id__not__in=dispositivos_ids)
        ).distinct(field="dispositivo_id")
    ]
    return sensores_ids


def obtener_todos_entre_fechas(fecha_inicial: str, fecha_final: str) -> [RegistroSensor]:
    fecha_inicial_date = datetime.strptime(fecha_inicial, '%Y-%m-%d')
    fecha_final_date = datetime.strptime(fecha_final, '%Y-%m-%d') + timedelta(days=1)

    registros = RegistroSensor.objects(
        Q(fecha_creacion__gte=fecha_inicial_date) &
        Q(fecha_creacion__lte=fecha_final_date)
    )

    return registros


def obtener_todos_entre_fechas_por_habitacion(habitacion_id: str, fecha_inicial: str, fecha_final: str) -> [RegistroSensor]:
    fecha_inicial_date = datetime.strptime(fecha_inicial, '%Y-%m-%d')
    fecha_final_date = datetime.strptime(fecha_final, '%Y-%m-%d') + timedelta(days=1)

    registros = RegistroSensor.objects(
        Q(fecha_creacion__gte=fecha_inicial_date) &
        Q(fecha_creacion__lte=fecha_final_date) &
        Q(habitacion_id__exact=habitacion_id)
    )

    return registros
