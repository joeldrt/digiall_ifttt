import mongoengine
from datetime import datetime

import data.mongo_digiall_utils as mongo_utils


class Sensor(mongoengine.Document):
    fecha_creacion = mongoengine.DateTimeField(default=datetime.now())

    usuario_propietario = mongoengine.EmailField()
    dispositivo_id = mongoengine.StringField()
    nombre = mongoengine.StringField()
    tipo_sensor = mongoengine.StringField()

    def to_dict(self):
        return mongo_utils.mongo_to_dict_1(self)

    meta = {
        'db_alias': 'ifttt',
        'collection': 'sensor',
        'indexes': [
            {'fields': ('usuario_propietario', 'dispositivo_id'), 'unique': True}
        ]
    }
