from .input_helpers import get_valid_number

def format_name(raw):
    parts = raw.strip().split()
    return " ".join(p.capitalize() for p in parts)

def read_customer_data_manual():
    raw_name = input("Enter your full name: ")
    name = format_name(raw_name)
    balance = get_valid_number("Enter your current balance: ")
    loan = get_valid_number("Enter your active loan balance: ")
    return name, balance, loan

def read_customer_data_file(file_path):
    try:
        with open(file_path, "r") as f:
            line = f.readline().strip()
            parts = line.split(", ")
            if len(parts) != 4:
                raise ValueError("Invalid file format")
            raw_name = f"{parts[0]} {parts[1]}"
            name = format_name(raw_name)
            balance = float(parts[2])
            loan = float(parts[3])
            print('data', name, balance, loan)
            return name, balance, loan
    except FileNotFoundError:
        print("File not found.")
        exit()
    except ValueError:
        print("Invalid data format in the file.")
        exit()
