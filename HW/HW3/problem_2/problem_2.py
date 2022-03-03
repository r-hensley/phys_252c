import math

import matplotlib.pyplot as plt
import numpy as np

# 2. Using the no-signal data sample posted on the web page, determine a 95% CL upper
# limit  on  the  cross  section  for  a  700  GeV  resonance  with  width  of  50  GeV,  using  a)  the
# window counting method and the Helene formula from HW 2, and b) a Bayesian method
# (using  the  binned  likelihood  from  problem  1).    I  forget  whether  the  background  is  the
# same or not here.  ;)

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


def logstir(n):
    factorial = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 36288]

    if n < 10:
        logfact = np.log(factorial[n])
    else:
        logfact = np.log(ROOT2PI) + 0.5*np.log(n) + n*np.log(n) - n + np.log(1+1/12/n+1/288/n**2)

    return logfact


def find_bin(_bins, _x):
    for bin_number, bin_cutoff in enumerate(_bins):
        if _x <= bin_cutoff:
            return bin_number, bin_cutoff


luminosity = 1

# with open("../Data/resonance.dat", "r") as f:
with open("../../Data/resonance-nosig.dat", "r") as f:
    data = f.read().replace(' ', '').splitlines()

data = [float(i) for i in data]
print(min(data), max(data))

fig, ax = plt.subplots()

n, bins, patches = ax.hist(data, 36, (100, 1000), label="Resonance data")
bin_width = bins[1] - bins[0]
# print(f"{max(n)=}")
# max_bin = np.where(n == max(n))[0][0]
# print(f"{max_bin=}")
max_bin = find_bin(bins, MU)[0]
print(f"{max_bin=}")
print(f"{n[max_bin]=}, {bins[max_bin]=}")
print(f"{bin_width=}")

lower_window = find_bin(bins, 625)[0]
upper_window = find_bin(bins, 775)[0]
print(f"{lower_window=}, {upper_window=}")

# Estimate background using first 40% of bins
x = bins[int(len(n)*4/10)] - bins[0]
background = sum(n[0:int(len(n)*4/10)]) / x
# background=10.125714285714286
print(f"{background=}")

print(f"{find_bin(bins, MU)=}")

cut_results = []

# Consider all possible mass windows across the entire spectrum
# for peak_bin in [max_bin]:  range(0, len(bins))
for peak_bin in [max_bin]:  # len(bins) = 101, range is 0 --> 100
    # for lower_cut in [lower_window]:
    for lower_cut in range(peak_bin + 1):  # ranges from 0 --> 100
        # for upper_cut in [upper_window]:
        for upper_cut in range(peak_bin, len(bins)):  # ranges from 0 --> 100
            if lower_cut == upper_cut == peak_bin:
                continue
            efficiency = gint(MU, SIGMA, bins[lower_cut], bins[upper_cut]) / 1
            x = bins[upper_cut] - bins[lower_cut]  # width of mass window
            n_obs = sum(n[lower_cut:upper_cut])  # number of events in that window
            estimator = (n_obs - background * x) / (luminosity * efficiency)
            print(f"{n_obs=}, {background*x=}, {estimator=}")
            if not estimator > 0:
                # continue
                pass  # Using window from last homework, I get a negative estimator (-96.788)
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
max_bin = cut_results[0][0]
ax.axvline(bins[max_bin], color="#000000")

# Plot the fit
x = np.linspace(100, 1000, 37)  # 100, 125, 150, ..., 950, 975, 1000
y = np.zeros(37)

for i, x_i in enumerate(n):
    y[i] = 10*bin_width + cut_results[0][3]*gint(MU, SIGMA, bins[i], bins[i+1])
ax.plot(x, y, "r+", label="Minimized error fit")
ax.legend()

ideal_low_bin = cut_results[0][1]
ideal_high_bin = cut_results[0][2]
ideal_low_mass = bins[ideal_low_bin]
ideal_high_mass = bins[ideal_high_bin]
ax.axvline(ideal_low_mass, color="#FF0000")
ax.axvline(ideal_high_mass, color="#FF0000")

print(f"Ideal cutoffs are from {ideal_low_mass} (bin {ideal_low_bin}) to {ideal_high_mass} (bin {ideal_high_bin})")
# Ideal cutoffs are from 625.0 (bin 21) to 775.0 (bin 27)

print(f"The estimator here is {cut_results[0][3]} and sigma is {cut_results[0][4]}")
# The estimator here is -96.78800386703442 and sigma is 43.72274524860117

# expected_events = cut_results[0][3] * gint(MU, SIGMA, 625, 775)
expected_background = background * (775 - 625)
# total_expected = expected_background + expected_events
total_observed = int(sum(n[21:27]))
# print(f"{expected_events=}")
print(f"{expected_background=}")
# print(f"{total_expected=}")
print(f"{total_observed=}")

# [(24, 23, 29, 0.20847112903551113, 56.87518802323297), (24, 23, 30, 7.24509340517004, 61.082625845655144), (24, 23, 31, 8.473363572684633, 65.1966057804159), (24, 24, 28, 17.660643217157975, 66.95228697540132), (24, 24, 29, 37.03124736432202, 72.56695891378263), (24, 24, 30, 46.41096816268778, 78.74914377902306), (24, 24, 31, 48.02232781124245, 84.79790688816014), (24, 24, 32, 35.71654554121121, 90.404835057835), (24, 24, 33, 3.4285946854855043, 95.4993388835851)]
# Ideal cutoffs are from 675.0 (bin 23) to 825.0 (bin 29)
# The estimator here is 0.20847112903551113 and sigma is 56.87518802323297
# expected_events=0.208471128839867
# expected_background=9113.142857142857
# total_expected=9113.351328271698
# total_observed=9010

# Using window from last homework:
# n_obs=1435.0, background*x=1518.857142857143, estimator=-96.78800386703442
# [(24, 21, 27, -96.78800386703442, 43.72274524860117), (24, 21, 26, -119.70100923502395, 44.21810853646901), (24, 22, 27, -77.09556527001547, 44.83578822817332), (24, 20, 27, -113.12986353633337, 44.871254012681), (24, 22, 26, -100.44188347570352, 45.00467685975994), (24, 21, 28, -59.31080224234952, 45.525174411666946), (24, 20, 26, -136.643153617521, 45.82170060071054), (24, 20, 28, -76.62836474847535, 46.28684116894763), (24, 22, 28, -36.47307676380832, 47.13803814124568), (24, 19, 27, -78.90284307248014, 47.66072429004762)]
# Ideal cutoffs are from 625.0 (bin 21) to 775.0 (bin 27)
# The estimator here is -96.78800386703442 and sigma is 43.72274524860117
# expected_background=1518.857142857143
# total_observed=1435

ratio = 1
expected_events = 0
while ratio > 0.05 and expected_events < 10000:
    total_expected = expected_background + expected_events
    numerator = 0
    denominator = 0
    for i in range(total_observed + 1):
        numerator_addition = i*np.log(total_expected) - total_expected - logstir(i)
        numerator_addition = np.exp(numerator_addition)
        numerator += numerator_addition

        denominator_addition = i * np.log(expected_background) - expected_background - logstir(i)
        denominator_addition = np.exp(denominator_addition)
        denominator += denominator_addition
    ratio = round(numerator / denominator, 5)
    print(f"{expected_events=}: {numerator=}/{denominator=} = {ratio=}")
    expected_events += 1

# expected_events=1: numerator=0.13875115302771854/denominator=0.14107724324797827 = ratio=0.98351
# expected_events=2: numerator=0.13645149038745277/denominator=0.14107724324797827 = ratio=0.96721
# expected_events=3: numerator=0.1341782016280386/denominator=0.14107724324797827 = ratio=0.9511
# expected_events=4: numerator=0.13193122793251652/denominator=0.14107724324797827 = ratio=0.93517
# expected_events=5: numerator=0.12971050543319604/denominator=0.14107724324797827 = ratio=0.91943
# expected_events=132: numerator=0.007162003251685104/denominator=0.14107724324797827 = ratio=0.05077
# expected_events=133: numerator=0.006958680522552051/denominator=0.14107724324797827 = ratio=0.04933

# Using window from last homework (22 - 27)
# expected_events=130: numerator=0.007584473971751966/denominator=0.14107724324797827 = ratio=0.05376
# expected_events=131: numerator=0.007370563611455755/denominator=0.14107724324797827 = ratio=0.05224
# expected_events=132: numerator=0.007162003251685104/denominator=0.14107724324797827 = ratio=0.05077
# expected_events=133: numerator=0.006958680522552051/denominator=0.14107724324797827 = ratio=0.04933


# Obs / back = (1500, 1500) --> exp. events < 78

# Obs / back = (1206, 1518) --> exp. events < 15
# expected_events=15: numerator=1.95341493771351e-18/denominator=4.716756711383502e-17 = ratio=0.04141

# Obs / back = (1435, 1518) --> exp. events < 41
# expected_events=41: numerator=0.0007170667907593477/denominator=0.015597420758386849 = ratio=0.04597


plt.show()
