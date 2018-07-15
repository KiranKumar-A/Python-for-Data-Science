# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 00:18:03 2018

@author: KIRAN
"""
from statistics import mean
import numpy as np

import matplotlib.pyplot as plt

from matplotlib import style
style.use('fivethirtyeight')


#xs = [1,2,3,4,5,6]
#ys = [5,4,6,5,6,7]

#plt.plot(xs,ys)
#plt.scatter(xs,ys)
#plt.show()

xs = np.array([1,2,3,4,5,6], dtype = np.float64)
ys = np.array([5,4,6,5,6,7],dtype = np.float64)

#def best_fit_slope(xs,ys):
#    m = ( ((mean(xs)*mean(ys)) - mean(xs*ys)) /
#         ((mean(xs)*mean(xs))- mean(xs * xs)))
#    
#    return m

def best_fit_slope_intercept(xs,ys):
    m = ( ((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs))- mean(xs * xs)))
    b= mean(ys) - m*mean(xs)
    return m, b


#m = best_fit_slope(xs,ys)

m,b = best_fit_slope_intercept(xs, ys)

regression_line = [(m*x) + b for x in xs]

print(m,b)

predict_x = 8
predict_y = (m*predict_x)+b


plt.scatter(xs, ys)
plt.scatter(predict_x, predict_y, c = 'g')
plt.plot(xs, regression_line)
plt.show()
