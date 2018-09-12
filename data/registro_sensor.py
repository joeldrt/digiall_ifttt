import mongoengine
import datetime

import data.mongo_digiall_utils as mongo_utils


class RegistroSensor(mongoengine.Document):
    fecha_creacion = mongoengine.DateTimeField(default=datetime.datetime.now())

    tipo_evento = mongoengine.StringField()

    sensor_id = mongoengine.StringField()
    reported_at = mongoengine.StringField()

    def to_dict(self):
        return mongo_utils.mongo_to_dict(self)

    meta = {
        'db_alias': 'ifttt',
        'collection': 'registro_sensor'
    }