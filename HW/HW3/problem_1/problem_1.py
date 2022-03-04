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


def log_likelihood(_n, _bins, _s):
    # print(f"{_s=}")
    log_likelihood_sum = 0
    for bin_number, bin_value in enumerate(_n):
        # print(f"{_bins[bin_number]=}")
        # print(f"{_bins[bin_number+1]=}")
        # print(f"{bin_number=}")
        # print(f"{bin_value=}")
        mu = 251.188 + _s * gint(MU, SIGMA, _bins[bin_number], _bins[bin_number+1])
        # print(f"{mu=}")
        # print("")
        log_likelihood_sum += mu - bin_value * np.log(mu)
    return 2*log_likelihood_sum


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
        print(int_sum)
        if int_sum < -0.15865:
            return _x[i]


with open("../../Data/resonance.dat", "r") as f:
    data = f.read().replace(' ', '').splitlines()

data = [float(i) for i in data]
fig, ax = plt.subplots()

n, bins, patches = ax.hist(data, 36, (100, 1000), label="Resonance data")

precision = 5
max_s = 2500
number_of_bins = int(max_s/precision + 1)
likelihood_list_x = np.array([])
likelihood_list_y = np.array([])
base_likelihood = 0
for i, s in enumerate(np.linspace(0, max_s, number_of_bins)):
    next_likelihood = log_likelihood(n, bins, s)
    if s == 0:
        base_likelihood = next_likelihood
    print(f"{s=}, {base_likelihood=}, {next_likelihood=}")
    if next_likelihood - base_likelihood > 0:
        break
    likelihood_list_x = np.append(likelihood_list_x, s)
    likelihood_list_y = np.append(likelihood_list_y, next_likelihood - base_likelihood)

likelihood_list_y = np.exp(likelihood_list_y)
likelihood_magnitude = integrate_likelihood(likelihood_list_x, likelihood_list_y, 0, likelihood_list_x[-1])
likelihood_list_y = likelihood_list_y / likelihood_magnitude
lower_bound = find_bound(likelihood_list_x, likelihood_list_y, backwards=False)
upper_bound = find_bound(likelihood_list_x, likelihood_list_y, backwards=True)
print(f"{lower_bound=} --- {upper_bound=}")
# print(f"{likelihood_list_x=}")
# print(f"{likelihood_list_y=}")

# print(f"{max(likelihood_list[1])=}")
max_bin = np.where(likelihood_list_y == min(likelihood_list_y))[0][0]
print(f"{max_bin=}")


print("Likelihoods")
for i, j in enumerate(likelihood_list_x):
    # print(f"{likelihood_list_x[i]}: {likelihood_list_y[i]}")
    pass

print(f"Bin {max_bin}:\n{likelihood_list_x[max_bin]}: {likelihood_list_y[max_bin]}")


fig2, ax2 = plt.subplots()
fig2: Figure
ax2: Axes
ax2.plot(likelihood_list_x, likelihood_list_y)
ax2.set_title("Posterior PDF from likelihood fit with 68.27% window")
ax2.set_xlabel("s estimator")
ax2.set_ylabel("Probability")
ax2.fill_between(likelihood_list_x,
                 likelihood_list_y,
                 where=(lower_bound < likelihood_list_x) & (likelihood_list_x < upper_bound),
                 alpha=0.5)
# plt.xlim(686, 1150)
plt.xlim(0, 2000)
ax2.text(0.05, 0.95, f"Lower bound: {lower_bound}\nUpper bound: {upper_bound}",
         transform=ax2.transAxes, fontsize=12, verticalalignment="top")
# Lower bound: 866, Upper bound: 972.7

max_s = likelihood_list_x[max_bin]

ax2.text(0.60, 0.95, rf"Estimator: ${max_s}^{{+{round(upper_bound-max_s, 1)}}}_{{-{round(max_s-lower_bound, 1)}}}$",
         transform=ax2.transAxes, fontsize=12, verticalalignment="top")
# 918.2 + 54.5 - 52.2
bottom, _ = plt.ylim()
top = 0
plt.ylim(top=top)
y_percentage = (likelihood_list_y[max_bin] - top) / (top - bottom)
ax2.axvline(max_s, 1-y_percentage, 1, color="#FF0000")


# lower_bound=866.0 --- upper_bound=972.7
# max_bin=9182
# Likelihoods
# Bin 9182:
# 918.2: 0.007474625108787476

plt.show()
