import random

class Dice:
    def __init__(self, probabilities):
        if len(probabilities) != 6:
            raise ValueError("ต้องมี 6 ค่า")
        
        for p in probabilities:
            if not isinstance(p, (int, float)):
                raise ValueError("ทุกค่าต้องเป็นตัวเลข")
        
        for p in probabilities:
            if p < 0:
                raise ValueError("ความน่าจะเป็นต้องไม่ติดลบ")
        
        total = sum(probabilities)
        if abs(total - 1.0) > 0.000000001:
            raise ValueError(f"ผลรวมต้องเป็น 1.0 แต่ได้ {total}")
        
        self.probabilities = probabilities
        self.outcomes = [1, 2, 3, 4, 5, 6]
    
    def roll_multiple(self, count):
        results = random.choices(self.outcomes, weights=self.probabilities, k=count)
        return results