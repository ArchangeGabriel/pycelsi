from scipy.integrate import odeint

y0_0 = 1
y1_0 = 0
z = [y0_0, y1_0]

def func(z, t):

    t = z[0]

    z[0] = z[1]
    z[1] = t

    return z

dt = 0.1

z = odeint(func, z, [0, dt])
print z

z = odeint(func, z[1], [0, dt])
print z
