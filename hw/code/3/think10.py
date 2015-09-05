
import random

#Exercise 8.1
def has_duplicates(x):
	for i in x:
		if (filter(lambda a: a == i, x).__len__() > 1):
			return True

	return False


def populateBirthdays(number):
	return map(lambda _: random.randrange(1, 365, 1), range(number))

def generateBirthdayStats(students, iterations):
	x = filter(lambda x: x == True , map(lambda _: has_duplicates(populateBirthdays(students)), range(iterations)) ).__len__() /float(iterations)
	return x


a = [1, 2, 3, 4]
b = [2, 5, 6, 5]
print a, " has duplicates?: ", has_duplicates(a)
print b, " has duplicates?: ", has_duplicates(b)

print "Probability of 23 students having the same birthday: " , generateBirthdayStats(23, 100000)


