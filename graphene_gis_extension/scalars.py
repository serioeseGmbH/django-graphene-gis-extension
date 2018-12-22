from graphql.language import ast

from graphene.types import Scalar

from django.contrib.gis.geos import GEOSGeometry


class GeometryScalar(Scalar):
    """
    A Graphene Scalar type for the GEOSGeometry type.
    See https://docs.djangoproject.com/en/2.1/ref/contrib/gis/geos/ for reference.

    This scalar type can contain any kind of GEOSGeometry,
    and doesn't enforce a specific geom_typeid.

    This scalar is deserialized and serialized from/as WKT strings
    (e.g. "POINT(0 0)", for a Point).
    """

    @staticmethod
    def serialize(d):
        return str(d)

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, ast.StringValue):
            geom = GEOSGeometry(node.value)
            return geom

    @classmethod
    def parse_value(cls, value): # Expects that isinstance(value, str) is True
        geom = GEOSGeometry(value)
        return geom


class SpecificGeometryBaseScalar(Scalar):
    """
    [!] This class is conceptually abstract and should not be instantiated; only its subtypes should be.

    A Graphene Scalar base type for concrete GEOSGeometry subtypes with a fixed geom_typeid.
    See https://docs.djangoproject.com/en/2.1/ref/contrib/gis/geos/ for reference.

    These scalars are  is deserialized and serialized from/as WKT strings
    (e.g. "POINT(0 0)", for a Point).
    """

    @property
    def geom_typeid(self):
        raise NotImplementedError(
            "SpecificGEOSGeometryBaseScalar is abstract and doesn't have a geom_typeid!\
            Instantiate a concrete subtype instead."
        )

    @staticmethod
    def serialize(d):
        return str(d)

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, ast.StringValue):
            geom = GEOSGeometry(node.value)
            # Only return if the correct geom_typeid (and not another Geometry type) was parsed. See:
            # https://docs.djangoproject.com/en/2.1/ref/contrib/gis/geos/#django.contrib.gis.geos.GEOSGeometry.geom_typeid
            if geom.geom_typeid == cls.geom_typeid:
                return geom

    @classmethod
    def parse_value(cls, value): # Expects that isinstance(value, str) is True
        geom = GEOSGeometry(value)
        if geom.geom_typeid == cls.geom_typeid:
            return geom

class PointScalar(SpecificGeometryBaseScalar):
    geom_typeid = 0
    class Meta:
        description = "A GIS Point serialized/parsed as WKT."

class LineStringScalar(SpecificGeometryBaseScalar):
    geom_typeid = 1
    class Meta:
        description = "A GIS LineString serialized/parsed as WKT."

class LinearRingScalar(SpecificGeometryBaseScalar):
    geom_typeid = 2
    class Meta:
        description = "A GIS LinearRing serialized/parsed as WKT."

class PolygonScalar(SpecificGeometryBaseScalar):
    geom_typeid = 3
    class Meta:
        description = "A GIS Polygon serialized/parsed as WKT."

class MultiPointScalar(SpecificGeometryBaseScalar):
    geom_typeid = 4
    class Meta:
        description = "A GIS MultiPoint serialized/parsed as WKT."

class MultiLineStringScalar(SpecificGeometryBaseScalar):
    geom_typeid = 5
    class Meta:
        description = "A GIS MultiLineString serialized/parsed as WKT."

class MultiPolygonScalar(SpecificGeometryBaseScalar):
    geom_typeid = 6
    class Meta:
        description = "A GIS MultiPolygon serialized/parsed as WKT."

class GeometryCollectionScalar(SpecificGeometryBaseScalar):
    geom_typeid = 7
    class Meta:
        description = "A GIS GeometryCollection serialized/parsed as WKT."
