# Static method : Just a normal function which doesnt need the reference of the class instance just like a single solo function or helper / utility function :


class ChaiUtils:
    @staticmethod
    def clean_ingridents(text):

        return [item.strip() for item in text.split(",")]


raw = " water , milk  ,ginger"


obj = ChaiUtils()
filtered = obj.clean_ingridents(
    raw
)  # Error if not used static : because if the method is not static python passes self reference into the paramater  which we were not accepting in thr fn
filtered1 = ChaiUtils.clean_ingridents(
    raw
)  # No any error even if static isn't used  ✅ Works — no self is auto-passed when calling on the class directly
print(filtered)
print(filtered1)
