import mongoengine
from datetime import datetime

import data.mongo_digiall_utils as mongo_utils


class Habitacion(mongoengine.Document):
    fecha_creacion = mongoengine.DateTimeField(default=datetime.now())

    usuario_propietario = mongoengine.EmailField()

    complejo_id = mongoengine.StringField()
    nombre = mongoengine.StringField()
    tipo = mongoengine.StringField()
    precio_base = mongoengine.DecimalField()
    usa_servicio_doble_sensor = mongoengine.BooleanField(default=False)
    dispositivos_ids_servicio_doble = mongoengine.ListField(mongoengine.StringField())
    hora_extra = mongoengine.DecimalField()
    persona_extra = mongoengine.DecimalField()

    def to_dict(self):
        return mongo_utils.mongo_to_dict_1(self)

    @mongoengine.queryset_manager
    def objects(doc_cls, queryset):
        # This may actually also be done by defining a default ordering for
        # the document, but this illustrates the use of manager methods
        return queryset.order_by('fecha_creacion')

    meta = {
        'db_alias': 'ifttt',
        'collection': 'habitacion',
        'indexes': [
            {'fields': ('complejo_id', 'nombre'), 'unique': True}
        ]
    }
