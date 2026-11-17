import math
import sys

from utils import estimate_price, load_data, load_thetas, plot_line


def ask_mileage():
    while True:
        raw = input("Mileage: ")
        try:
            mileage = float(raw)
        except ValueError:
            print("Please enter a number.")
            continue
        if not math.isfinite(mileage):
            print("Please enter a finite number.")
            continue
        if mileage < 0:
            print("Mileage can't be negative.")
            continue
        return mileage


def main():
    theta0, theta1, trained = load_thetas()
    if not trained:
        raise("Model not trained yet (run train.py): theta0 = theta1 = 0.")
    mileage = ask_mileage()
    price = estimate_price(mileage, theta0, theta1)
    print(f"Estimated price: {price:.2f}")
    if price < 0:
        print("Warning: this mileage is far outside the training data, "
              "the linear model is not meaningful here.")
    show_bonus(theta0, theta1, mileage, price)


def show_bonus(theta0, theta1, mileage, price):
    try:
        import matplotlib.pyplot as plt
        from precision import r_squared

        data = load_data("data.csv")
    except (ImportError, ValueError) as e:
        print(f"(graph skipped: {e})")
        return

    plt.scatter(data.mileages, data.prices, label="data")
    plot_line(data, theta0, theta1, "green", "linear regression")
    plt.scatter([mileage], [price], color="red", zorder=3, label="prediction")
    plt.title("Price as a function of mileage")
    plt.xlabel("mileage (km)")
    plt.ylabel("price")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
