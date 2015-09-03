
import random

#Exercise 8.1
def has_duplicates(x):
	for i in x:
		if (filter(lambda a: a == i, x).__len__() > 1):
			return True

	return False


def populateBirthdays(number):
	return map(lambda _: random.randrange(1, 365, 1), range(number))

def generateBirthdayStats(iterations):
	x = filter(lambda x: x == True , map(lambda _: has_duplicates(populateBirthdays(23)), range(iterations)) ).__len__() / iterations
	return x


print generateBirthdayStats(100000)

