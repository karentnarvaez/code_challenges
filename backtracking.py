# Exercise 1:
# Given a list of integers and a target number
# find all the ways you can have the target adding numbers

class FindSum():

	def __init__(self, numbers, target):
		self.numbers = numbers
		self.target = target
		self.solution = [None for i in numbers]
		self.acumulator = 0

	def backtracking(self, k):
		if k == len(self.numbers):
			if self.acumulator == self.target:
				numbers_solution = [self.numbers[n] for n in range(0, len(self.numbers)) if self.solution[n] == True ]
				print(numbers_solution)
				return True
		else:
			self.acumulator += self.numbers[k]
			self.solution[k] = True
			if self.backtracking(k+1) == True:
				return True 
			self.acumulator -= self.numbers[k]
			self.solution[k] = None



			self.acumulator += 0
			self.solution[k] = False
			if self.backtracking(k+1) == True:
				return True 
			self.acumulator -= 0
			self.solution[k] = None

		return False

# case = FindSum([i for i in range(0, 10)], 17)
# case.backtracking(0)

# Exercise 2:
# given a list of integers get all permutations


class FindPermutations():

	def __init__(self, numbers):
		self.numbers = numbers
		self.used = [False for n in self.numbers]
		self.solution = list()

	def backtracking(self, numbers):
		if False not in self.used:
			print(self.solution)
		
		else:
			for n in range(0, len(self.numbers)):
				if self.used[n] == False:			
					self.used[n] = True
					self.solution.append(self.numbers[n])

					self.backtracking(self.numbers[n+1:len(self.numbers)])

					self.used[n] = False
					self.solution.pop()

		return

numbers = [i for i in range(0, 4)]

case = FindPermutations(numbers)
case.backtracking(numbers)
