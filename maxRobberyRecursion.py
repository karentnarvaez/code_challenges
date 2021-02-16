# [1, 2, 3] => 4
# [] => 0
# [2, 20, 9] => 20
# [1, 2, 3, 4] => 6


houses = [7, 4, 2, 8, 2, 5]
cache = [None for h in houses]

def maxRobberyRecursion(k):
	if k >= len(houses):
		return 0
	elif k == len(houses) - 1:
		return houses[k]
	elif cache[k] is not None:
		return cache[k]
	else:
		res = max(houses[k] + maxRobberyRecursion(k+2), maxRobberyRecursion(k+1))
		cache[k] = res
		return res


print(maxRobberyRecursion(0))