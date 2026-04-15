import json
from pathlib import Path
from typing import List, Dict
from schema.product import Product


BASE_DIR = Path(__file__).parent.parent  # go up one level cleanly
DATA_FILE1 = BASE_DIR / "data" / "products.json"
DATA_FILE2 = BASE_DIR / "data" / "dummy.json"

# print(__file__)
# print(DATA_FILE1)


def load_products1() -> List[Dict]:
    if not DATA_FILE1.exists():
        return []
    with open(DATA_FILE1, "r", encoding="utf-8") as f:
        return json.load(f)


def get_all_products1() -> List[Dict]:

    return load_products1()


def load_products2() -> List[Dict]:
    if not DATA_FILE2.exists():
        return []
    with open(DATA_FILE2, "r", encoding="utf-8") as f:
        return json.load(f)  # directly converts to python obj


def get_all_products2() -> List[Dict]:

    return load_products2()


def addProducts1(products: List[dict]):  # Rewrite the whole file
    with open(DATA_FILE2, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2)


def deleteProduct(id: str):

    products: List[Product] = get_all_products2()
    print("=" * 100)
    # print(products[0]["id"])  # This works fine
    # print(products[0].id)  # But this  throws error ?
    # print(type(products[0]["id"]))
    # print(type(id))

    filered_products_after_deletion = [
        product for product in products if not product["id"] == id
    ]
    print(filered_products_after_deletion)
    if filered_products_after_deletion == products:
        raise ValueError(f"Product with ID :{id} not found")
    with open(DATA_FILE2, "w") as f:
        json.dump(filered_products_after_deletion, f, indent=2)
