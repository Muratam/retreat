from py import yuni
import numpy
np = yuni.py.numpy
yuni.py.prelude.print("client python")
print(numpy.array([1,2.3,3]) + numpy.array([1,2.3,3]))
print(np.array([1,2.3,3]) + np.array([1,2.3,3]))
print(sorted([5,4,2,9], key=lambda x: -x))
print(yuni.py.prelude.sorted([5,4,2,9], key=lambda x: -x))
