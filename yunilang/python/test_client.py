import yuni
import numpy
np = yuni.py.numpy
max = yuni.py.prelude.max
print(dir(np.array([])))
print(numpy.array([1,2.3,3]) + numpy.array([1,2.3,3]))
x = np.array([1,2,3.3])
y = np.array([1,2,3.3])
print(x)
print(y)
print(x + y)

# TODO: websocket のやりとりを一つの実装だけにして、各言語はstdioでやりとりする
#       websocket 以外の接続も設計する
