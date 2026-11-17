import sys

from line import linear_regression
from utils import load_data, save_thetas


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data.csv"

    data = load_data(path)
    theta0, theta1 = linear_regression(data)
    save_thetas(theta0, theta1)
    print(f"theta0 = {theta0:.2f}   theta1 = {theta1:.5f}   saved to thetas.csv")


if __name__ == "__main__":
    try:
        main()
    except (ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
