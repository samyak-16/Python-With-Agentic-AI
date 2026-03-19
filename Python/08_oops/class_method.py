# @classmethod as alternate constructors (most Pythonic for truly different construction logic)
class ChaiOrder:
    def __init__(self, tea_type, sweetness, size):

        self.tea_type = tea_type
        self.sweetness = sweetness
        self.size = size

    @classmethod
    def from_dict(cls, order_data):
        return cls(
            order_data["tea_type"],
            order_data["sweetness"],
            order_data["size"],
        )

    @classmethod
    def from_string(cls, order_data):
        tea_type, sweetness, size = order_data.split("-")
        return cls(tea_type, sweetness, size)


order = ChaiOrder.from_string("capachino-mid-xl")

print(order.size)  # xl - works fine
print(order.__dict__)

# How static method is different


class ChaiUtils:
    @staticmethod
    def is_valid_size(size):
        return size in ["small", "Medium", "Large"]

print(ChaiUtils.is_valid_size("Medium"))