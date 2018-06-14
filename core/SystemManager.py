from core.Exceptions import *
from core.Singleton import Singleton

@Singleton
class SystemManager(object):
    def __init__(self):
        pass
    
    # A container and manager for :class:`ecs.models.System` objects.
    def __init__(self):
        pass
        
    def Init(self):
        self._systems = []
        self._system_types = {}

    # Allow getting the list of systems but not directly setting it.
    @property
    def systems(self):
        return self._systems

    def get_system_of_type(self, system_type):
        if system_type in self._system_types:
            return self._system_types[system_type]
        else:
            return None

    # Add a sub-system to the system manager
    def add_system(self, system_instance, priority=0):
        system_type = type(system_instance)
        if system_type in self._system_types:
            raise DuplicateSystemTypeError(system_type)

        system_instance.init()

        self._system_types[system_type] = system_instance
        self._systems.append(system_instance)

        system_instance.priority = priority

        # Sorts into ascending list, reverse so that higher number means more important
        self._systems.sort(key=lambda x: x.priority)
        self._systems = self._systems[::-1]

    def remove_system(self, system_type):
        system = self._system_types[system_type]
        self._systems.remove(system)
        del self._system_types[system_type]

    # Run each system's ``update()`` method for this frame. The systems
    # are run in the order in which they were added.
    def update(self, dt):

        # Iterating over a list of systems instead of values in a dictionary is
        # noticeably faster. I maintain a list in addition to a dictionary
        # specifically for this purpose.
        #
        # Though initially I had the entity manager being passed through to
        # each update() method, this turns out to cause quite a large
        # performance penalty. So now it is just set on each system.
        for system in self._systems:
            system.update(dt)