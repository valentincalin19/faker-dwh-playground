import random

from faker import Faker
from typing import List
from src.data_generator.utils.config_loader import ConfigLoader
from src.data_generator.utils.data_corruption import DataCorruption
from src.data_generator.base_generator import BaseGenerator
from src.data_generator.users_generator import User
from src.data_generator.products_generator import Product

class Transaction:
    def __init__(
        self, transaction_id: str, user_id: str, product_id: str, quantity: int, unit_price: float,
        discount: int, total_amount: float, currency: str, transaction_date: str, payment_method: str, status: str
    ) -> None:
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.discount = discount
        self.total_amount = total_amount
        self.currency = currency
        self.transaction_date = transaction_date
        self.payment_method = payment_method
        self.status = status

    def __str__(self) -> str:
        return(
            f"transaction_id: {self.transaction_id}\n"
            f"user_id: {self.user_id}\n"
            f"product_id: {self.product_id}\n"
            f"quantity: {self.quantity}\n"
            f"unit_price: {self.unit_price}\n"
            f"discount: {self.discount}\n"
            f"total_amount: {self.total_amount}\n"
            f"currency: {self.currency}\n"
            f"transaction_date: {self.transaction_date}\n"
            f"payment_method: {self.payment_method}\n"
            f"status: {self.status}\n"
        )
    
class TransactionGenerator(BaseGenerator):
    def __init__(
        self, users: List[User], products: List[Product], 
        config_file="transactions_config.json"
    ) -> None:
        self.config = ConfigLoader.load_config(config_file)
        self.fake = Faker()
        self.data_corruption = DataCorruption()
        self.users = users
        self.products = products

    def generate_record(self) -> Transaction:
        """Generate a random transaction based on config and Faker."""
        user = random.choice(self.users)
        product = random.choice(self.products)

        max_quantity = self.config["MAX_QUANTITY"]
        max_discount = self.config["MAX_DISCOUNT"]
        datetime_formats = self.config["DATETIME_FORMATS"]
        currencies = self.config["CURRENCIES"]
        payment_methods = self.config["PAYMENT_METHODS"]
        statuses = self.config["STATUSES"]

        transaction_date = self.fake.date_time_between(start_date="-3y", end_date="now")
        transaction_date_str = transaction_date.strftime(random.choice(datetime_formats))

        quantity = random.randint(0, max_quantity)
        discount = random.randint(0, max_discount)

        if product.price:
            total_amount = (product.price * quantity) - (discount * (product.price * quantity) / 100)
        else:
            total_amount = 0

        transaction = Transaction(
            transaction_id=self.fake.uuid4(),
            user_id=user.user_id,
            product_id=product.product_id,
            quantity=quantity,
            unit_price=product.price,
            discount=random.randint(0, max_discount),
            total_amount=total_amount,
            currency=random.choice(currencies),
            transaction_date=transaction_date_str,
            payment_method=random.choice(payment_methods),
            status=random.choice(statuses)
        )
        transaction = self.inject_errors(transaction)

        return transaction

    def inject_errors(self, transaction: Transaction) -> Transaction:
        """Apply random corruptions to selected product fields."""
        corruption_map = {
            "user_id": self.data_corruption.corrupt_string,
            "product_id": self.data_corruption.corrupt_string,
            "quantity": lambda d: self.data_corruption.corrupt_integer(d, self.config["MAX_QUANTITY"]),
            "unit_price": lambda d: self.data_corruption.corrupt_integer(d, self.config["MAX_PRICE"]),
            "discount": lambda d: self.data_corruption.corrupt_integer(d, self.config["MAX_DISCOUNT"]),
            "total_amount": lambda d: self.data_corruption.corrupt_integer(d, self.config["MAX_PRICE"]*self.config["MAX_QUANTITY"]),
            "currency": self.data_corruption.corrupt_string,
            "transaction_date": self.data_corruption.corrupt_date,
            "payment_method": self.data_corruption.corrupt_string,
            "status": self.data_corruption.corrupt_string
        }

        attrs_to_corrupt = random.sample(list(corruption_map.keys()), k=random.randint(1, len(corruption_map)))

        for attr in attrs_to_corrupt:
            attr_value = getattr(transaction, attr)
            corrupter = corruption_map[attr]
            setattr(transaction, attr, corrupter(attr_value))

        return transaction