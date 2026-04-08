import unittest

class SimpleTest(unittest.TestCase):
    def test_float_sum(self):
        a = 0.1 + 0.2 + 0.3 + 0.1 + 0.2 + 0.1
        self.assertAlmostEqual(a, 1.0, places=5)

if __name__ == '__main__':
    unittest.main()