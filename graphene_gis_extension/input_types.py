import graphene

from . import scalars


class NearInputType(graphene.InputObjectType):
    """
    Describes a specific Graphene input type to construct a nearness query.

    :param str geom: A GEOSGeometry object to query in prox
    :param float max_distance_km: The maximum distance, in kilometers, to search in around `geom`.
    """
    geom = graphene.NonNull(scalars.GeometryScalar)
    max_distance_km = graphene.NonNull(graphene.Float)
