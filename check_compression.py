# Given a string and a possible compression
# tell if that compression belongs to the string 

def validate_compression(text, compression):
	words = text.split(" ")
	tokens = compression.split(" ")

	if len(words) != len(tokens):
		return False

	words_to_tokens = {}

	for i, word in enumerate(words):
		current_token = tokens[i]

		if word in words_to_tokens:
			value_expected = words_to_tokens[word]

			if current_token != value_expected:
				print(f"Error with word {word} expected value {value_expected} found {current_token}")
				return False
		else:
			words_to_tokens[word] = current_token

	return True


A = ""
B = ""
#output: True
print(validate_compression(A, B))

A = "victor hugo pepe pepe victor"
B = "x h p p x"
# True
print(validate_compression(A, B))

A = "victor hugo pepe pepe victor"
B = "x h p p s"
# False
print(validate_compression(A, B))

A = "victor hugo pepe pepe victor"
B = "x h s p x"
# False
print(validate_compression(A, B))

A = "victor hugo pepe pepe victor"
B = ""
# False
print(validate_compression(A, B))

A = "victor hugo pepe pepe"
B = "x h s p x"
# False
print(validate_compression(A, B))
