import matplotlib.pyplot as plt

from utils import load_data, plot_line
from line import cheapest_and_priciest, mayer_method, linear_regression
from precision import r_squared


def main():
    data = load_data("data.csv")

    methods = [
        ("cheapest/priciest", cheapest_and_priciest, "red"),
        ("mayer", mayer_method, "blue"),
        ("linear regression", linear_regression, "green"),
    ]

    plt.scatter(data.mileages, data.prices)
    for name, method, color in methods:
        theta0, theta1 = method(data)
        r2 = r_squared(data, theta0, theta1)
        print(f"{name:20} theta0 = {theta0:9.2f}   theta1 = {theta1:.5f}   R2 = {r2:.4f}")
        plot_line(data, theta0, theta1, color, name)

    plt.title("Price as a function of mileage")
    plt.xlabel("mileage (km)")
    plt.ylabel("price")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
