# Done

# python3 py_mergesort.py

# Ran in my native system macOS Catalina Version 10.15.6
#
# Time took -  34.585477925
# Time took -  34.765227752
# Time took -  36.743492262
# Time took -  38.992350808

# Ran on a Docker Container
#
# Time took -  39.245423599997594
# Time took -  40.03151469999284
# Time took -  42.721318200005044
# Time took -  37.69889829999738

# Ran on GCP
#
# Time took -  66.66056957300043
# Time took -  65.51820057799978
# Time took -  65.97373585600053
# Time took -  65.79712596900026

# Ran in docker inside GCP
#
# Time took -  48.77300166399982
# Time took -  48.19091662699975
# Time took -  48.35740338800133
# Time took -  48.00048861899995

# docker run -t python-merge py_mergesort.py

from contextlib import contextmanager
from multiprocessing import Manager, Pool
import threading
from time import perf_counter
import random

@contextmanager
def pool_com_process(size):
    pool = Pool(size)
    yield pool
    pool.close()
    pool.join()

def merge(mergeArray):
    if len(mergeArray) <= 1:
        return mergeArray
    midVal = int(len(mergeArray) / 2)
    return merge_together(merge(mergeArray[0:midVal]), merge(mergeArray[midVal:]))

def merge_together(left_tree, right_tree):
    listSort = []
    left_tree = left_tree[:]
    right_tree = right_tree[:]
    while len(left_tree) > 0 or len(right_tree) > 0:
        if len(left_tree) > 0 and len(right_tree) > 0:
            if left_tree[0] <= right_tree[0]:
                listSort.append(left_tree.pop(0))
            else:
                listSort.append(right_tree.pop(0))
        if len(left_tree) > 0:
            listSort.append(left_tree.pop(0))
        if len(right_tree) > 0:
            listSort.append(right_tree.pop(0))
    return listSort

if __name__ == '__main__':
    #To deternine the sample size
    len_n = ((2 * 0.01) / 0.01) ** 2
    p_threads = 4
    arr_length = 300000
    arr_random = [random.randint(0, n * 100) for n in range(100)]
    start = perf_counter()
    for i in range(int(len_n)):
        for i in range(p_threads):
            pace = int(arr_length / p_threads)
            data_man = Manager()
            results = data_man.list()
            with pool_com_process(size=p_threads) as pool:
                for n in range(p_threads):
                    if n < p_threads - 1:
                        valc = arr_random[n * pace:(n + 1) * pace]
                    else:
                        valc = arr_random[n * pace:]
                    pool.apply_async(results.append(merge(valc)))

            while len(results) > 1:
                with pool_com_process(size=p_threads) as pool:
                    pool.apply_async(results.append(merge_together(results.pop(0), results.pop(0))))
    stop = perf_counter() 
    print("Time elapsed - ", stop-start)