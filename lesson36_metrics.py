import math
import unittest

def calculate_errors(actual, predicted):
    actual = [float(value) for value in actual]
    predicted = [float(value) for value in predicted]

    if not actual or len(actual) != len(predicted):
        raise ValueError("Inputs must be non-empty and equal in length")

    if not all(math.isfinite(value) for value in actual + predicted):
        raise ValueError("Prices must be finite numbers")

    #POSITIVE: PREDICTED TOO LOW
    #NEGATIVE: PREDICTED TOO HIGH

    signed_error = [
          real - estimate
        for real, estimate in zip(actual, predicted)

    ]
    absolute_error = [abs(error) for error in signed_error]
    mae = sum(absolute_error) / len(absolute_error)

    return signed_error, absolute_error, mae

class TestPriceErrors(unittest.TestCase):
    def test_mixed_errors(self):
        signed, absolute, mae = calculate_errors(
            [10000,20000,30000],
            [8000,23000,30000]
        )

        self.assertEqual(signed,[2000,-3000,0])
        self.assertEqual(absolute,[2000,3000,0])

    def test_perfect_predictions(self):
        _,_, mae = calculate_errors(
            [10000,20000],
            [10000,20000]
        )
        self.assertEqual(mae,0)

    def test_empty_inputs(self):
        with self.assertRaises(ValueError):
            calculate_errors([],[])

    def test_different_lengths(self):
        with self.assertRaises(ValueError):
            calculate_errors([10000, 20000], [9000])

    def test_infinite_price(self):
        with self.assertRaises(ValueError):
            calculate_errors([10000], [float("inf")])


if __name__ == "__main__":
    unittest.main()

