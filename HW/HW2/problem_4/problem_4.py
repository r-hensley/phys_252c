import matplotlib.pyplot as plt
import numpy as np

# 4. Using the data set resonance.dat provided on the course web site, in which there are
# background  events  with  a  flat  distribution  (approximately  10  events/GeV  -  use  data  to
# estimate this), and a resonance with a mass of 700 GeV with a Gaussian sigma (width)
# of 50 GeV, make a measurement of the cross section for the resonance assuming that
# the integrated luminosity of the sample is 1 fb-1. Do this using a simple “mass window”
# method, in which you place cuts around the mass peak and simply count the number of
# events  in  the  window,  subtracting  the  expected  background.      Find  the  optimum  width
# for the mass window first by calculating the expected error on the measured cross sec-
# tion as a function of the width of the mass window, and assuming there are about 1000
# signal events expected.  Assume that your estimate of the expected background has no
# error, but remember that the expected number of events in the cut window (Nobs) will be
# the sum of the background and signal, and will be Poisson-distributed.

ROOT2PI = 2.50662827463
MU = 700
SIGMA = 50


def gint(mu, sigma, xlow, xhigh):
    precision = 100
    dx = (xhigh - xlow) / precision

    sum = 0
    for i in range(precision):
        x = xlow + dx*i + dx/2
        sum += np.exp(-(x-mu)**2 / (2 * sigma**2))

    return sum * dx / (sigma * ROOT2PI)


def find_bin(_bins, _x):
    for bin_number, bin_cutoff in enumerate(_bins):
        if _x < bin_cutoff:
            return bin_number, bin_cutoff


luminosity = 1

with open("./Data/resonance.dat", "r") as f:
    data = f.read().replace(' ', '').splitlines()

data = [float(i) for i in data]
print(min(data), max(data))
fig, ax = plt.subplots()

n, bins, patches = ax.hist(data, 36, (100, 1000), label="Resonance data")
bin_width = bins[1] - bins[0]
max_bin = np.where(n == max(n))[0][0]
max_bin = find_bin(bins, MU)[0]
print(f"{max_bin=}")
print(f"{n[max_bin]=}, {bins[max_bin]=}")
print(f"{bin_width=}")
ax.axvline(MU, color="#000000")

# Estimate background using first 40% of bins
x = bins[int(len(n)*4/10)] - bins[0]
background = sum(n[0:int(len(n)*4/10)]) / x
# background = 10
print(f"{background=}")

print(f"{find_bin(bins, MU)=}")

cut_results = []

# Consider all possible mass windows across the entire spectrum
# for peak_bin in [max_bin]:  range(0, len(bins))
for peak_bin in [max_bin]:  # len(bins) = 101, range is 0 --> 100
    for lower_cut in range(peak_bin + 1):  # ranges from 0 --> 100
        for upper_cut in range(peak_bin, len(bins)):  # ranges from 0 --> 100
            if lower_cut == upper_cut == peak_bin:
                continue
            efficiency = gint(MU, SIGMA, bins[lower_cut], bins[upper_cut]) / 1
            x = bins[upper_cut] - bins[lower_cut]  # width of mass window
            n_obs = sum(n[lower_cut:upper_cut])  # number of events in that window
            estimator = (n_obs - background * x) / (luminosity * efficiency)
            if not estimator > 0:
                continue
            variance_square = (estimator * efficiency + background * x) / (luminosity * efficiency)**2
            variance = np.sqrt(variance_square)
            if variance == 0:
                continue
            cut_results.append((peak_bin, lower_cut, upper_cut, estimator, variance))

cut_results.sort(key=lambda i: i[4], reverse=False)
print(cut_results[0:10], sep="\n")

ax.set_title("Fitting resonance data by minimizing error")
ax.set_xlabel("Mass (GeV)")
ax.set_ylabel("Events per 25 GeV")

# Plot the fit
x = np.linspace(100, 1000, 37)  # 100, 125, 150, ..., 950, 975, 1000
y = np.zeros(37)

for i, x_i in enumerate(n):
    y[i] = 10*bin_width + cut_results[0][3]*gint(MU, SIGMA, bins[i], bins[i+1])
ax.plot(x, y, "r+", label="Minimized error fit")
ax.legend()

# variable peak location, dynamic background counting 10.077 / GeV:
# [(55, 55, 75, 900.2081499972741, 56.11166095491515), (55, 55, 76, 921.5834837734922, 56.21871004606231),
# (55, 55, 77, 936.7760835271105, 56.5068719827808), (55, 55, 74, 905.4459755743469, 56.57402476686067),
# (55, 54, 75, 901.7202524627356, 56.737747467759625), (55, 54, 76, 922.9143689338258, 56.807305433681904),
# (55, 55, 78, 938.0386254629182, 56.85290115501761), (55, 54, 77, 937.9822151148103, 57.06450333830345),
# (55, 54, 74, 906.9644396003491, 57.237623176273466)]
#
#
# Variable peak location, set 10 background events / GeV
# [(58, 58, 75, 907.5016321092223, 55.156770831209144), (59, 58, 75, 907.5016321092223, 55.156770831209144),
# (60, 58, 75, 907.5016321092223, 55.156770831209144), (61, 58, 75, 907.5016321092223, 55.156770831209144),
# (62, 58, 75, 907.5016321092223, 55.156770831209144), (63, 58, 75, 907.5016321092223, 55.156770831209144),
# (64, 58, 75, 907.5016321092223, 55.156770831209144), (65, 58, 75, 907.5016321092223, 55.156770831209144),
# (66, 58, 75, 907.5016321092223, 55.156770831209144), (67, 58, 75, 907.5016321092223, 55.156770831209144)]
#
#
# Set dynamic peak location (680), variable background
# [(65, 58, 75, 893.8833856753009, 55.156770831209144), (65, 57, 75, 891.4257456085787, 55.22349990629425),
# (65, 58, 76, 916.3942740441902, 55.37919521911017), (65, 57, 76, 913.5364706278463, 55.40914549738576),
# (65, 59, 75, 901.5632200376291, 55.432398514904), (65, 56, 75, 882.8862225088003, 55.45443296979653),
# (65, 58, 74, 899.1798048486354, 55.52598646963874), (65, 56, 76, 904.8622967093777, 55.60645818742867),
# (65, 57, 74, 896.5335587037811, 55.6167469174911), (65, 59, 76, 924.5263154302062, 55.68948722961617)]
#
#
# Forcing peak to 700, variable background
# [(67, 58, 75, 893.8833856753009, 55.156770831209144), (67, 57, 75, 891.4257456085787, 55.22349990629425),
# (67, 58, 76, 916.3942740441902, 55.37919521911017), (67, 57, 76, 913.5364706278463, 55.40914549738576),
# (67, 59, 75, 901.5632200376291, 55.432398514904), (67, 56, 75, 882.8862225088003, 55.45443296979653),
# (67, 58, 74, 899.1798048486354, 55.52598646963874), (67, 56, 76, 904.8622967093777, 55.60645818742867),
# (67, 57, 74, 896.5335587037811, 55.6167469174911), (67, 59, 76, 924.5263154302062, 55.68948722961617)]

ideal_low_bin = cut_results[0][1]
ideal_high_bin = cut_results[0][2]
ideal_low_mass = bins[ideal_low_bin]
ideal_high_mass = bins[ideal_high_bin]
ax.axvline(ideal_low_mass, color="#FF0000")
ax.axvline(ideal_high_mass, color="#FF0000")

print(f"Ideal cutoffs are from {ideal_low_mass} (bin {ideal_low_bin}) to {ideal_high_mass} (bin {ideal_high_bin})")
# Ideal cutoffs are from 625.0 (bin 21) to 775.0 (bin 27)

print(f"The estimator here is {cut_results[0][3]} and sigma is {cut_results[0][4]}")
# The estimator here is 883.1287030866033 and sigma is 55.160668614936334

plt.show()
