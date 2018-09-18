from data.habitacion import Habitacion, ExtrasHabitacion
from datetime import datetime


def agregar(complejo_id: str, nombre: str, tipo: str, precio_base: float) -> Habitacion:
    habitacion = Habitacion()
    habitacion.complejo_id = complejo_id
    habitacion.nombre = nombre
    habitacion.tipo = tipo
    habitacion.precio_base = precio_base

    habitacion = habitacion.save()

    return habitacion


def obtener_habitaciones_por_complejo(complejo_id: str) -> [Habitacion]:
    return Habitacion.objects(complejo_id=complejo_id)


def obtener_habitacion_por_id(habitacion_id: str) -> Habitacion:
    habitacion = Habitacion.objects().get(id=habitacion_id)
    return habitacion


def agregar_extras_habitacion(habitacion_id: str, extras_habitacion: ExtrasHabitacion) -> Habitacion:
    habitacion = Habitacion.objects().get(id=habitacion_id)

    habitacion.extras = extras_habitacion
    habitacion.save()

    habitacion = Habitacion.objects().get(id=habitacion_id)

    return habitacion


def generar_extras_habitacion(hora_extra: float, persona_extra: float) -> ExtrasHabitacion:
    return ExtrasHabitacion(hora_extra=hora_extra, persona_extra=persona_extra)

