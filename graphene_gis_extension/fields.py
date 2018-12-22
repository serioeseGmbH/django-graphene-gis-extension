from django import forms
from django.db import models

from django.contrib.gis import forms as gis_forms
from django.contrib.gis.db import models as gis_models

import graphene

from graphene_django.converter import convert_django_field
from graphene_django.forms.converter import convert_form_field

from . import scalars


def make_field_converter(scalar, description):
    def convert_field(field, registry=None):
        if isinstance(field, models.fields.Field):
            required = not field.null
            return graphene.Field(
                scalar,
                description=description,
                required=required
            )
        if isinstance(field, forms.fields.Field):
            required = field.required
            return graphene.Argument(
                scalar,
                description=description,
                required=required
            )
        raise NotImplementedError(
            "Can't convert field if it's neither a model field nor a form field"
        )
    return convert_field


def register_model_and_form_fields(model_field, form_field, scalar, description):
    # The odd call syntax is because `register` is usually used as a decorator.
    # We want to avoid this, because if you use decorators at the top-level,
    # they might run multiple times, or not at the right time.
    # We want the registration process to happen once during the loading of
    # this app, so we do it in this function like this instead.
    convert_django_field.register(gis_models.PointField)(
        make_field_converter(scalar, description)
    )
    convert_form_field.register(gis_forms.PointField)(
        make_field_converter(scalar, description)
    )


def register_field_conversions():
    """
    Registers all field conversion functions. Should be called once during
    `ready` of the AppConfig.
    """

    # TODO add more than PointField here
    register_model_and_form_fields(
        gis_models.PointField,
        gis_forms.PointField,
        scalar=scalars.PointScalar,
        description="A GEOS Point object with x/y/srid, sent/received as WKT"
    )
