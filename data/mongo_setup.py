import mongoengine


def global_init():
    mongoengine.register_connection(alias='ifttt', name='da_ifttt')