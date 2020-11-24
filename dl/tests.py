from django.test import TestCase
import operator
# Create your tests here.
test = [{'name': 'tom', 'salary': 20000}, {'name': 'jack', 'salary': 15000}, {'name': 'liming', 'salary': 10000}, ]
test.sort(key=operator.itemgetter('salary'))
print(test)


def xx(x):
    a = []
    for i in range(4):
        print(a)
        a.append(i * x)
    return a


def multipliers():
    a = [lambda x: i * x for i in range(4)]
    return a

# print([m(2) for m in multipliers()])
