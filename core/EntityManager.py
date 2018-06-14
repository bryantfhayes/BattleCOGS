from core.Entity import Entity
from core.Singleton import Singleton

import six

@Singleton
class EntityManager(object):
    def __init__(self):
        pass

    def Init(self):
        self._database = {}
        self._next_guid = 0

    # Get this manager's database. Direct modification not permitted
    @property
    def database(self):
        return self._database

    # Return a new entity with the lowest GUID available. No stored references
    def create_entity(self, symbol, z=0):
        entity = Entity(self._next_guid, symbol, z)
        self._next_guid += 1
        return entity

    # Add a component to the database and associate it with the given entity
    def add_component(self, entity, component_instance):
        component_type = type(component_instance)
        if component_type not in self._database:
            self._database[component_type] = {}

        self._database[component_type][entity] = component_instance

        # Add easy reference for entity
        entity.components[component_type.__name__] = component_instance

    # Remove the component of 'type' associated with an entity in database
    def remove_component(self, entity, component_type):
        try:
            del self._database[component_type][entity]
            del entity.components[component_type.__name__]
            if self._database[component_type] == {}:
                del self._database[component_type]
        except KeyError:
            pass

    # Returns an iterator over (entity, component_instance)
    def pairs_for_type(self, component_type):
        try:
            return six.iteritems(self._database[component_type])
        except KeyError:
            return six.iteritems({})

    # Return the instance of ``component_type`` for the entity from the database
    def component_for_entity(self, entity, component_type):
        try:
            return self._database[component_type][entity]
        except KeyError:
            raise NonexistentComponentTypeForEntity(
                entity, component_type)

    # Remove all components from the database that are associated with the entity
    def remove_entity(self, entity):
        for comp_type in list(self._database.keys()):
            try:
                del self._database[comp_type][entity]
                if self._database[comp_type] == {}:
                    del self._database[comp_type]
            except KeyError:
                pass
