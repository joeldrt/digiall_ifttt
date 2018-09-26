from data.habitacion import Habitacion
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


def obtener_servicios_por_habitacion(habitacion_id: str, fecha_inicial: str, fecha_final: str) -> dict:
    sensores_de_servicio_objs = sensor_service.obtener_sensores_de_servicio_por_habitacion(habitacion_id=habitacion_id)
    dispositivos_ids = [
        sensor.dispositivo_id for sensor in sensores_de_servicio_objs
    ]
    if len(dispositivos_ids) == 0:
        return {'numero_servicios': 0,
                'ultimo_status': 'Desconocido'}

    registros = registro_sensor_service.obtener_todos_entre_fechas_por_dispositivos_ids(dispositivos_ids=dispositivos_ids,
                                                                                        fecha_inicial=fecha_inicial,
                                                                                        fecha_final=fecha_final)

    if len(registros) == 0:
        return {'numero_servicios': 0,
                'ultimo_status': 'Desconocido'}

    (numero_servicios, ultimo_status) = calculadora_servicios.calcular(
        registros=registros, dispositivos_ids=dispositivos_ids)

    objeto = {'numero_servicios': numero_servicios,
              'ultimo_status':
                  ('Disponible' if calculadora_servicios.EstadoHabitacion.DISPONIBLE == ultimo_status else 'Servicio')}

    return objeto
