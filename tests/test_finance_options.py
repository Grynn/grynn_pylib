import unittest
from grynn_pylib.finance import options
import numpy as np

class TestOptions(unittest.TestCase):

    def test_bs_d1_d2(self):
        # Sample inputs
        S = 100  # Stock price
        K = 100  # Strike price
        T = 1    # Time to maturity
        r = 0.05 # Risk-free rate
        sigma = 0.2 # Volatility

        # Expected outputs (calculated using a known implementation)
        expected_d1 = 0.35
        expected_d2 = 0.15

        # Call the function
        d1, d2 = options.bs_d1_d2(S, K, T, r, sigma)

        # Assert the results
        self.assertAlmostEqual(d1, expected_d1, places=2)
        self.assertAlmostEqual(d2, expected_d2, places=2)

    def test_bs_delta(self):
        # Sample inputs
        S = 100
        K = 100
        T = 1
        r = 0.05
        sigma = 0.2

        # Expected outputs
        expected_call_delta = 0.6368
        expected_put_delta = -0.3632

        # Call the function
        call_delta = options.bs_delta(S, K, T, r, sigma, option_type='call')
        put_delta = options.bs_delta(S, K, T, r, sigma, option_type='put')

        # Assert the results
        self.assertAlmostEqual(call_delta, expected_call_delta, places=4)
        self.assertAlmostEqual(put_delta, expected_put_delta, places=4)

    def test_bs_gamma(self):
        # Sample inputs
        S = 100
        K = 100
        T = 1
        r = 0.05
        sigma = 0.2

        # Expected output
        expected_gamma = 0.0188

        # Call the function
        gamma = options.bs_gamma(S, K, T, r, sigma)

        # Assert the result
        self.assertAlmostEqual(gamma, expected_gamma, places=4)

    def test_bs_theta(self):
        # Sample inputs
        S = 100
        K = 100
        T = 1
        r = 0.05
        sigma = 0.2

        # Expected outputs
        expected_call_theta = -0.0176
        expected_put_theta = -0.0045

        # Call the function
        call_theta = options.bs_theta(S, K, T, r, sigma, option_type='call')
        put_theta = options.bs_theta(S, K, T, r, sigma, option_type='put')

        # Assert the results
        self.assertAlmostEqual(call_theta, expected_call_theta, places=4)
        self.assertAlmostEqual(put_theta, expected_put_theta, places=4)

    def test_bs_omega(self):
        # Sample inputs
        S = 100
        K = 100
        T = 1
        r = 0.05
        sigma = 0.2
        option_price = 10.4506

        # Expected outputs
        expected_call_omega = 6.094
        expected_put_omega = -3.475

        # Call the function
        call_omega = options.bs_omega(S, K, T, r, sigma, option_price, option_type='call')
        put_omega = options.bs_omega(S, K, T, r, sigma, option_price, option_type='put')

        # Assert the results
        self.assertAlmostEqual(call_omega, expected_call_omega, places=3)
        self.assertAlmostEqual(put_omega, expected_put_omega, places=3)

    def test_bs_omega_short_put(self):
        # Sample inputs
        S = 100
        K = 100
        T = 1
        r = 0.05
        sigma = 0.2
        option_price = 10.4506

        # Expected output
        expected_omega_short_put = 3.475

        # Call the function
        omega_short_put = options.bs_omega_short_put(S, K, T, r, sigma, option_price)

        # Assert the result
        self.assertAlmostEqual(omega_short_put, expected_omega_short_put, places=3)

    def test_payoff_put(self):
        # Sample inputs
        S = 90
        K = 100
        premium = 5

        # Expected output
        expected_payoff = -0.0526

        # Call the function
        payoff = options.payoff_put(S, K, premium)

        # Assert the result
        self.assertAlmostEqual(payoff, expected_payoff, places=4)

        S=110
        expected_payoff=0.0526
        payoff=options.payoff_put(S,K,premium)
        self.assertAlmostEqual(payoff,expected_payoff,places=4)

if __name__ == "__main__":
    unittest.main()