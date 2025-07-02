# 由于FLAG中BCL参数化的a0₂并未给出，此文件用于计算a0₂，计算方法为解f+(0)=f0(0)关于a0₂的一元方程。
import math
import sympy as sp

ap = [0.0, 0.0, 0.0, 0.0]
x = sp.IndexedBase('x')
a0 = [0, 0, x]  # 列表长度根据实际的N修改，一般为3或4

m1 = 5.27966
m2 = 0.495644
mBstar = 5.3252
ap[0] = 0.471
ap[1] = -0.74
ap[2] = 0.32
# ap[3] = 2.11
a0[0] = 0.301
a0[1] = 0.4
# a0[2] = 0.2
# 根据要计算的列表填写数据

tp = (m1 + m2)**2
t0 = (m1 + m2) * (math.sqrt(m1) - math.sqrt(m2))**2

# tp = (m1 + m2)**2
# tm = (m1 - m2)**2
# t0 = tp - math.sqrt(tp*(tp - tm))
# 根据实际情况修改


def z(qs):
    # ref eq.524
    return (math.sqrt(tp - qs) - math.sqrt(tp - t0)) / (math.sqrt(tp - qs) + math.sqrt(tp - t0))


def fpBCL(qs):
    # ref: eq.533
    result = 0
    for n in range(0, 3):  # 根据N修改
        term = (z(qs)**n - (-1)**(n - 3) * n / 3 * z(qs)**3) * ap[n]
        result += term
    return 1 / (1 - qs / mBstar**2) * result


def f0BCL(qs):
    # ref: eq.534
    result = 0
    for n in range(0, 3):  # 根据N修改
        term = a0[n] * z(qs)**n
        result += term
    return result


Sol = sp.solve(f0BCL(0) - fpBCL(0), a0)  # 解一元方程
a0 = list(Sol[0])

print(a0)
