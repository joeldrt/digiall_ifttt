from data.habitacion import Habitacion
from data.registro_sensor import RegistroSensor
from datetime import datetime

from services import sensor_service, registro_sensor_service
from brain import calculadora_servicios


def agregar(usuario_propietario: str, complejo_id: str, nombre: str, tipo: str, precio_base: str,
            hora_extra: str, persona_extra: str) -> Habitacion:
    habitacion = Habitacion()
    habitacion.usuario_propietario = usuario_propietario
    habitacion.complejo_id = complejo_id
    habitacion.nombre = nombre
    habitacion.tipo = tipo
    habitacion.precio_base = float(precio_base) if precio_base else None
    habitacion.hora_extra = float(hora_extra) if hora_extra else None
    habitacion.persona_extra = float(persona_extra) if persona_extra else None

    habitacion = habitacion.save()

    return habitacion


def editar(habitacion_id: str, nombre: str, tipo: str, precio_base: str, hora_extra: str,
           persona_extra: str) -> Habitacion:
    habitacion = Habitacion.objects().get(id=habitacion_id)
    habitacion.nombre = nombre
    habitacion.tipo = tipo
    habitacion.precio_base = float(precio_base) if precio_base else None
    habitacion.hora_extra = float(hora_extra) if hora_extra else None
    habitacion.persona_extra = float(persona_extra) if persona_extra else None

    habitacion.save()

    return habitacion


def habitacion_le_pertenece_a_propietario(usuario_propietario: str, habitacion_id: str) -> bool:
    habitacion = Habitacion.objects().get(id=habitacion_id)
    return habitacion.usuario_propietario == usuario_propietario


def obtener_habitaciones_por_usuario_propietario(usuario_propietario: str) -> [Habitacion]:
    return Habitacion.objects(usuario_propietario=usuario_propietario)


def obtener_habitacion_por_id(habitacion_id: str) -> Habitacion:
    habitacion = Habitacion.objects().get(id=habitacion_id)
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


def obtener_servicios_por_habitacion(habitacion_id: str, fecha_inicial: str, fecha_final: str) -> dict:
    habitacion = obtener_habitacion_por_id(habitacion_id=habitacion_id)

    sensores_de_servicio_objs = sensor_service.obtener_sensores_de_servicio_por_habitacion(habitacion_id=habitacion_id)
    dispositivos_ids = [
        sensor.dispositivo_id for sensor in sensores_de_servicio_objs
    ]

    resultado_dict = {}
    resultado_dict['habitacion'] = habitacion.to_dict()
    resultado_dict['fecha_inicial'] = fecha_inicial
    resultado_dict['fecha_final'] = fecha_final
    resultado_dict['numero_servicios'] = 0
    resultado_dict['ultimo_status'] = 'Desconocido'
    resultado_dict['ganancia'] = 0.0
    resultado_dict['registros'] = []

    if len(dispositivos_ids) == 0:
        return resultado_dict

    registros_obj = registro_sensor_service.obtener_todos_entre_fechas_por_dispositivos_ids(
        dispositivos_ids=dispositivos_ids,
        fecha_inicial=fecha_inicial,
        fecha_final=fecha_final)

    if len(registros_obj) == 0:
        return resultado_dict

    registros = [
        registro.to_dict() for registro in registros_obj
    ]

    (numero_servicios, ultimo_status) = calculadora_servicios.calcular2(
        registros=registros_obj, dispositivos_ids=dispositivos_ids)


    resultado_dict['ultimo_status'] = 'Disponible' if calculadora_servicios.EstadoHabitacion.DISPONIBLE == ultimo_status else 'Servicio',
    resultado_dict['numero_servicios'] = numero_servicios
    resultado_dict['ganancia'] = numero_servicios * float(habitacion.precio_base if habitacion.precio_base else 0.0)
    resultado_dict['registros'] = registros

    return resultado_dict


def obtener_registros_por_habitacion(habitacion_id: str,fecha_inicial: str, fecha_final: str) -> [RegistroSensor]:
    sensores_de_servicio_objs = sensor_service.obtener_sensores_de_servicio_por_habitacion(habitacion_id=habitacion_id)
    dispositivos_ids = [
        sensor.dispositivo_id for sensor in sensores_de_servicio_objs
    ]
    if len(dispositivos_ids) == 0:
        return []

    registros = registro_sensor_service.obtener_todos_entre_fechas_por_dispositivos_ids(
        dispositivos_ids=dispositivos_ids,
        fecha_inicial=fecha_inicial,
        fecha_final=fecha_final)

    return registros
