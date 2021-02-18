# Done

# python3 py_multiply.py

# Ran in my native system macOS Catalina Version 10.15.6
#
# 805.937778031
# 819.08957042
# 827.0954972440001
# 845.8964010870001

# Ran on a Docker Container
#
# 455.19402889999765
# 460.9632053999994
# 474.0602813999976
# 485.43309769999905

# Ran on GCP
#
# 331.3474356280003
# 323.14612699300005
# 320.464658331
# 319.6493112090002

# Ran in the docker inside GCP
#
# 1360.722489574
# 1363.5188884689996
# 1481.028831472
# 1500.2958547320004

# docker run -t python-matrix py_multiply.py

from contextlib import contextmanager
from multiprocessing import Manager, Pool
import threading
import numpy as np
from time import perf_counter

@contextmanager
def pool_com_process(size):
    pool = Pool(size)
    yield pool
    pool.close()
    pool.join()

class pooling(threading.Thread):
    def __init__(self, num, matA, matB, res_dict):
        threading.Thread.__init__(self)
        self.tnum = num
        self.MxA = matA
        self.MxB = matB
        self.res_dict =  res_dict

    def run(self):
        rows = []
        columns = []
        for p in zip(range(self.MxB.shape[1]), range(self.MxA.shape[0])):
            fill_in1 = []
            fill_in2 = []
            for i in zip(range(self.MxB.shape[0]), range(self.MxA.shape[1])):
                fill_in1.append(self.MxB[i, p])
                fill_in2.append(self.MxA[p, i])
            columns.append(fill_in1)
            rows.append(fill_in2)

        result = np.zeros((0, self.MxA.shape[1]))
        fill_in = np.zeros((1, 0))
        for row in self.MxA[:]:
            for col in self.MxB.T:
                fill_in = np.concatenate((fill_in, row * col.T), 1)
            result = np.concatenate((result, fill_in), 0)
            fill_in = np.zeros((1, 0))

        mutexLock = threading.Lock()
        mutexLock.acquire()
        self.res_dict[self.tnum] = result
        mutexLock.release()

if __name__ == '__main__':
    # Matrix A that generates a matrix of 100 x 100
    matrixA = np.matrix(np.random.random((100, 100)))
    # Matrix B that generates a matrix of 100 x 100
    matrixB = np.matrix(np.random.random((100, 100)))
    mx_result = np.zeros((0, matrixB.shape[1]))
    thread_array = []
    no_of_thds = 4
    first = int(matrixA.shape[0] / no_of_thds)
    second = int(matrixA.shape[0] % no_of_thds)
    mxstart = 0
    outcomeDict = {}
    start = perf_counter()

    with pool_com_process(size=no_of_thds) as pool:
        for i in range(no_of_thds):
            if i < second:
                thread_array.append(pooling(i, matrixA[mxstart:mxstart+first+1], matrixB , outcomeDict))
                mxstart += 1
            else:
                thread_array.append(pooling(i, matrixA[mxstart:mxstart+first:], matrixB, outcomeDict))
            mxstart += first

    for th in thread_array:
       th.start()

    while len(outcomeDict.keys()) < no_of_thds:
        pass

    #To deternine the sample size
    len_n = ((2 * 0.01) / 0.01) ** 2

    for i in range(int(len_n)):
        for i in range(no_of_thds):
            mx_result = np.concatenate((mx_result, outcomeDict[i]), 0)

    stop = perf_counter()     
    print("Time took - ", stop-start)