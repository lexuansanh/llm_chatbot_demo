import os
import random

import yaml

from src.config.constants import Constant


def load_yaml_config(config_path="config/settings.yaml"):
    """
    Loads a YAML configuration file.

    Args:
        config_path (str): Path to the YAML configuration file.

    Returns:
        dict: Parsed YAML configuration data.
    """
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def update_text_with_image(text):
    """
    Replaces occurrences of predefined image names in the text with HTML image tags.

    Args:
        text (str): The input text containing image placeholders.

    Returns:
        tuple: (Updated text with HTML image tags, List of image URLs)
    """
    image_links = []

    for image in list(set(Constant.LIST_IMAGES)):  # Ensure unique images
        if image in text:
            image_links.append(f"https://example.com/{image}")  # Generate image link
            text = text.replace(
                image,
                f"<img style='margin: 8px; width: 100%' src='https://iili.io/{image}' />",
            )

    text = text.strip().replace("\n", "<br>").replace('"', "'")  # Clean formatting

    return text, image_links
