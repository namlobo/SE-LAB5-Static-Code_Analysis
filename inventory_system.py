"""
Simple inventory management system with safe file handling and logging.
"""

import json
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(filename="inventory.log", level=logging.INFO)

stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Add or update item quantity in stock."""
    if logs is None:
        logs = []
    if not isinstance(item, str) or not isinstance(qty, int):
        logging.warning("Invalid item or quantity type.")
        return None
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info("Added %d of %s", qty, item)
    return True


def remove_item(item, qty):
    """Remove quantity from an item if it exists."""
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
        logging.info("Removed %d of %s.", qty, item)
    except KeyError:
        logging.warning("Attempted to remove non-existing item: %s", item)


def get_qty(item):
    """Return current quantity of given item."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Safely load stock data from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        logging.info("Inventory loaded from file.")
        return data
    except FileNotFoundError:
        logging.warning("No inventory file found — starting fresh.")
        return {}


def save_data(file="inventory.json"):
    """Save stock data to JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f)
    logging.info("Inventory saved to file.")


def print_data():
    """Print full inventory report."""
    print("\nItems Report")
    for item, qty in stock_data.items():
        print("%s -> %d", item, qty)


def check_low_items(threshold=5):
    """Return list of items with low stock."""
    return [i for i, q in stock_data.items() if q < threshold]


def main():
    """Main execution to test inventory system."""
    stock_data.clear()
    stock_data.update(load_data())
    add_item("apple", 10)
    add_item("banana", 3)
    remove_item("apple", 2)
    print("Apple stock:", get_qty("apple"))
    print("Low stock items:", check_low_items())
    save_data()
    print_data()


if __name__ == "__main__":
    main()
