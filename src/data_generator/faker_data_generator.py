import csv
import os

from src.data_generator.utils.config_loader import ConfigLoader
from src.data_generator.base_generator import BaseGenerator
from src.data_generator.users_generator import UserGenerator


class DataGenerator:
    def __init__(self, config_file="files_config.json"):
        self.config = ConfigLoader.load_config(config_file)

    def write_csv(self, generator: BaseGenerator, config_key: str):
        file_config = self.config[config_key]
        file_path = os.path.join(self.config["OUTPUT_PATH"], file_config["file_name"])
        count = file_config["rows"]

        records = generator.generate_records(count)

        with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(vars(records[0]).keys()) 
            for record in records:
                writer.writerow(vars(record).values())


if __name__ == "__main__":
    data_generator = DataGenerator()

    data_generator.write_csv(UserGenerator(), "USERS_FILE")