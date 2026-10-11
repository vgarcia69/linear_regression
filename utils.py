import csv
from dataclasses import dataclass

import matplotlib.pyplot as plt


@dataclass
class Data:
    mileages: list[float]
    prices: list[float]


def load_data(path):
    mileages, prices = [], []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mileages.append(float(row["km"]))
            prices.append(float(row["price"]))
    return Data(mileages, prices)


def estimate_price(mileage, theta0, theta1):
    return theta0 + theta1 * mileage


def line_from_points(xs, ys):
    """Turn two points (xs = [x1, x2], ys = [y1, y2]) into theta0, theta1."""
    theta1 = (ys[1] - ys[0]) / (xs[1] - xs[0])
    theta0 = ys[0] - theta1 * xs[0]
    return theta0, theta1


def plot_line(data, theta0, theta1, color, label):
    x = [min(data.mileages), max(data.mileages)]
    y = [estimate_price(mileage, theta0, theta1) for mileage in x]
    plt.plot(x, y, color=color, label=label)
