# Error indicating that a component type does not exist for a certain entity.
class NonexistentComponentTypeForEntity(Exception):
    def __init__(self, entity, component_type):
        self.entity = entity
        self.component_type = component_type

    def __str__(self):
        return "Nonexistent component type: `{0}' for entity: `{1}'".format(
            self.component_type.__name__, self.entity)

# Error indicating that the system type already exists in the system manager.
class DuplicateSystemTypeError(Exception):
    def __init__(self, system_type):
        self.system_type = system_type

    def __str__(self):
        return "Duplicate system type: `{0}'".format(self.system_type.__name__)
