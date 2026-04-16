import json
from pathlib import Path
from typing import List, Dict
from schema.product import Product, ProductUpdate


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
        return json.load(f)  # directly converts to python obj(dict)


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


def deep_merge(base: dict, updates: dict) -> dict:
    result = base.copy()
    for key, value in updates.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def updateProduct(product_updates: ProductUpdate):
    all_products = load_products2()  # This excludes the deleted product

    # convert dict → Product
    product_models = [Product(**p) for p in all_products]
    try:
        old_product = [p for p in product_models if p.id == product_updates.id][0]
    except IndexError:
        raise ValueError(f"No any product found with ID {str(product_updates.id)}")
    old_product_dict = old_product.model_dump(mode="json", exclude_none=True)
    product_updates_dict = product_updates.model_dump(mode="json", exclude_none=True)

    #  update the dict + nested dict
    updated_product = deep_merge(old_product_dict, product_updates_dict)
    # print(updated_product)

    # remove the dict with the id
    deleteProduct(str(product_updates.id))

    # insert the updated dict
    all_products = load_products2()  # This excludes the deleted product
    all_products.append(updated_product)
    addProducts1(all_products)
