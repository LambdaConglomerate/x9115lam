
#Exercise 8.1
def has_duplicates(x):
	for i in x:
		if (filter(lambda a: a == i, x).__len__() > 1):
			return True

	return False


