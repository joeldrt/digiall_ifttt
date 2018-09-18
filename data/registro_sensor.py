import mongoengine
from datetime import datetime

import data.mongo_digiall_utils as mongo_utils


class RegistroSensor(mongoengine.Document):
    ABIERTO = 'ABIERTO'
    CERRADO = 'CERRADO'

    fecha_creacion = mongoengine.DateTimeField(default=datetime.now())

    tipo_evento = mongoengine.StringField()
    dispositivo_id = mongoengine.StringField()
    reported_at = mongoengine.StringField()
    usuario_propietario = mongoengine.EmailField()

    def to_dict(self):
        return mongo_utils.mongo_to_dict(self)

    meta = {
        'db_alias': 'ifttt',
        'collection': 'registro_sensor'
    }
