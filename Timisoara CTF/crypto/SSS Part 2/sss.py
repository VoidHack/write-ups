from os import urandom

class SSS:

    def __init__(self, N, T):
        self.T = T
        self.N = N
        self.coefficients = self.generate_poly_coefficients()

    # splits a secret into N parts so that at least T shares are needed to reconstruct the secret
    def split_secret(self, secret):
        shares = []

        for i in range(self.N):
            shares.append({"x":i+1, "y":self.compute_poly_value(i+1, secret, self.coefficients)})

        return shares

    # reconstruct secret given enough shares
    def join_shares(self, shares):
        return self.compute_lagrange_interpolating_polynomial(0, shares)

    # randomly pick T-1 coefficients where T-1 = the degree of the polynomial
    def generate_poly_coefficients(self):
        return [int(urandom(10).encode("hex"), 16) for _ in range(self.T-1)]

    # compute f(x), given the coefficients and the constant term (secret) of the polynomial
    def compute_poly_value(self, x, secret, coefficients):
        value = 0
        _x = x
        for c in coefficients:
            value += c*_x
            _x *= x

        return value + int(secret.encode("hex"), 16)

    # lagrange helper stuff
    def compute_lagrange_interpolating_polynomial(self, x, points):
        s = 0
        for i, point in enumerate(points):
            s = (s + point["y"] * self.lagrange_basis_polynomial(x, points, i))
        return s

    # more lagrange stuff
    def lagrange_basis_polynomial(self, x, points, i):
        numerator = 1
        denominator = 1
        for j, p in enumerate(points):
            if i == j:
                continue
            numerator *= (x - p["x"])
            denominator *= (points[i]["x"] - p["x"])
        return int(numerator/denominator)
