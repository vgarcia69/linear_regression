import csv
import math
from dataclasses import dataclass

THETAS_PATH = "thetas.csv"


@dataclass
class Data:
    mileages: list[float]
    prices: list[float]


def load_data(path):
    """Read the dataset. Raises ValueError with a clear message if it's unusable."""
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
    """The hypothesis from the subject: estimatePrice(mileage) = theta0 + theta1 * mileage."""
    return theta0 + theta1 * mileage


def load_thetas(path=THETAS_PATH):
    """Return (theta0, theta1, trained). Before training, both thetas are 0."""
    try:
        with open(path) as f:
            theta0, theta1 = (float(v) for v in f.read().strip().split(","))
    except (OSError, ValueError):
        return 0.0, 0.0, False
    if not (math.isfinite(theta0) and math.isfinite(theta1)):
        return 0.0, 0.0, False
    return theta0, theta1, True


def save_thetas(theta0, theta1, path=THETAS_PATH):
    with open(path, "w") as f:
        f.write(f"{theta0},{theta1}\n")


def plot_line(data, theta0, theta1, color, label):
    import matplotlib.pyplot as plt

    x = [min(data.mileages), max(data.mileages)]
    y = [estimate_price(mileage, theta0, theta1) for mileage in x]
    plt.plot(x, y, color=color, label=label)
