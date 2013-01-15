from scipy.integrate import odeint

y0_0 = 1
y1_0 = 0
z = [y0_0, y1_0]

def func(y, t):

    dz = y[:]

    dz[1] = -y[0]
    dz[0] = y[1]

    return dz

dt = 0.1

z = odeint(func, z, [0, dt])
print z

z = odeint(func, z[1], [0, dt])
print z
