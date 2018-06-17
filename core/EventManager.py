from core.Events import *
from core.Singleton import Singleton

from core.Exceptions import *

@Singleton
class EventManager(object):
	def __init__(self):
		self._events = {}

	def Init(self):
		# For each possible event, create a list which will hold the subscribed functions to call
		for e in EVENTS:
			self._events[e] = []

	def subscribe(self, event, fn):
		# Confirm event exists
		if event not in self._events:
			return

		# Add fn to end of list
		if fn not in self._events[event]:
			self._events[event].append(fn)

	def unsubscribe(self, event, fn):
		# Confirm event exists
		if event not in self._events:
			return

		if fn in self._event[event]:
			self._events[event].remove(fn)

	def fireEvent(self, event, args):
		return_arr = []

		# Confirm event exists
		if event not in self._events:
			return

		# Fire all registered functions for this event
		triggeredEvent = self._events[event]
		for fn in triggeredEvent:
			return_arr.append(fn(args))

		return return_arr