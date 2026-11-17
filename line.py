from utils import estimate_price


def linear_regression(data, learning_rate=0.1, iterations=10000):
    """Gradient descent with the subject's formulas.

    Mileages (~10^5) are rescaled to [0, 1] first: with raw values the gradient
    on theta1 is ~10^10 times bigger than on theta0 and the descent overflows.
    The thetas found on the rescaled axis are converted back at the end, so the
    saved thetas work directly with raw mileages in estimatePrice.
    """
    m = len(data.mileages)
    if m == 0:
        raise ValueError("no data to train on")

    min_mileage = min(data.mileages)
    mileage_range = max(data.mileages) - min_mileage
    if mileage_range == 0:
        raise ValueError("all mileages are identical, the slope can't be learned")
    normalized = [(mileage - min_mileage) / mileage_range for mileage in data.mileages]

    theta0 = theta1 = 0.0
    for _ in range(iterations):
        sum0 = sum1 = 0.0
        for i in range(m):
            error = estimate_price(normalized[i], theta0, theta1) - data.prices[i]
            sum0 += error * 1
            sum1 += error * normalized[i]
        tmp_theta0 = learning_rate * sum0 / m
        tmp_theta1 = learning_rate * sum1 / m
        theta0 -= tmp_theta0
        theta1 -= tmp_theta1

    theta1 = theta1 / mileage_range
    theta0 = theta0 - theta1 * min_mileage
    return theta0, theta1
