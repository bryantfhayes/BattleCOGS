class Entity(object):
    __slots__ = ("_guid", "components", "symbol", "z", "removable")
    """Encapsulation of a GUID to use in the entity database."""
    def __init__(self, guid, symbol=' ', z=0):
        """:param guid: globally unique identifier
        :type guid: :class:`int`
        """
        self._guid = guid
        self.components = {}
        self.symbol = symbol
        self.z = z
        self.removable = False

    def __repr__(self):
        return '{0}({1})'.format(type(self).__name__, self._guid)

    def __hash__(self):
        return self._guid

    def __eq__(self, other):
        return self._guid == hash(other)

    def hasComponent(self, component):
        if component.__name__ in self.components:
            return True
        else:
            return False

    def remove(self):
        # Mark for removal so that it is garbage collected
        self.removable = True