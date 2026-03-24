import time


def make_coffee():
    print("boiling water...")
    time.sleep(3)  # just sits here waiting 3 seconds
    print("coffee ready")


def make_toast():
    print("toasting bread...")
    time.sleep(2)
    print("toast ready")


make_coffee()  # waits 3 seconds doing nothing
make_toast()  # only starts after coffee done
# total: 5 seconds

# CPU is just **sitting idle** during those sleeps. Waiting. Doing nothing. Wasting time.

# ---

# ## The Real World Problem

# In backend work — almost everything is waiting.
# ```
# send DB query     → wait 100ms for response
# call external API → wait 500ms for response
# read a file       → wait 50ms from disk
# ```

# Your CPU is idle 90% of the time just waiting. Meanwhile other requests are piling up.

# ---

# ## What If You Could Say "While Waiting, Go Do Something Else"?
# ```
# start making coffee → water boiling (waiting)
#                    → hey, while waiting — start making toast
#                    → toast done ✅
#                    → coffee done ✅
# total: 3 seconds instead of 5
