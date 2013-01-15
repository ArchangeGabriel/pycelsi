from scipy.integrate import odeint

y0_0 = 1
y1_0 = 0
z = [y0_0, y1_0]

def func(z, t):

    t = z[:]

    t[1] = -z[0]
    t[0] = z[1]

    return t

dt = 0.1

z = odeint(func, z, [0, dt])
print z

z = odeint(func, z[1], [0, dt])
print z
