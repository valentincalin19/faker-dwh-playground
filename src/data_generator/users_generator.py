from faker import Faker
import csv
import os
import random
from datetime import datetime, date
from src.data_generator.base_generator import BaseGenerator
from src.data_generator.utils.data_corruption import DataCorruption
from src.data_generator.utils.config_loader import ConfigLoader


class User:
    def __init__(
        self, user_id: str, first_name: str, last_name: str, email: str, signup_date: str, 
        country: str, city: str, birth_date: str, is_active: bool, loyalty_points: int
        ) -> None:
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.signup_date = signup_date
        self.country = country
        self.city = city
        self.birth_date = birth_date
        self.is_active = is_active
        self.loyalty_points = loyalty_points

    def __str__(self) -> str:
        return (
            f"user_id: {self.user_id}\n"
            f"first_name: {self.first_name}\n"
            f"last_name: {self.last_name}\n"
            f"email: {self.email}\n"
            f"signup_date: {self.signup_date}\n"
            f"country: {self.country}\n"
            f"city: {self.city}\n"
            f"birth_date: {self.birth_date}\n"
            f"is_active: {self.is_active}\n"
            f"loyalty_points: {self.loyalty_points}"
        )

class UserGenerator(BaseGenerator):
    def __init__(self, config_file="users_config.json") -> None:
        self.config = ConfigLoader.load_config(config_file)
        self.fake = Faker()
        self.data_corruption = DataCorruption()

    def generate_record(self) -> User:
        """Generate a random user based on config and Faker."""
        datetime_formats = self.config["DATETIME_FORMATS"]
        date_formats = self.config["DATE_FORMATS"]
        countries = self.config["COUNTRIES"]
        max_loyalty_points = self.config["MAX_LOYALTY_POINTS"]
        
        signup_date = self.fake.date_time_between(start_date="-10y", end_date="now")
        signup_date_str = signup_date.strftime(random.choice(datetime_formats))

        birth_date = self.fake.date_between(start_date="-80y", end_date="-18y")
        birth_date_str = birth_date.strftime(random.choice(date_formats))

        country = random.choice(list(countries))
        city = random.choice(countries[country])

        user = User(
            user_id=self.fake.uuid4(),
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.fake.email(),
            signup_date=signup_date_str,
            country=country,
            city=city,
            birth_date=birth_date_str,
            is_active=random.random() < 0.3,
            loyalty_points=random.randint(0, max_loyalty_points)
        )
        user = self.inject_errors(user)

        return user
    
    def inject_errors(self, user: User) -> User:
        """Apply random corruptions to selected user fields."""
        corruption_map = {
            "first_name": self.data_corruption.corrupt_user_str,
            "last_name": self.data_corruption.corrupt_user_str,
            "email": self.data_corruption.corrupt_user_email,
            "signup_date": self.data_corruption.corrupt_user_date,
            "country": self.data_corruption.corrupt_user_str,
            "city": self.data_corruption.corrupt_user_str,
            "birth_date": self.data_corruption.corrupt_user_date,
            "is_active": self.data_corruption.corrupt_user_is_active,
            "loyalty_points": lambda d: self.data_corruption.corrupt_user_loyalty_points(d, self.config["MAX_LOYALTY_POINTS"])
        }

        attrs_to_corrupt = random.sample(list(corruption_map.keys()), k=random.randint(1, len(corruption_map)))

        for attr in attrs_to_corrupt:
            corrupter = corruption_map[attr]
            attr_value = getattr(user, attr)
            setattr(user, attr, corrupter(attr_value))

        return user
