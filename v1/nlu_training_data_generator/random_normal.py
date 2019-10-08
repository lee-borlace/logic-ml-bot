# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 20:17:06 2019

@author: LeeBorlace
"""


import numpy as np


# Get a normally distributed random number most highly concentrated around min_val and least highly around max_val
def normal_distribution_random(min_val, max_val):
    # Get a random number between 0 and 1, distributed normally around 0
    mu, sigma = 0, 0.26
    sample = abs(np.random.normal(mu, sigma, 1)[0])
    
    number_range = max_val-min_val+1
    
    retval = int(min_val + (number_range * sample))
    
    return min(retval, max_val)

samples = []

max_val = 99

for i in range(200000):
    sample = normal_distribution_random(0,max_val)
    samples.append(sample)
    
#for i in range(max_val+1) :
#    found = False
#    for sample in samples:
#        if sample == i:
#            found = True
#    
#    if not found:
#        print(f"Didn't find {i}")
#    else:
#        print(f"Found {i}")
            
    
    
import matplotlib.pyplot as plt
count, bins, ignored = plt.hist(samples, 100, density=True)
#plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=2, color='r')
plt.show()    