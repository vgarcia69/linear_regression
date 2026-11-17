import csv
import math
from dataclasses import dataclass

THETAS_PATH = "thetas.csv"


@dataclass
class Data:
    mileages: list[float]
    prices: list[float]


def load_data(path):
    mileages, prices = [], []
    try:
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None or not {"km", "price"} <= set(reader.fieldnames):
                raise ValueError(f"{path}: expected a header with 'km' and 'price'")
            for line, row in enumerate(reader, start=2):
                try:
                    mileage, price = float(row["km"]), float(row["price"])
                except (TypeError, ValueError):
                    raise ValueError(f"{path}:{line}: invalid row {row}")
                if not (math.isfinite(mileage) and math.isfinite(price)):
                    raise ValueError(f"{path}:{line}: non-finite value")
                mileages.append(mileage)
                prices.append(price)
    except OSError as e:
        raise ValueError(f"cannot read {path}: {e.strerror}")
    if not mileages:
        raise ValueError(f"{path}: no data")
    return Data(mileages, prices)


def estimate_price(mileage, theta0, theta1):
    return theta0 + theta1 * mileage


def load_thetas(path=THETAS_PATH):
    try:
        with open(path) as f:
            theta0, theta1 = (float(v) for v in f.read().strip().split(","))
    except ValueError:
        return 0.0, 0.0, False
    except OSError as e:
        raise OSError(f"cannot read {path}: {e.strerror}")
    if not (math.isfinite(theta0) and math.isfinite(theta1)):
        return 0.0, 0.0, False
    return theta0, theta1, True


def save_thetas(theta0, theta1, path=THETAS_PATH):
    try:
        with open(path, "w") as f:
            f.write(f"{theta0},{theta1}\n")
    except OSError as e:
        raise ValueError(f"cannot read {path}: {e.strerror}")


def plot_line(data, theta0, theta1, color, label):
    import matplotlib.pyplot as plt

    x = [min(data.mileages), max(data.mileages)]
    y = [estimate_price(mileage, theta0, theta1) for mileage in x]
    plt.plot(x, y, color=color, label=label)
