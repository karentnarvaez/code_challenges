'''
You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed,
the only constraint stopping you from robbing each of them is that adjacent houses have security system connected and
it will automatically contact the police if two adjacent houses were broken into on the same night.

Given a list of non-negative integers representing the amount of money of each house,
determine the maximum amount of money you can rob tonight without alerting the police.

 
Input: nums = [1,2,3,1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
             Total amount you can rob = 1 + 3 = 4.
             
Input: nums = [2,7,9,3,1]
Output: 12
Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
             Total amount you can rob = 2 + 9 + 1 = 12.

Input: []
Output: 0

[5] => 

when i == 0
	max = l[0]
maxes [5]

[5 20] => 20 lastPreviousMax
when i == 1
 bigger = max(l[0], l[1])
maxes [5,20]

[5 20 9] => 20 previousMax
when i == 2
bigger = max(max[max.length - 2] + l.last , max.last])
maxes = [5,20]

[5 20 9 30] => 5 + 9 || 20 + 30 || 5 + 30 || 9 +5 || 20 || 9
when i == 3
bigger = max(maxes[maxes.length - 1], l[i] + maxes[maxes.length - 2])

'''

def findMaxRobbery(houses):
    maximum_list = [0]
  
    for i in range(len(houses)): 
        if i == 0:
            maximum_list.append(houses[i])
        elif i == 1:
            maximum_list.append(max(houses[0:2]))
        else:
            maximum_list.append(max(maximum_list[i], maximum_list[i-1] + houses[i]))
    
    return maximum_list[len(houses)-1]
                          

                          
print(findMaxRobbery([5, 20, 9]))