# Validate if you can form the string based on a given dictionary 
#
# "catfoxdog" ("cat", "dog" "cow", "foxdog") => True
# "catfoxdog" ("cat", "dog" "cow") => False
# "catfoxcat" ("cat", "dog" "cow") => False
# "" ("cat", "dog" "cow") => True
# "catfoxdog" ("catfox", "dog", "cat") => False
# "catfoxdog" ("catfox", "foxdog", "cat") => True
# "catfoxcat" () => False // dict will have at least 1 valid word
# "catsdog" ("cat", "dog") => False // dict will have at least 1 valid word
# "catsdog" ("cat", "dog" "cats") => True // dict will have at least 1 valid word

def find_words(target, dictionary):
	# target: str
	# dictionary: list
	if target == "":
		return True

	for word in dictionary:		
		if target.startswith(word):
			# target catfoxdog 0-3-1 = 0:2=
			# word cat => 3			
			if find_words(target[len(word):], dictionary) == True:
				return True

	return False

print(find_words("catfoxdog", ["cat", "dog", "cow", "foxdog"]))
print(find_words("catfoxdog", ["cat", "dog", "cow"]))
print(find_words("catfoxcat", ("cat", "dog", "cow")))
print(find_words("", ("cat", "dog", "cow")))
print(find_words("catfoxdog", ["catfox", "dog", "cat"]))
print(find_words("catfoxdog", ("catfox", "foxdog", "cat")))
print(find_words("catfoxcat", ()))
print(find_words("catsdog", ("cat", "dog")))
print(find_words("catsdog", ("cat", "dog", "cats")))


