import multiprocessing
import os

def test_function(arg1=1,arg2=2):
    string="arg1 = {0}, arg2 = {1}".format(arg1,arg2) +" from process id: "+ str(os.getpid())
    return string

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=3)
    for i in range(6):
        result = pool.apply_async(test_function)
        print(result.get(timeout=1))
    pool.close()
    pool.join()
