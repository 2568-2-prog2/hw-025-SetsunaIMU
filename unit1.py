import unittest
from dice import Dice

class DiceTest(unittest.TestCase):
    
    def test_probabilities_sum_to_one(self):
        dice = Dice([0.1, 0.2, 0.3, 0.1, 0.2, 0.1])
        self.assertIsNotNone(dice)
        
        # ถ้าผลรวมไม่เป็น 1.0 ต้อง error
        with self.assertRaises(ValueError):
            Dice([0.2, 0.2, 0.2, 0.2, 0.2, 0.2])

    def test_exactly_six_entries(self):
        with self.assertRaises(ValueError):
            Dice([0.5, 0.5])
        
        with self.assertRaises(ValueError):
            Dice([0.1] * 7)
        
        Dice([0.1, 0.2, 0.3, 0.1, 0.2, 0.1])

    def test_no_negative_probabilities(self):
        with self.assertRaises(ValueError):
            Dice([0.1, -0.2, 0.3, 0.1, 0.2, 0.5])
        
        Dice([0.0, 0.2, 0.3, 0.1, 0.2, 0.2])

    def test_random_output_range(self):
        dice = Dice([0.1, 0.2, 0.3, 0.1, 0.2, 0.1])
        rolls = dice.roll_multiple(100)
        for r in rolls:
            self.assertTrue(1 <= r <= 6)

if __name__ == '__main__':
    unittest.main()