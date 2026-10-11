from utils import estimate_price

def r_squared(data, theta0, theta1):
    """Share of the price variation explained by the line (1 = perfect)."""
    mean_price = sum(data.prices) / len(data.prices)

    line_errors = mean_errors = 0
    for mileage, price in zip(data.mileages, data.prices):
        estimate = estimate_price(mileage, theta0, theta1)
        line_errors += (estimate - price) ** 2
        mean_errors += (mean_price - price) ** 2

    return 1 - line_errors / mean_errors

