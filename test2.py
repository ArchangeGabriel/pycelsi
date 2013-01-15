from scipy.integrate import odeint

y0_0 = 1
y1_0 = 0
z = [y0_0, y1_0]

def func(y, t):

    temp = y[0]

    y[0] = y[1]
    y[1] = -temp

    return y

dt = 0.1

z = odeint(func, z, [0, dt])
print z

z = odeint(func, z[1], [0, dt])
print z
