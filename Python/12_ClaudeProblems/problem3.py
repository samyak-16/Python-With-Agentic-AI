# One thread produces numbers 1-10
# (with 0.5s delay between each).
# Another thread consumes them
# and prints "consumed: X".
# Use Queue for communication between them.