# Done

# python3 py_dns.py names1.txt names2.txt names3.txt names4.txt names5.txt results.txt

# Ran in my native system macOS Catalina Version 10.15.6
#
# Total time took is 1.1709082126617432s
# Second Time: 0.01732921600341797

# Ran on a Docker Container
#
# Total time took is 0.11195778846740723
# Second Time 0.0030951499938964844

# Ran on GCP
#
# First time: 3.823492164000072
# Second time: 1.5596253890000753
# 1.1851327970000511
# 0.20729835499992078

# Ran in docker inside GCP
#
# First Time: 3.131492999000102
# Second Time: 2.231737143999908
# 1.5080837640000482
# 1.2603184399999918

# docker run -it python-dns py_dns.py names1.txt names2.txt names3.txt names4.txt names5.txt results.txt

from contextlib import contextmanager
from multiprocessing import Manager, Pool
import threading
from time import perf_counter
import sys
import socket
import time

@contextmanager
def pool_com_process(size):
    pool = Pool(size)
    yield pool
    pool.close()
    pool.join()

class InitiateThread(threading.Thread):
   def __init__(self, ip, result):
      self.hostname = hostname
      self.result = result
      threading.Thread.__init__(self)

   def run(self):
      hostname = self.hostname
      try:
         IP = socket.gethostbyname(hostname.strip())
         self.result[hostname] = {'host': hostname.strip(), 'IP': IP}
      except socket.gaierror:
         self.result[hostname] = {'host': 'dnslookup error', 'IP': hostname.strip()}

if __name__ == '__main__':
   n = len(sys.argv)
   outfile = sys.argv[-1]
   result = {}
   if n < 4:
      print("Need input file to proceed further")
      sys.exit()
   
   ip_addresses = set()
   for i in range(1, n - 1):
      inputs = open(sys.argv[i], "r")
      for hostname in inputs:
         lookup_threads = [InitiateThread(hostname.strip(), result)]
         for t in lookup_threads:
            t.start()
      inputs.close()

   #To deternine the sample size
   len_n = ((2 * 0.01) / 0.01) ** 2

   start = perf_counter()

   main_thread = threading.currentThread()
   for i in range(int(len_n)):
      for thread in threading.enumerate():
         if thread is main_thread:
            continue
         thread.join()
   end = perf_counter()
   elapsed = end - start
   print("Elapsed time: ", elapsed)
   
   f =  open(outfile, "w")
   for hostname, ip in result.items():
      f = open(outfile, "a")
      f.write(str(ip['host']) + ", " + str(ip['IP'])+'\n')
      f.close()