import numpy as np
import random
import matplotlib.pyplot as plt

# 5.  Fit  the  resonance  data  from  problem  4,  this  time  using  a  linear  least  squares  ap-
# proach, and the full mass spectrum, binned into 25 GeV bins.  This time do not assume
# you  know  the  background  rate,  but  let  it  be  one  of  the  parameters  for  which  you  fit.
# Please quote the full covariance matrix.  What is the correlation coefficient between the
# measured cross section and the measured background rate?

# y~ = b + s * Gint(lo_i, hi_i)


def gint(_mu, _sigma, xlow, xhigh):
    precision = 100
    dx = (xhigh - xlow) / precision

    sum = 0
    for i in range(precision):
        x = xlow + dx*i + dx/2
        sum += np.exp(-(x-_mu)**2 / (2 * _sigma**2))

    return sum * dx / (_sigma * ROOT2PI)


def gaus(_mu, _sigma):
    return np.exp(-(x - _mu) ** 2 / (2 * _sigma ** 2)) * bin_width / (_sigma * ROOT2PI)


ROOT2PI = 2.50662827463

with open("../problem_4/Data/resonance.dat", "r") as f:
    data = f.read().replace(' ', '').splitlines()

data = [float(i) for i in data]
mu = 700
sigma = 50
luminosity = 1
efficiency = 1

fig, ax = plt.subplots()
n, bins, patches = ax.hist(data, 36, (100, 1000), label="Resonance data")
bin_width = bins[1] - bins[0]
print(bin_width)
print(len(bins), bins)

A = np.zeros((36, 2))
B = np.zeros((36, 1))
for i, x_i in enumerate(n):
    A[i][0] = 25  # bin width
    A[i][1] = gint(mu, sigma, bins[i], bins[i+1])  # percentage of gaussian
    B[i][0] = n[i]  # bin value
At = np.matrix.transpose(A)
AtA = np.matmul(At, A)
AtA_inv = np.linalg.inv(AtA)
AtA_invAt = np.matmul(AtA_inv, At)
solution = np.matmul(AtA_invAt, B)  # 2 element column matrix [[background], [cross-section]]
print(f"{A=}\n{B=}")
print(f"{solution=}")

# Solution:
# [[ 10.1271681 ],
#  [885.54871282]]

# Variance method
A = np.zeros((2, 2))
B = np.zeros((2, 1))
for i, n_i in enumerate(n):
    error = np.sqrt(n_i)
    error_squared = error**2
    g_percent = gint(mu, sigma, bins[i], bins[i + 1])
    A[0][0] += bin_width**2/error_squared
    A[0][1] += bin_width * g_percent/error_squared
    A[1][1] += g_percent**2 / error_squared
    B[0][0] += bin_width * n_i/error_squared
    B[1][0] += g_percent*n_i / error_squared
A[1][0] = A[0][1]

# Variance matrix:
# [[8.33272555e+01 6.74275697e-02]
#  [6.74275697e-02 3.58186906e-04]]
# Covariance matrix:
# [[ 1.41574427e-02 -2.66509451e+00]
#  [-2.66509451e+00  3.29353426e+03]]
# Solution:
# [[ 10.07660393]
#  [894.9492    ]]

print(f"Variance matrix: \n{A}")
Ainv = np.linalg.inv(A)
solution = np.matmul(Ainv, B)
print(f"Covariance matrix: \n{Ainv}")
print(f"Solution: \n{solution}")

# Plot the fit
x = np.linspace(100, 1000, 37)  # 100, 125, 150, ..., 950, 975, 1000
y = np.zeros(37)

for i, x_i in enumerate(n):
    y[i] = solution[0][0]*bin_width + solution[1][0]*gint(mu, sigma, bins[i], bins[i+1])

ax.plot(x, y, "r+", label="Least squares fit")
ax.set_title("Linear least squares fit on resonance data over background")
ax.set_xlabel("Mass (GeV)")
ax.set_ylabel("Events per 25 GeV")

ax.legend()
plt.show()
