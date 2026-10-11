from utils import line_from_points, estimate_price

def cheapest_and_priciest(data):
    """Line through the cheapest car and the most expensive one."""
    i_max_price = data.prices.index(max(data.prices))
    i_min_price = data.prices.index(min(data.prices))

    x = [data.mileages[i_min_price], data.mileages[i_max_price]]
    y = [data.prices[i_min_price], data.prices[i_max_price]]
    return line_from_points(x, y)


def mayer_method(data):
    """Line through the mean points of the two halves of the dataset."""
    points = sorted(zip(data.mileages, data.prices))
    m = len(points)
    half = m // 2

    g1x = g1y = 0
    for i in range(half):
        g1x += points[i][0]
        g1y += points[i][1]
    g1x /= half
    g1y /= half

    g2x = g2y = 0
    for i in range(half, m):
        g2x += points[i][0]
        g2y += points[i][1]
    g2x /= m - half
    g2y /= m - half

    return line_from_points([g1x, g2x], [g1y, g2y])


def linear_regression(data, learning_rate=0.1, iterations=10000):
    """Gradient descent on mileages normalized between 0 and 1."""
    m = len(data.mileages)

    min_mileage = min(data.mileages)
    max_mileage = max(data.mileages)
    mileage_range = max_mileage - min_mileage
    normalized = [(mileage - min_mileage) / mileage_range for mileage in data.mileages]

    theta0 = theta1 = 0
    for _ in range(iterations):
        sum0 = sum1 = 0
        for i in range(m):
            error = estimate_price(normalized[i], theta0, theta1) - data.prices[i]
            sum0 += error
            sum1 += error * normalized[i]
        tmp0 = learning_rate * sum0 / m
        tmp1 = learning_rate * sum1 / m
        theta0 -= tmp0
        theta1 -= tmp1

    theta1 = theta1 / mileage_range
    theta0 = theta0 - theta1 * min_mileage
    return theta0, theta1

