import mongoengine
from datetime import datetime

import data.mongo_digiall_utils as mongo_utils


class Sensor(mongoengine.Document):
    fecha_creacion = mongoengine.DateTimeField(default=datetime.now())

    dispositivo_id = mongoengine.StringField(unique=True)
    nombre = mongoengine.StringField()
    tipo_sensor = mongoengine.StringField()

    def to_dict(self):
        return mongo_utils.mongo_to_dict(self)

    meta = {
        'db_alias': 'ifttt',
        'collection': 'sensor'
    }
