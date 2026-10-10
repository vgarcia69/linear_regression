import matplotlib.pyplot as plt
import numpy as np
import csv

from dataclasses import dataclass

@dataclass
class Data:
	kms: list[float]
	prices: list[float]


def estimateNextPrice(km, theta0, theta1):
	return theta0 + theta1 * km

def load_data(path):
    kms, prices = [], []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            kms.append(float(row["km"]))
            prices.append(float(row["price"]))
    return kms, prices

def premier_dernier():
    x = [data.kms[iMinPrice], data.kms[iMaxPrice]]
    y = [data.prices[iMinPrice], data.prices[iMaxPrice]]
    return x, y 

def methode_mayar():
    sorted_datas = sorted(zip(data.kms, data.prices))
    m = len(sorted_datas)

    g1x = 0
    g1y = 0
    halfm = int(m/2)
    for i in range(halfm):
        g1x += sorted_datas[i][0]
        g1y += sorted_datas[i][1]
    g1x /= halfm
    g1y /= halfm

    g2x = 0
    g2y = 0
    for i in range(halfm):
        g2x += sorted_datas[i + halfm][0]
        g2y += sorted_datas[i + halfm][1]
    g2x /= halfm
    g2y /= halfm
    return [g1x, g2x], [g1y, g2y]

def regression_lineaire():
    theta0 = theta1 = 0
    learning_rate = 0.01
    m = len(data.kms)
    for j in range(1000): # 1000 peut etre changer par un check de si tmp0/tmp1 a changer ou non
        somme0 = somme1 = 0
        for i in range(m):
            somme_erreur_prix = estimateNextPrice(data.kms[i], theta0, theta1) - data.prices[i]
            somme0 += somme_erreur_prix
            somme1 += somme_erreur_prix * data.kms[i]
        tmp0 = learning_rate * somme0 / m
        tmp1 = learning_rate * somme1 / m
        theta0 -= tmp0
        theta1 -= tmp1
    return theta0, theta1

def change_en_droite(xs, ys):
    theta1 = (ys[1] - ys[0]) / (xs[1] - xs[0])
    theta0 = ys[0] - theta1 * xs[0]
    return theta0, theta1

def trace_droite(theta0, theta1, color):
    x = [min(data.kms), max(data.kms)]
    y = [estimateNextPrice(x[0], theta0, theta1), estimateNextPrice(x[1], theta0, theta1)]
    plt.plot(x, y, color=color)



data = Data
data.kms, data.prices = load_data("data.csv");	

iMaxPrice = data.prices.index(max(data.prices))
iMinPrice = data.prices.index(min(data.prices))



# theta0, theta1 = change_en_droite(premier_dernier()[0], premier_dernier()[1])
# trace_droite(theta0, theta1, color="red")

# theta0, theta1 = change_en_droite(methode_mayar()[0], methode_mayar()[1])
# trace_droite(theta0, theta1, color="blue") 

theta0, theta1 = regression_lineaire()
print("theta0:",theta0, "\ntheta1:", theta1)
trace_droite(theta0, theta1, color="green")

plt.scatter(data.kms, data.prices)

plt.title("this is a title")

plt.xlabel("kms")
plt.ylabel("price")

plt.show()