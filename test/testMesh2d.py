import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.
def FF(y1, y2):
    return  -2*(y1/5)**3+3*(y1/3-y2/7)**2+3*(y2/9)**2

Y1 = np.arange(0, 4, 0.01)
Y2 = np.arange(0, 4, 0.01)
Y1, Y2 = np.meshgrid(Y1, Y2)
# R = np.sqrt(X**2 + Y**2)
Z = FF(Y1,Y2)

# Plot the surface.
surf = ax.plot_surface(Y1, Y2, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
# Customize the z axis.
ax.set_zlim(0, 4.01)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()

(N1, N2) = (4, 4) # Number of points in 2d meshgrid
# print(N1, ' ', N2)
(d1, d2) = (1, 1)
y1grd = [d1*i for i in range(0,N1+1)]
y2grd = [d1*j for j in range(0,N2+1)]

A = np.ndarray(shape=(N1+1, N2+1))
for j in range(N2+1):
    for i in range(N1+1):
        A[i,j] = ( (FF(y1grd[i], y2grd[j]) - FF(y1grd[i-1], y2grd[j]))/d1 if i > 0 else 0)
print(A.transpose())

# Phi definitions
def Phi(y1, j):
    return FF(y1grd[0],y2grd[j])+sum( (A[i,j] - A[i-1,j])*max(0,y1-y1grd[i-1]) for i in range(1, N1+1) )

print('============== Phi Checking ==========')
for j in range(N2+1):
    PhiVal = Phi(y1grd[2],j)
    FFval = FF(y1grd[2],y2grd[j])
    print(j, PhiVal, FFval, abs(PhiVal - FFval) )

# B