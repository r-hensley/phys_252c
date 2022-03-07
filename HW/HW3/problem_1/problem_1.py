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
        mu = 10 * BIN_WIDTH + _s * gint(MU, SIGMA, _bins[bin_number], _bins[bin_number+1])
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


def find_bound(_x, _y, backwards=False):  # 15.865
    dx = _x[1] - _x[0]
    int_sum = 0
    if backwards:
        _x = np.flip(_x)
        _y = np.flip(_y)
    for i, y in enumerate(_y):
        int_sum += dx * y
        if int_sum > 0.15865:
            return _x[i]


with open("../../Data/resonance.dat", "r") as f:
    data = f.read().replace(' ', '').splitlines()

data = [float(i) for i in data]
fig, ax = plt.subplots()

n, bins, patches = ax.hist(data, (1000-100)/BIN_WIDTH, (100, 1000), label="Resonance data")

precision = 0.5
max_s = 2500
number_of_bins = int(max_s/precision + 1)
s_values = np.linspace(0, max_s, number_of_bins)  # [0, 0.5, 1.0, 1.5, ..., 2499.05, 2500]
log_likelihood_list_y = np.array([])

base_likelihood = calc_log_likelihood(n, bins, 0)  # Will subtract the s=0 likelihood as an offset
for i, s in enumerate(s_values):
    log_likelihood = calc_log_likelihood(n, bins, s) - base_likelihood
    if log_likelihood < 0:
        break  # Stop adding values to array when likelihood becomes negative
    log_likelihood_list_y = np.append(log_likelihood_list_y, log_likelihood)

# Cut off end of x-array to match size of y-array
s_values = s_values[0 : len(log_likelihood_list_y)]

# Exponentiate and normalize
likelihood_list_y = np.exp(log_likelihood_list_y)
likelihood_magnitude = integrate_likelihood(s_values, likelihood_list_y, 0, s_values[-1])
likelihood_list_y = likelihood_list_y / likelihood_magnitude

# Find lower and upper bounds of 67% confidence interval
lower_bound = find_bound(s_values, likelihood_list_y, backwards=False)  # Lower bound of 67% interval (x-value)
upper_bound = find_bound(s_values, likelihood_list_y, backwards=True)  # Upper bound of 67% interval (x-value)

max_bin = np.where(likelihood_list_y == max(likelihood_list_y))[0][0]  # Bin number of maximum bin
max_x = s_values[max_bin]  # X-value for maximum bin

# Plot posterior PDF
fig2, ax2 = plt.subplots()
fig2: Figure  # Typehinting
ax2: Axes  # Typehinting
ax2.plot(s_values, likelihood_list_y)
ax2.set_title("Posterior PDF from likelihood fit with 68.27% window")
ax2.set_xlabel("s estimator")
ax2.set_ylabel("Probability")
plt.xlim(686, 1150)  # Center view around peak

# Fill in 67% confidence range
ax2.fill_between(s_values,
                 likelihood_list_y,
                 where=(lower_bound < s_values) & (s_values < upper_bound),
                 alpha=0.5)

# Add text for bounds and estimator value
ax2.text(0.05, 0.95, f"Lower bound: {lower_bound}\nUpper bound: {upper_bound}",
         transform=ax2.transAxes, fontsize=12, verticalalignment="top")
ax2.text(0.60, 0.95, rf"Estimator: ${max_x}^{{+{round(upper_bound-max_x, 1)}}}_{{-{round(max_x-lower_bound, 1)}}}$",
         transform=ax2.transAxes, fontsize=12, verticalalignment="top")

# Add vertical line marking maximum
_, top = plt.ylim()
plt.ylim(bottom=0)
y_percentage = likelihood_list_y[max_bin] / top
ax2.axvline(max_x, 0, y_percentage, color="#FF0000")


# #############################################
# ################## RESULTS ##################
# Precision=0.5
# max_bin=1818
# Bin 1818:
# 909.0: 0.007478422884021669
# Lower bound: 857, Upper bound: 963.5
# Estimator: 909 + 54.5 - 52.0
# #############################################
# #############################################


plt.show()
