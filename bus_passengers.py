from enum import Enum
import heapq
from functools import total_ordering

@total_ordering
class Passenger:

	def __init__(self, identifier, start, end):
		self.id = identifier
		self.start = start
		self.end = end

	def __eq__(self, other):
		return self.end == other.end

	def __lt__(self, other):
		return not(self.end < other.end)

	def __repr__(self):
		return "(" + str(self.start) + ", " + str(self.end) + ")"

EXIT = 1
ENTER = 2

class Event:

	def __init__(self, passenger_id, event_type, time):
		# passenger_id int: index to the passenger
		# event_type EventType:
		# time int: given time in timeline 
		self.passenger_id = passenger_id
		self.type = event_type
		self.time = time

class Bus:

	def __init__(self, capacity):
		# :param capacity int:
		self.capacity = capacity
		self.passengers = []
		self.current_active = set()
		self.final = []

	def pick_passenger_up(self, passenger):
		# :param passenger Passenger:
		# :return 
		heapq.heappush(self.passengers, passenger)
		self.current_active.add(passenger.id)

	def exchange_passenger(self, p, current_time):
		# remove the passenger that will take longer to get off	
		self.remove_ghosts(current_time)	
		worst = self.passengers[0]
		if worst < p:
			heapq.heappop(self.passengers)
			self.current_active.remove(worst.id)
			self.pick_passenger_up(p)

	def remove_ghosts(self, current_time):
		# :param current_time int:
		# print("before: ", self.passengers)		
		# print("time: ", current_time)		
		while len(self.passengers) > 0 and self.passengers[0].end < current_time:
			heapq.heappop(self.passengers)
		# print("after ", self.passengers)		

	def get_passenger_off(self, p):
		# :param index int: index for passenger to exit
		if p.id in self.current_active:
			self.final.append(p)
			self.current_active.remove(p.id)

	def is_full(self):
		# returns boolean
		return self.capacity == len(self.current_active)



def get_max_passengers(passengers, bus_capacity):
	"""
	:param passengers list((start, end)):
	:param capacity int:
	:return int: max number of passengers to be picked up
	"""
	max_number_passengers = 0
	bus = Bus(bus_capacity)

	passengers_obj = [Passenger(i, p[0], p[1]) for i, p in enumerate(passengers)] 
	passengers_obj.sort(key=lambda p: p.start) # sort passengers based on who will be picked sooner
	
	event_list = []
	for index, passenger in enumerate(passengers_obj):
		event_list.append(Event(index, ENTER, passenger.start))
		event_list.append(Event(index, EXIT, passenger.end))

	event_list.sort(key=lambda e: (e.time, e.type))
	for e in event_list:
		current_passenger = passengers_obj[e.passenger_id]

		if e.type == ENTER:
			if bus.is_full():
				bus.exchange_passenger(current_passenger, e.time) 
			else:		
				bus.pick_passenger_up(current_passenger)
				max_number_passengers += 1
		else:
			bus.get_passenger_off(current_passenger)

	print("passengers during day: ", bus.final)
	return max_number_passengers


A = [(1,6), (2,4), (5,8)]
k = 1
print(get_max_passengers(A, k))


A = [(1,4), (2,6), (1,5), (2,3), (4,6), (3,6)]
k = 2
print(get_max_passengers(A, k))