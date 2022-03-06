import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

# This file exists as a gutted version of the full problem for the purpose of showing the
# minimal steps necessary to find the correct peak for troubleshooting steps.

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


print(gint(700, 50, 678.5, 713.9))


def log_likelihood(_n, _bins, _s):
    log_likelihood_sum = 0

    # Iterate over bins in histogram
    for bin_number, bin_value in enumerate(_n):
        gauss = gint(MU, SIGMA, _bins[bin_number], _bins[bin_number+1])
        mu = 10 * BIN_WIDTH + _s * gauss
        log_likelihood_sum += mu - bin_value * np.log(mu)
        if _s == 1000:
            print(f"(mu_i, Log_likelihood, N_i) = {mu}, {-log_likelihood_sum}, {bin_value}, {gauss}")
    return -log_likelihood_sum


with open("../../Data/resonance.dat", "r") as f:
    data = f.read().replace(' ', '').splitlines()

data = [float(i) for i in data]

# Create histogram
fig, ax = plt.subplots()
n, bins, patches = ax.hist(data, 36, (100, 1000), label="Resonance data")

# Setup likelihood plot
precision = 1
max_s = 2500
number_of_bins = int(max_s/precision + 1)
likelihood_list_x = np.array([])
likelihood_list_y = np.array([])

# Fill likelihood plot data
for i, s in enumerate(np.linspace(0, max_s, number_of_bins)):
    next_likelihood = log_likelihood(n, bins, s)
    if next_likelihood < 0:
        # break
        pass
    likelihood_list_x = np.append(likelihood_list_x, s)
    likelihood_list_y = np.append(likelihood_list_y, next_likelihood)

# taking negative values: 918.0: 45412.155666197774
# ignori negative values: 918.0: 45412.155666197774 (max 45220ish)

# Find max bin
max_bin = np.where(likelihood_list_y == max(likelihood_list_y))[0][0]
print(f"Max bin: {max_bin}:\n{likelihood_list_x[max_bin]}: {likelihood_list_y[max_bin]}")

# Plot likelihood
fig2, ax2 = plt.subplots()
fig2: Figure
ax2: Axes
ax2.plot(likelihood_list_x, likelihood_list_y)
ax2.set_title("Posterior PDF from likelihood fit with 68.27% window")
ax2.set_xlabel("s estimator")
ax2.set_ylabel("Probability")

plt.show()
