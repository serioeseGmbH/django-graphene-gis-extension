==============================
Django Graphene: GIS Extension
==============================

https://github.com/serioeseGmbH/django-graphene-gis-extension

django-graphene-gis-extension extends ``django-graphene`` with GIS related type definitions
(i.e. scalars, field conversions, ...).

Quick start
-----------

1. Install the package with pip::

    pip install django-graphene-gis-extension

2. Add "serious_django_services" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'graphene_gis_extension',
    ]

3. Use the scalars and input type definitions wherever you need them, for instance in a Query::

     from graphene_gis_extension.scalars import PointScalar
     from graphene_gis_extension.input_types import NearInputType

     class Query(graphene.ObjectType):
         thing_with_location = graphene.Field(
	     ThingWithLocationType,
	     exactly_at=graphene.Argument(PointScalar)
	     near=graphene.Argument(NearInputType)
	 )
