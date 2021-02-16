class Person: 

	def __init__(self, name, last_name, age):
		self.name = name
		self.last_name = last_name
		self.age = age


def sort_by_age(person_list):
	return sorted(person_list, key=lambda p: p.age, reverse=True)


def sort_by_last_name_and_name(person_list):
	return sorted(person_list, key=lambda p: (p.last_name, p.name, p.age))




people = [Person("Karent", "Narvaez", 29), Person("Gatin", "Padilla", 2), Person("Victor", "Padilla", 33)]

print([p.name for p in sort_by_age(people)])
print([p.name for p in sort_by_last_name_and_name(people)])