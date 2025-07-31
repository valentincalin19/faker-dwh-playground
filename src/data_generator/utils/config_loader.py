import json
import os

class ConfigLoader:
    @staticmethod
    def load_config(config_name: str) -> dict:
        """Load JSON configuration file from config folder."""
        base_path = os.path.join(os.path.dirname(__file__), "..", "config")
        file_path = os.path.join(base_path, config_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Config file not found at: {file_path}")

        with open(file_path, "r") as config_file:
            return json.load(config_file)