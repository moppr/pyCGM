import numpy as np

# data = np.array([[[1, 2, 3], [8, 8, 8], [10, 10, 10], [5, 5, 5], [5, 5, 5]],
#                  [[4, 5, 6], [7, 7, 7], [9, 9, 9], [4, 4, 4], [4, 4, 4]],
#                  [[7, 8, 9], [6, 6, 6], [8, 8, 8], [3, 3, 3], [3, 3, 3]],
#                  [[6, 7, 8], [4, 4, 4], [8, 8, 8], [2, 2, 2], [2, 2, 2]],
#                  [[5, 6, 7], [2, 2, 2], [8, 8, 8], [0, 0, 0], [0, 0, 0]]])
# result = np.zeros((5, 3), dtype=int)
# 
# for i, frame in enumerate(data):
#     result[i] = frame[0]
# 
# print(result)

# x = np.array([[5, 5, 5], [7, 7, 7]])
# y = x[0]
# z = x[1]
# print(type(x[0]))
# print(type(z - y))
# print(type(np.mean(np.array([y, z]), axis=0, dtype=int)))

#zeros = np.zeros((5, 5, 3), dtype=int)

# arr = np.array([9, 9, 9])
# arr2 = np.array([10, 10, 10])
# print(arr)
# print(arr2)
# print(arr + arr2)


# def e():
#     return 1, 2
# 
# 
# x = np.zeros(10)
# y = np.zeros(10)
# x[0], y[0] = e()
# print(x)
# print(y)

# x = np.array([1, 2, 3, 4, 5])
# print(np.sum(x))
# print(np.prod(x))

# class Foo:
#     @staticmethod
#     def e():
#         return 5
# 
# f = Foo()
# print(f.e())
# print(Foo.e())