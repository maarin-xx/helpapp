import numpy as np

def aver():
    # Read the array from disk
    new_data = np.loadtxt('test.txt')
    # Note that this returned a 2D array!
    print
    new_data.shape
    n=new_data.shape[0]
    m=new_data.shape[1]
