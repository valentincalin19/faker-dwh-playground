import random
from typing import List

class DataUtils:
    @staticmethod
    def insert_randomly(s: str, insertion: str) -> str:
        """Insert a string at a random position in another string."""
        pos = random.randint(0, len(s))
        return s[:pos] + insertion + s[pos:]

    @staticmethod
    def choose_random(probability: str = "low") -> bool:
        """Return True or False based on a probability range."""
        ranges = {
            "high": (0.05, 0.15),
            "medium": (0.03, 0.10),
            "low": (0.01, 0.05)
        }
        min_prob, max_prob = ranges.get(probability.lower(), ranges["low"])
        threshold = random.uniform(min_prob, max_prob)
        return random.random() < threshold

    @staticmethod
    def select_random_chars(k: int = None) -> List[str]:
        """Select a list of random special characters."""
        chars_pool = ["!", "~", "$", "^", "&", "*", "()", "@"]
        if k is None:
            k = random.randint(1, 3)
        return random.choices(chars_pool, k=k)
