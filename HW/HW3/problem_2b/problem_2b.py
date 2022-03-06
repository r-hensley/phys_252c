import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

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


def calc_log_likelihood(_n, _bins, _s):
    log_likelihood_sum = 0
    for bin_number, bin_value in enumerate(_n):
        mu = 251.188 + _s * gint(MU, SIGMA, _bins[bin_number], _bins[bin_number+1])
        log_likelihood_sum += bin_value * np.log(mu) - mu
    return log_likelihood_sum


def integrate_likelihood(_x, _y, _low_x, _high_x):
    dx = _x[1] - _x[0]
    int_sum = 0
    for i, y in enumerate(_y):
        if not _low_x <= _x[i] <= _high_x:
            continue
        int_sum += dx * y
    return int_sum


def find_bound(_x, _y):  # 15.865
    dx = _x[1] - _x[0]
    int_sum = 0
    for i, y in enumerate(_y):
        int_sum += dx * y
        if int_sum > 0.95:
            return _x[i]


with open("../../Data/resonance-nosig.dat", "r") as f:
    data = f.read().replace(' ', '').splitlines()

data = [float(i) for i in data]
fig, ax = plt.subplots()

n, bins, patches = ax.hist(data, 36, (100, 1000), label="Resonance data")

precision = 0.1  # Iterate over values of s to max_s with precision
max_s = 100
number_of_bins = int(max_s/precision + 1)  # Include "0" so +1 bin necessary (example, max_s=precision=1 gives [0, 1])
s_values = np.linspace(0, max_s, number_of_bins)  # [0.0, 0.1, 0.2, ..., 99.8, 99.9, 100.0]
log_likelihood_list_y = np.array([])

base_likelihood = calc_log_likelihood(n, bins, 0)  # Will subtract the s=0 likelihood as an offset
for i, s in enumerate(s_values):
    log_likelihood = calc_log_likelihood(n, bins, s)
    log_likelihood_list_y = np.append(log_likelihood_list_y, log_likelihood)

# Subtract value of likelihood at end from rest of values to make likelihood normalizable
base_likelihood = log_likelihood_list_y[-1]
log_likelihood_list_y = log_likelihood_list_y - base_likelihood

# Exponentiate and normalize
likelihood_list_y = np.exp(log_likelihood_list_y)
likelihood_magnitude = integrate_likelihood(s_values, likelihood_list_y, 0, s_values[-1])
likelihood_list_y = likelihood_list_y / likelihood_magnitude

# Find lower and upper bounds of 95% confidence interval
upper_bound = find_bound(s_values, likelihood_list_y)  # Upper bound of 95% interval (x-value)

# Plot posterior PDF
fig2, ax2 = plt.subplots()
fig2: Figure  # Typehinting
ax2: Axes  # Typehinting
ax2.plot(s_values, likelihood_list_y)
ax2.set_title("Posterior PDF from likelihood fit with 95% window")
ax2.set_xlabel("s estimator")
ax2.set_ylabel("Probability")
plt.xlim(left=0)
plt.ylim(bottom=0)

# Fill in 95% confidence range
ax2.fill_between(s_values,
                 likelihood_list_y,
                 where=s_values < upper_bound,
                 alpha=0.5)

ax2.text(0.60, 0.95, rf"Estimator: $s < {upper_bound}$",
         transform=ax2.transAxes, fontsize=12, verticalalignment="top")

# Print and plot results
print(f"{max_s=} ({precision=})  -->  {upper_bound=}")
plt.show()


# #############################################
# ################## RESULTS ##################
# max_s=1000 (precision=5)  -->  upper_bound=50.0
# max_s=500 (precision=5)  -->  upper_bound=50.0
# max_s=500 (precision=1)  -->  upper_bound=49.0
# max_s=100 (precision=0.1)  -->  upper_bound=49.6
# #############################################
# #############################################



