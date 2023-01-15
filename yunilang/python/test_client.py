import yuni
import numpy
np = yuni.py.numpy
max = yuni.py.prelude.max
# print(dir(np.array([])))
print(np.array([1,2.3,3]) + np.array([1,2.3,3]))
print(sorted([5,4,2,9], key=lambda x: -x))
print(yuni.py.prelude.sorted([5,4,2,9], key=lambda x: -x))
# print(numpy.array([1,2.3,3]) + numpy.array([1,2.3,3]))
# print(numpy.array([1,2.3,3]) + np.array([1,2.3,3]))
# print(np.array([1,2.3,3]) + numpy.array([1,2.3,3]))

# TODO: websocket のやりとりを一つの実装だけにして、各言語はstdioでやりとりする
#       websocket 以外の接続も設計する
