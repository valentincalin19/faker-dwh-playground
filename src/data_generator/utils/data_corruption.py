import random
import re
from src.data_generator.utils.data_utils import DataUtils

class DataCorruption:
    def __init__(self) -> None:
        self.data_utils = DataUtils()

    def _should_corrupt(self) -> bool:
        return self.data_utils.choose_random("low")

    def corrupt_user_str(self, user_str: str) -> str | None:
        """Insert random chars and randomly change case, or return None."""
        if self._should_corrupt():
            return None

        if self._should_corrupt():
            for char in self.data_utils.select_random_chars():
                user_str = self.data_utils.insert_randomly(user_str, char)

        if self._should_corrupt():
            user_str = user_str.lower() if random.choice([True, False]) else user_str.upper()

        return user_str

    def corrupt_user_email(self, user_email: str) -> str | None:
        """Replace '@' with special char and insert random chars, or return None."""
        if self._should_corrupt():
            return None

        if self._should_corrupt():
            user_email = user_email.replace("@", random.choice(["$", "#", "&"]))

        if self._should_corrupt():
            for char in self.data_utils.select_random_chars():
                user_email = self.data_utils.insert_randomly(user_email, char)

        return user_email

    def corrupt_user_date(self, user_date: str) -> str | None:
        """Apply random date corruptions or return None."""
        if self._should_corrupt():
            return None

        corruptions = [
            lambda d: re.sub(r"[-/:]", random.choice(["/", "-", ".", " "]), d) if self._should_corrupt() else d,
            lambda d: re.sub(r"\s+\d{2}:\d{2}(:\d{2})?", "", d) if self._should_corrupt() else d,
            lambda d: re.sub(r"(\d{2})[-/](\d{2})", r"\2-\1", d) if self._should_corrupt() else d,
            lambda d: d + random.choice([" Z", " UTC", " GMT+3"]) if self._should_corrupt() else d,
            lambda d: d.lower() if self._should_corrupt() else d,
        ]

        # Randomly apply 1 to all corruptions
        for corruption in random.sample(corruptions, k=random.randint(1, len(corruptions))):
            try:
                user_date = corruption(user_date)
            except re.error as e:
                print(f"Warning: regex corruption failed with error: {e}")

        return user_date
    
    def corrupt_user_is_active(self, user_is_active: bool) -> bool | str | None:
        """Change from bool to string or return None."""
        if self._should_corrupt():
            return None
        
        if self._should_corrupt():
            return str(user_is_active)
        
    def corrupt_user_loyalty_points(self, user_loyalty_points: int, max_points: int) -> int | None:
        """Change from valid range or return None."""
        if self._should_corrupt():
            return None

        if self._should_corrupt():
            return user_loyalty_points + max_points



