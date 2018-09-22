import mongoengine
from datetime import datetime

import data.mongo_digiall_utils as mongo_utils


class Sensor(mongoengine.Document):
    fecha_creacion = mongoengine.DateTimeField(default=datetime.now())

    usuario_propietario = mongoengine.EmailField(required=True)
    habitacion_id = mongoengine.StringField()
    dispositivo_id = mongoengine.StringField(required=True)
    nombre = mongoengine.StringField(required=True)
    tipo_sensor = mongoengine.StringField()

    def to_dict(self):
        return mongo_utils.mongo_to_dict_1(self)

    @mongoengine.queryset_manager
    def objects(doc_cls, queryset):
        # This may actually also be done by defining a default ordering for
        # the document, but this illustrates the use of manager methods
        return queryset.order_by('fecha_creacion')

    meta = {
        'db_alias': 'ifttt',
        'collection': 'sensor',
        'indexes': [
            {'fields': ('usuario_propietario', 'dispositivo_id'), 'unique': True}
        ]
    }
