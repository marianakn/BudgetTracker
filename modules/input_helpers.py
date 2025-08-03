def get_valid_number(prompt):
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Please enter numbers only (e.g. 100.50)")
