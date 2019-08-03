import matplotlib
matplotlib.use("TKAgg")
from matplotlib import pyplot as plt
import numpy as np
import pickle

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
def get(path):
    x=[]
    y=[]
    z=[]
    l = []
    s = 0
    with open(path,'rb') as f:
        a = pickle.load(f)
    for i in a:
        i1,i2,i3=i
        x.append(i1)
        y.append(i2)
        z.append(i3)
        l.append(s)
        s=s+1
    return x,y,z,l


x,y,z,l = get('curiosity/TDW_A2C_step_loss_reward_sum.p')

ry = np.array(z)
ry = moving_average(-1*ry,n=10)
#print(l,y)
plt.plot(ry)
plt.show()
#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)





#p1, = ax.plot(l,y)
#p2, = ax.plot(x2,y2)
#p3, = ax.plot(x3,y3)


#ax.legend([p1, p2,p3], ["whole","random","subset"], loc='best')


#plt.savefig('finalgg.png')