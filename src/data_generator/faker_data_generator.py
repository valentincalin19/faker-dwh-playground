import csv
import os
from typing import List, Any
from src.data_generator.utils.config_loader import ConfigLoader
from src.data_generator.base_generator import BaseGenerator
from src.data_generator.users_generator import UserGenerator, User
from src.data_generator.products_generator import ProductGenerator, Product
from src.data_generator.transactions_generator import TransactionGenerator


class DataGenerator:
    def __init__(self, config_file="files_config.json"):
        self.config = ConfigLoader.load_config(config_file)

    def write_csv(self, generator: BaseGenerator, config_key: str) -> List[Any]:
        file_config = self.config[config_key]
        file_path = os.path.join(self.config["OUTPUT_PATH"], file_config["file_name"])
        count = file_config["rows"]

        records = generator.generate_records(count)

        with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(vars(records[0]).keys()) 
            for record in records:
                writer.writerow(vars(record).values())

        return records


if __name__ == "__main__":
    data_generator = DataGenerator()

    users = data_generator.write_csv(UserGenerator(), "USERS_FILE")
    products = data_generator.write_csv(ProductGenerator(), "PRODUCTS_FILE")
    
    transaction_generator = TransactionGenerator(users, products)
    data_generator.write_csv(transaction_generator, "TRANSACTIONS_FILE")