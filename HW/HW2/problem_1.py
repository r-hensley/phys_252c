import numpy as np
import random
import matplotlib.pyplot as plt

# Which formula gives an unbiased estimate of the population variance of a distribu-
# tion?  You might demonstrate this numerically, with a little simulation, for a gaussian dis-
# tribution.  To see the bias clearly, you need to use a value of N~20.
#
#     sigma1 = np.sqrt(sum([(i - mu)**2 for i in data])/len(data))
#     sigma2 = np.sqrt(sum([(i - mu)**2 for i in data])/(len(data)-1))


def gaus(x, mu, sigma):
    return np.exp(-((x-mu)**2)/(2*sigma**2))/(sigma*np.sqrt(2 * np.pi))


def gausdist(n, mu, sigma):
    # https://en.wikipedia.org/wiki/Box%E2%80%93Muller_transform
    if isinstance(n, float):
        if not n.is_integer():
            raise ValueError("Please give integer number for n")
    n = int(n)

    numbers = np.array([])
    while True:
        r1 = random.random()
        r2 = random.random()

        z0 = sigma * np.sqrt(-2*np.log(r1))*np.cos(2*np.pi*r2) + mu
        numbers = np.append(numbers, z0)
        if len(numbers) == n:
            break

        continue

        z1 = sigma * np.sqrt(-2 * np.log(r1)) * np.sin(2 * np.pi * r2) + mu
        numbers = np.append(numbers, z1)
        if len(numbers) == n:
            break
    return numbers


sigma = 1
mu = 0
sigma1_data = np.array([])
sigma2_data = np.array([])

for _ in range(100000):
    # data = gausdist(20, mu, sigma)
    data = [random.gauss(mu, sigma) for _ in range(20)]

    sigma1 = np.sqrt(sum([(i - mu)**2 for i in data])/len(data))
    sigma2 = np.sqrt(sum([(i - mu)**2 for i in data])/(len(data)-1))

    sigma1_data = np.append(sigma1_data, sigma1)
    sigma2_data = np.append(sigma2_data, sigma2)

f, (ax1, ax2) = plt.subplots(1, 2)
f.suptitle(f"Comparing variance calculations (μ={mu}, σ={sigma})")

ax1.hist(sigma1_data, 30, (sigma-0.5, sigma+0.5))
ax1.set_title("1/N Variance")
ax1.set_xlabel(f"σ")
ax1.axvline(sigma, color="#000000")

ax2.hist(sigma2_data, 30, (sigma-0.5, sigma+0.5))
ax2.set_title("1/N-1 Variance")
ax2.set_xlabel(f"σ")
ax2.axvline(sigma, color="#000000")

plt.subplots_adjust(wspace=0.3)
plt.show()
