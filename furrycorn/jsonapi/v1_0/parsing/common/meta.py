from collections import namedtuple


class Meta(namedtuple('Meta', ['dict_attrs'])):
    """
    Representation of freeform metadata anywhere in a response.
    """

    __slots__ = ()

    def __new__(cls, dict_attrs):
        return super(Meta, cls).__new__(cls, dict_attrs)


def mk(obj, config):
    return Meta(obj)

