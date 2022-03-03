import numpy as np
import matplotlib.pyplot as plt

# 1. Using the resonance spectrum data from the previous homework assignment, apply a
# Bayesian likelihood method to obtain a posterior pdf in the signal cross section, based
# on a binned Poisson likelihood.  From this posterior, quote the most probable value and
# a central 68.27% confidence interval.  Here we assume we know the mass and width of
# the peak, and the number of background events per GeV.  Assume a flat prior pdf in s.

BIN_WIDTH = 25
ROOT2PI = 2.50662827463
MU = 700
SIGMA = 50


def gint(mu, sigma, xlow, xhigh):
    precision = 100
    dx = (xhigh - xlow) / precision

    int_sum = 0
    for i in range(precision):
        x = xlow + dx*i + dx/2
        int_sum += np.exp(-(x-mu)**2 / (2 * sigma**2))

    return int_sum * dx / (sigma * ROOT2PI)


def log_likelihood(_n, _bins, _s):
    # print(f"{_s=}")
    log_likelihood_sum = 0
    for bin_number, bin_value in enumerate(_n):
        # print(f"{_bins[bin_number]=}")
        # print(f"{_bins[bin_number+1]=}")
        # print(f"{bin_number=}")
        # print(f"{bin_value=}")
        mu = 10 * BIN_WIDTH + _s * gint(MU, SIGMA, _bins[bin_number], _bins[bin_number+1])
        # print(f"{mu=}")
        # print("")
        log_likelihood_sum += mu - bin_value * np.log(mu)
    return -log_likelihood_sum


def integrate_likelihood(_x, _y, _low_bin, _high_bin):
    dx = _x[1] - _x[0]

    int_sum = 0
    for i in range(_low_bin, _high_bin+1):
        current_bin = _low_bin + dx * i
        int_sum += dx * _y[current_bin]


with open("../../Data/resonance.dat", "r") as f:
    data = f.read().replace(' ', '').splitlines()

data = [float(i) for i in data]
fig, ax = plt.subplots()

n, bins, patches = ax.hist(data, 36, (100, 1000), label="Resonance data")

precision = 5
max_s = 5000
number_of_bins = int(max_s/precision + 1)
likelihood_list_x = np.array([])
likelihood_list_y = np.array([])
base_likelihood = 0
for i, s in enumerate(np.linspace(0, max_s, number_of_bins)):
    next_likelihood = log_likelihood(n, bins, s)
    if s == 0:
        base_likelihood = next_likelihood
    if next_likelihood - base_likelihood < 0:
        break
    likelihood_list_x = np.append(likelihood_list_x, s)
    likelihood_list_y = np.append(likelihood_list_y, next_likelihood - base_likelihood)

# print(f"{likelihood_list_x=}")
# print(f"{likelihood_list_y=}")

# print(f"{max(likelihood_list[1])=}")
max_bin = np.where(likelihood_list_y == max(likelihood_list_y))[0][0]
print(f"{max_bin=}")


print("Likelihoods")
for i, j in enumerate(likelihood_list_x):
    # print(f"{likelihood_list_x[i]}: {likelihood_list_y[i]}")
    pass

print(f"Bin {max_bin}:\n{likelihood_list_x[max_bin]}: {likelihood_list_y[max_bin]}")

fig2, ax2 = plt.subplots()
ax2.plot(likelihood_list_x, likelihood_list_y)

# max_bin=184
# Likelihoods
# Bin 184:
# 920.0: 197.54595161386533

plt.show()
