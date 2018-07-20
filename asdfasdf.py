import itertools
import operator

# print(operator.mul(4,5))
#
# h = [3,4,5]
# g = itertools.accumulate(h, operator.mul)
# # itertools.accumulate(h)


data = [1, 2, 3, 4, 5]
# result = itertools.accumulate(data, operator.mul)
# for each in result:
#     print(each)

k = itertools.combinations(data, 3)
print(k)
# for i in k:
#     print(i)

# arrr = []
# for i in range(0, sz):
#     arrr.append(funct())
