import pandas as pd

from app.services.profiling import profile_dataset

data = {
    "name": ["Ashif", "Rahul", "Aman", "Priya", "Ashif"],
    "age": [22, 24, None, 23, 22],
    "salary": [25000, 30000, 28000, None, 25000],
    "department": ["IT", "HR", "IT", "Finance", "IT"]
}

df = pd.DataFrame(data)

print("\nDATASET PROFILE:")
print(profile_dataset(df))


# import pandas as pd

# from app.services.profiling import profile_dataset

# df = pd.DataFrame(columns=["name", "age", "salary"])

# print("\nDATASET PROFILE:")
# print(profile_dataset(df))

# import pandas as pd

# from app.services.profiling import profile_dataset

# # data = {
# #     "name": ["Ashif", "Rahul", "Aman", "Priya"],
# #     "city": ["Delhi", "Mumbai", "Delhi", "Pune"],
# #     "department": ["IT", "HR", "IT", "Finance"]
# # }
# data = {
#     "name": ["Ashif", "Rahul", "Aman"],
#     "department": [None, None, None],
#     "city": ["Delhi", "Mumbai", "Pune"]
# }

# df = pd.DataFrame(data)

# print("\nDATASET PROFILE:")
# print(profile_dataset(df))

# import pandas as pd

# from app.services.profiling import profile_dataset

# data = [
#     ["Ashif", 22, 50000, "IT"],
#     ["Rahul", 24, 60000, "HR"]
# ]

# df = pd.DataFrame(
#     data,
#     columns=["name", "age", "age", "department"]
# )

# print("\nDATASET PROFILE:")
# print(profile_dataset(df))





























