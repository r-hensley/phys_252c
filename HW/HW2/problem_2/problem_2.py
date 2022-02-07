import numpy as np
import random
import matplotlib.pyplot as plt

# We  generate  pairs  of  correlated  gaussian  random  numbers  by  first  generating  two
# normal  deviates, ξ1  and  ξ2,  and  then  putting  out  the  pair  (ξ1, ρξ1  + ξ2(1-ρ2)1/2).    Show
# that  the  resulting  two-dimensional  distribution  has  a  correlation  coefficient  of ρ,  again
# either analytically or numerically, or both.  (There is a straightforward numeric solution -
# review the definition of the covariance of two deviates.)


def calc_sigma(_mu, _data):
    return np.sqrt(sum([(i - _mu) ** 2 for i in _data]) / (len(_data) - 1))


def calc_covariance(_mu1, _data1, _mu2, _data2):
    covariance = 0
    for i, _ in enumerate(_data1):
        covariance += (_data1[i] - _mu1) * (_data2[i] - _mu2)
    covariance = covariance / (len(_data1) - 1)
    return covariance


def problem_2():
    sigma_data1 = np.array([])
    sigma_data2 = np.array([])
    covariance_data = np.array([])
    correlation_data = np.array([])
    p = -0.5
    mu = 0
    sigma = 1

    for _ in range(10000):
        data1 = np.array([])  # will hold all the variances for each distribution
        data2 = np.array([])

        for _ in range(50):
            r1 = random.gauss(mu, sigma)
            r2 = random.gauss(mu, sigma)
            data1 = np.append(data1, r1)
            data2 = np.append(data2, p*r1 + r2*(1-p**2)**(1/2))

        mu1 = sum(data1) / len(data1)
        mu2 = sum(data2) / len(data2)
        sigma1 = calc_sigma(mu1, data1)
        sigma2 = calc_sigma(mu2, data2)
        covariance = calc_covariance(mu1, data1, mu2, data2)
        correlation = covariance / (sigma1 * sigma2)

        sigma_data1 = np.append(sigma_data1, sigma1)
        sigma_data2 = np.append(sigma_data2, sigma2)
        covariance_data = np.append(covariance_data, covariance)
        correlation_data = np.append(correlation_data, correlation)

    print(covariance_data[0:10])
    print(correlation_data[0:10])

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle(r"Correlation between $ξ_1$ and $\rho ξ_1 + ξ_2(1-\rho^2)^{1/2}$")

    ax1.hist(covariance_data) # , 30, (sigma - 0.5, sigma + 0.5))
    ax1.set_title("Covariance")
    # ax1.set_xlabel(f"")
    # ax1.axvline(sigma, color="#000000")

    ax2.hist(correlation_data)  # , 30, (sigma - 0.5, sigma + 0.5))
    ax2.set_title(rf"Correlation (expected $\rho = {p}$)")
    # ax2.set_xlabel(f"σ")
    ax2.axvline(p, color="#000000")

    fig2, ax3 = plt.subplots()
    ax3.scatter(data1, data2)
    ax3.set_title(rf"Example data (correlation $\rho = {round(correlation, 2)}$)")
    ax3.set_xlabel(r"$ξ_1$")
    ax3.set_ylabel(r"$\rho ξ_1 + ξ_2(1-\rho^2)^{1/2}$")

    plt.subplots_adjust(wspace=0.3)
    plt.show()

problem_2()


