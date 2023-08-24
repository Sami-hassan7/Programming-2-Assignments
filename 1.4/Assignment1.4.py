def applied_functions(data, *functions):
    return [[func(item) for item in data] for func in functions]

data = [1, 2, 3, 4, 5]

# Define the functions to be applied
multiplied_by_two = lambda x: x * 2
five_addition = lambda x: x + 5

# Apply the functions to the data
result = applied_functions(data, multiplied_by_two, five_addition)

print(result)
