import mongoengine
from datetime import datetime

import data.mongo_digiall_utils as mongo_utils


class Complejo(mongoengine.Document):
    fecha_creacion = mongoengine.DateTimeField(default=datetime.now())

    usuario_propietario = mongoengine.EmailField()

    nombre = mongoengine.StringField()
    direccion = mongoengine.StringField()
    telefonos = mongoengine.ListField(mongoengine.StringField())

    latitud = mongoengine.FloatField()
    longitud = mongoengine.FloatField()
    posicion_geografica = mongoengine.PointField()

    def to_dict(self):
        return mongo_utils.mongo_to_dict_1(self)

    @mongoengine.queryset_manager
    def objects(doc_cls, queryset):
        # This may actually also be done by defining a default ordering for
        # the document, but this illustrates the use of manager methods
        return queryset.order_by('fecha_creacion')

    meta = {
        'db_alias': 'ifttt',
        'collection': 'complejo',
        'indexes': [
            {'fields': ('usuario_propietario', 'nombre'), 'unique': True}
        ]
    }
