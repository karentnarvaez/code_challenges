# timestamp 	 user1 	 path:/home
# timestamp 	 user2	 path:/product
# timestamp		 user1	 path:/config


# Sequence of 5 most common 3 pages

# logs from single day

# user1: {A,B,C: 2, B,D,E:5 }
# user2: {A,B,G: 2, B,D,E:5 }
# user3: {A,B,C: 2, B,D,I:5 }
# Output: ABC: 4 ABG: 2 BDE: 10 BDI 5 = BDE, BDI, ABC


class LogEntry:

	def __init__(self, date, user, path):
		self.date = date
		self.user = user
		self.path = path


def analize_logs(logs_list):
	"""
	:param log_list list[LogEntry]: 
	"""
	logs_by_user = split_log_by_user(logs_list)
	patterns_frecuencies = count_patterns(logs_by_user)

	return get_the_k_most_common(patterns_frecuencies, k)


def get_the_k_most_common(patterns_count, k):
	result = list()

	for pattern, count in patterns_count.items():
		result.append((count, pattern))

	result.sort(reverse=true)
	return result[:k]


def split_log_by_user(logs_list):
	# { user1: [logs], user2: [logs]}
	result = dict()
	for line in logs_list:
		if line.user in result:
			result[line.user].append(line)
		else:
			result[line.user] = [line]

	for k, v in result.items():
		result[k] = sorted(v)

	return result


def count_patterns(logs_by_user):
	result = dict()

	for logs in logs_by_user.values():
		get_subpatterns(logs, result)

	return result


def get_subpatterns(logs, result):
	for i in range(len(logs)-2):
		pattern = logs[i].path + logs[i+1].path + logs[i+2].path 

		if pattern in result:
			result[pattern] += 1
		else:
			result[pattern] = 1





# LogEntry(dt.datetime().now())
# analize_logs()




