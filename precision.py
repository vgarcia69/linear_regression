"""Bonus: measure how good the trained thetas are on the dataset."""
import math
import sys

from utils import estimate_price, load_data, load_thetas


def r_squared(data, theta0, theta1):
    """Share of the price variation explained by the line (1 = perfect)."""
    mean_price = sum(data.prices) / len(data.prices)

    line_errors = mean_errors = 0
    for mileage, price in zip(data.mileages, data.prices):
        estimate = estimate_price(mileage, theta0, theta1)
        line_errors += (estimate - price) ** 2
        mean_errors += (mean_price - price) ** 2

    if mean_errors == 0:
        return 1.0 if line_errors == 0 else 0.0
    return 1 - line_errors / mean_errors


def mae(data, theta0, theta1):
    """Mean absolute error: average gap between prediction and real price."""
    return sum(abs(estimate_price(x, theta0, theta1) - y)
               for x, y in zip(data.mileages, data.prices)) / len(data.prices)


def rmse(data, theta0, theta1):
    """Root mean squared error: like MAE but punishes big errors more."""
    return math.sqrt(sum((estimate_price(x, theta0, theta1) - y) ** 2
                         for x, y in zip(data.mileages, data.prices)) / len(data.prices))


def main():
    try:
        data = load_data(sys.argv[1] if len(sys.argv) > 1 else "data.csv")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    theta0, theta1, trained = load_thetas()
    if not trained:
        print("Model not trained yet (run train.py): theta0 = theta1 = 0.")
    print(f"R2   = {r_squared(data, theta0, theta1):.4f}")
    print(f"MAE  = {mae(data, theta0, theta1):.2f}")
    print(f"RMSE = {rmse(data, theta0, theta1):.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
