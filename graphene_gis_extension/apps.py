from django.apps import AppConfig

from .fields import register_field_conversions

class GrapheneGisExtensionConfig(AppConfig):
    name = 'graphene_gis_extension'

    def ready(self):
        register_field_conversions()
