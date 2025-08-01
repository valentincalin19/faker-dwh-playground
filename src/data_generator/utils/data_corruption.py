import random
import re
from src.data_generator.utils.data_utils import DataUtils

class DataCorruption:
    def __init__(self) -> None:
        self.data_utils = DataUtils()

    def _should_corrupt(self) -> bool:
        return self.data_utils.choose_random("low")

    def corrupt_string(self, text: str) -> str | None:
        """Insert random chars and randomly change case, or return None."""
        if self._should_corrupt():
            return None

        if self._should_corrupt():
            for char in self.data_utils.select_random_chars():
                text = self.data_utils.insert_randomly(text, char)

        if self._should_corrupt():
            text = text.lower() if random.choice([True, False]) else text.upper()

        return text

    def corrupt_email(self, email: str) -> str | None:
        """Replace '@' with special char and insert random chars, or return None."""
        if self._should_corrupt():
            return None

        if self._should_corrupt():
            email = email.replace("@", random.choice(["$", "#", "&"]))

        if self._should_corrupt():
            for char in self.data_utils.select_random_chars():
                email = self.data_utils.insert_randomly(email, char)

        return email

    def corrupt_date(self, date_str: str) -> str | None:
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
                date_str = corruption(date_str)
            except re.error as e:
                print(f"Warning: regex corruption failed with error: {e}")

        return date_str
    
    def corrupt_is_active(self, is_active: bool) -> bool | str | None:
        """Change from bool to string or return None."""
        if self._should_corrupt():
            return None
        
        if self._should_corrupt():
            return f"'{is_active}'"
        
        return is_active
        
    def corrupt_integer(self, amount: int, max_amount: int) -> int | None:
        """Change from valid range or return None."""
        if self._should_corrupt():
            return None

        if self._should_corrupt():
            return amount + max_amount
        elif self._should_corrupt():
            return amount - max_amount
        
        return amount



