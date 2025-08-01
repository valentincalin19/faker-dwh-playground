from faker import Faker
import random
from src.data_generator.utils.config_loader import ConfigLoader
from src.data_generator.utils.data_corruption import DataCorruption
from src.data_generator.base_generator import BaseGenerator



class Product:
    def __init__(
        self, product_id: str, product_name: str, category: str, subcategory: str,
        price: float, currency: str, created_at: str, stock_quantity: int, is_active: bool
    ) -> None:
        self.product_id = product_id
        self.product_name = product_name
        self.category = category
        self.subcategory = subcategory
        self.price = price
        self.currency = currency
        self.created_at = created_at
        self.stock_quantity = stock_quantity
        self.is_active = is_active

    def __str__(self) -> str:
        return(
            f"product_id: {self.product_id}\n"
            f"product_name: {self.product_name}\n"
            f"category: {self.category}\n"
            f"subcategory: {self.subcategory}\n"
            f"price: {self.price}\n"
            f"currency: {self.currency}\n"
            f"created_at: {self.created_at}\n"
            f"stock_quantity: {self.stock_quantity}\n"
            f"is_active: {self.is_active}"
        )

class ProductGenerator(BaseGenerator):
    def __init__(self, config_file="products_config.json") -> None:
        self.config = ConfigLoader.load_config(config_file)
        self.fake = Faker()
        self.data_corruption = DataCorruption()

    def generate_record(self) -> Product:
        """Generate a random product based on config and Faker."""
        products = self.config["PRODUCTS"]
        date_formats = self.config["DATE_FORMATS"]
        currencies = self.config["CURRENCIES"]
        max_price = self.config["MAX_PRICE"]
        max_quantity = self.config["MAX_QUANTITY"]

        category = random.choice(list(products.keys()))
        subcategory = random.choice(list(products[category]))
        product_name = random.choice(list(products[category][subcategory]))

        created_at = self.fake.date_between(start_date="-5y", end_date="now")
        created_at_str = created_at.strftime(random.choice(date_formats))

        product = Product(
            product_id=self.fake.uuid4(),
            product_name=product_name,
            category=category,
            subcategory=subcategory,
            price=random.randint(0, max_price),
            currency=random.choice(currencies),
            created_at=created_at_str,
            stock_quantity=random.randint(0, max_quantity),
            is_active=random.random() < 0.2
        )
        product = self.inject_errors(product)

        return product

    def inject_errors(self, product: Product) -> Product:
        """Apply random corruptions to selected product fields."""
        corruption_map = {
            "product_name": self.data_corruption.corrupt_string,
            "category": self.data_corruption.corrupt_string,
            "subcategory": self.data_corruption.corrupt_string,
            "price": lambda d: self.data_corruption.corrupt_integer(d, self.config["MAX_PRICE"]),
            "currency": self.data_corruption.corrupt_string,
            "created_at": self.data_corruption.corrupt_date,
            "stock_quantity": lambda d: self.data_corruption.corrupt_integer(d, self.config["MAX_QUANTITY"]),
            "is_active": self.data_corruption.corrupt_is_active
        }

        attrs_to_corrupt = random.sample(list(corruption_map.keys()), k=random.randint(1, len(corruption_map)))

        for attr in attrs_to_corrupt:
            corrupter = corruption_map[attr]
            attr_value = getattr(product, attr)
            setattr(product, attr, corrupter(attr_value))

        return product
