class Entity(object):
    __slots__ = ("_guid", "components", "symbol", "z")
    """Encapsulation of a GUID to use in the entity database."""
    def __init__(self, guid, symbol=' ', z=0):
        """:param guid: globally unique identifier
        :type guid: :class:`int`
        """
        self._guid = guid
        self.components = {}
        self.symbol = symbol
        self.z = z

    def __repr__(self):
        return '{0}({1})'.format(type(self).__name__, self._guid)

    def __hash__(self):
        return self._guid

    def __eq__(self, other):
        return self._guid == hash(other)