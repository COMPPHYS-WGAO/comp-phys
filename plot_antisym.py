
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import argparse
    

def si(x1, x2, n1=1, n2=2, a=1.0):
    return 2/a*(np.sin(n1*np.pi*x1/a)*np.sin(n2*np.pi*x2/a)-np.sin(n1*np.pi*x2/a)*np.sin(n2*np.pi*x1/a))   
 

parser = argparse.ArgumentParser()
parser.add_argument('-n1', type = float)
parser.add_argument('-n2', type = float)
parser.add_argument('-a', type = float)
args = parser.parse_args()
n01 = args.n1
n02 = args.n2
a0 = args.a

x = y = np.linspace(-1.5, 1.5, 100)
xv, yv = np.meshgrid(x,y)
z = si(xv, yv)
z2 = z**2
    

fig = plt.figure()
plt.suptitle('Antisymmetric Spatial Wave Function.') 

ax = fig.add_subplot(121, projection = '3d')
ax.plot_surface(xv, yv, z, rstride = 1, cstride = 1, cmap=cm.coolwarm, linewidth = 0)
plt.title(‘wave function')

bx = fig.add_subplot(122, projection = '3d')
bx.plot_surface(xv, yv, z2, rstride = 1, cstride = 1, cmap=cm.coolwarm, linewidth = 0)
plt.title('probability density')

txt = 'The "effective" interaction between two neutral Fermions (both spin up) \nthat arises from the symmetry requirement on the total wave function.'
fig.text(0.1, 0.02, txt)

plt.show()