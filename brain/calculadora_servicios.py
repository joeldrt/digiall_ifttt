from enum import Enum
from data.registro_sensor import RegistroSensor

from datetime import datetime, timedelta
from services import registro_sensor_service

SEGUNDOS_PARA_CONTABILIZAR_REGISTRO = 60
SEGUNDOS_PARA_ASEGURAR_ESTATUS = 180


class EstadoHabitacion(Enum):
    DISPONIBLE = 1
    EN_SERVICIO = 0
    INCIERTO = 2


class EstadoSensor(Enum):
    ABIERTO = 1
    CERRADO = 0
    INCIERTO = 2


TIPOS_EVENTOS_SENSOR = {
    "ABIERTO": 1,
    "CERRADO": 0
}


def calcular(registros: [RegistroSensor], dispositivos_ids: [str]) -> (int, EstadoHabitacion):
    contador = 0
    (estado_inicial, fecha_inicial) = obtener_primer_estado_en_registros(registros=registros, dispositivos_ids=dispositivos_ids)
    if not estado_inicial or not fecha_inicial:
        return contador, None

    registros = limpiar_registros(registros=registros, fecha=fecha_inicial)

    estado_nuevo = None
    while len(registros) > 0:
        (estado_nuevo, fecha_nueva) = obtener_primer_estado_en_registros(registros=registros,
                                                                         dispositivos_ids=dispositivos_ids)

        if not estado_nuevo or not fecha_nueva:
            return contador, estado_inicial

        if estado_nuevo == EstadoHabitacion.DISPONIBLE and estado_nuevo != estado_inicial:
            contador += 1

        estado_inicial = estado_nuevo

        registros = limpiar_registros(registros=registros, fecha=fecha_nueva)

    return contador, estado_nuevo


def limpiar_registros(registros: [RegistroSensor], fecha: datetime) -> [RegistroSensor]:
    registros_nuevos = [
        registro for registro in registros if registro.fecha_creacion > fecha
    ]
    return registros_nuevos


def obtener_primer_estado_en_registros(registros: [RegistroSensor], dispositivos_ids: [str]) -> (EstadoHabitacion, datetime):
    if len(registros) == 0:
        return None, None

    estados_iniciales_dispositivos = []

    for dispositivo_id in dispositivos_ids:
        estado, fecha = obtener_estado_inicial_de_dispositivo(dispositivo_id=dispositivo_id, registros=registros)
        if estado and fecha:
            estados_iniciales_dispositivos.append((dispositivo_id, estado, fecha))

    if len(estados_iniciales_dispositivos) != len(dispositivos_ids):
        return None, None

    # parte en donde se meten los registros a la tabla de verdad para ver el estado de la habitacion
    # solución para sólo 2 sensores TODO limitar el maximo de sensores por habitación a 2
    suma = 0
    fecha_pivote = None
    for estado_inicial in estados_iniciales_dispositivos:
        suma += estado_inicial[1].value
        if not fecha_pivote:
            fecha_pivote = estado_inicial[2]
        else:
            fecha_pivote = estado_inicial[2] if estado_inicial[2] > fecha_pivote else fecha_pivote

    if suma == 0 or suma == len(estados_iniciales_dispositivos):
        return (EstadoHabitacion.EN_SERVICIO, fecha_pivote) if suma == 0 else (EstadoHabitacion.DISPONIBLE, fecha_pivote)

    # se borran los registros hasta la fecha_pivote para encontrar el estado inicial
    registros_nuevos = limpiar_registros(registros=registros, fecha=fecha_pivote)

    return obtener_primer_estado_en_registros(registros=registros_nuevos, dispositivos_ids=dispositivos_ids)


def obtener_estado_inicial_de_dispositivo(dispositivo_id: str, registros: [RegistroSensor]) -> (EstadoSensor, datetime):
    for registro in registros:
        if registro.dispositivo_id == dispositivo_id:
            fecha = registro.fecha_creacion
            estado = EstadoSensor.ABIERTO if registro.tipo_evento == RegistroSensor.ABIERTO else EstadoSensor.CERRADO
            return estado, fecha

    registro_buscado = registro_sensor_service.obtener_registro_inmediato_anterior_fecha_por_dispositivo_id(
        dispositivo_id=dispositivo_id, fecha=registros[0].fecha_creacion)

    if registro_buscado:
        fecha = registro_buscado.fecha_creacion
        estado = EstadoSensor.ABIERTO if registro_buscado == RegistroSensor.ABIERTO else EstadoSensor.CERRADO
        return estado, fecha

    return None, None


def calcular2(registros: [RegistroSensor], dispositivos_ids: [str]) -> (int, EstadoHabitacion):
    # generar matrix de 1 y 0 dependiendo del estatus por tiempo en base a los registros
    # en cada nuevo ingreso solo se modifica el
    estado_anterior_dispositivos = {}
    tabla = []
    for registro in registros:
        fecha = registro.fecha_creacion
        valores = []
        for dispositivo_id in dispositivos_ids:
            if registro.dispositivo_id == dispositivo_id:
                valores.append(TIPOS_EVENTOS_SENSOR.get(registro.tipo_evento))
                estado_anterior_dispositivos[dispositivo_id] = TIPOS_EVENTOS_SENSOR.get(registro.tipo_evento)
                continue

            if dispositivo_id not in estado_anterior_dispositivos.keys():
                valores.append(None)
                continue
            valores.append(estado_anterior_dispositivos[dispositivo_id])

        tabla.append((fecha, valores))

    estado = EstadoHabitacion.INCIERTO
    servicios = 0
    for fecha, estadosbinarios in tabla:
        if None in estadosbinarios:
            continue

        if sum(estadosbinarios) == 0:
            nuevo_estado = EstadoHabitacion.EN_SERVICIO
        if sum(estadosbinarios) == len(dispositivos_ids):
            nuevo_estado = EstadoHabitacion.DISPONIBLE

        if nuevo_estado == EstadoHabitacion.DISPONIBLE and estado != nuevo_estado:
            servicios += 1

        estado = nuevo_estado

    return servicios, estado
