import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey There ! My name is Samyak Raj Subedi, And Im From Biratnagar Currently in grade 12th"

# tokens = enc.encode(text)
# Tokens : [25216, 3274, 1073, 3673, 1308, 382, 8726, 68720, 40516, 5934, 7859, 11, 1958, 3133, 7217, 25152, 266, 77, 23482, 35002, 306, 15349, 220, 899, 404]
# print("Tokens :", tokens) 

decoded_token = enc.decode(
    [
        25216,
        3274,
        1073,
        3673,
        1308,
        382,
        8726,
        68720,
        40516,
        5934,
        7859,
        11,
        1958,
        3133,
        7217,
        25152,
        266,
        77,
        23482,
        35002,
        306,
        15349,
        220,
        899,
        404,
    ]
)

print("Tokens decoded  :", decoded_token)
