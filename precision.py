import math
import sys

from utils import estimate_price, load_data, load_thetas


def r_squared(data, theta0, theta1):
    mean_price = sum(data.prices) / len(data.prices)

    line_errors = mean_errors = 0
    for mileage, price in zip(data.mileages, data.prices):
        estimate = estimate_price(mileage, theta0, theta1)
        line_errors += (estimate - price) ** 2
        mean_errors += (mean_price - price) ** 2

    if mean_errors == 0:
        return 1.0 if line_errors == 0 else 0.0
    return 1 - line_errors / mean_errors

def main():
    data = load_data(sys.argv[1] if len(sys.argv) > 1 else "data.csv")
    theta0, theta1, trained = load_thetas()
    if not trained:
        print("Model not trained yet (run train.py): theta0 = theta1 = 0.")
    print(f"R2   = {r_squared(data, theta0, theta1):.4f}")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt, OSError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)