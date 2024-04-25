from datetime import timedelta, date

def add_date():
    today = date.today()
    ex_date = today + timedelta(days=30)
    return ex_date

def check_expi(saved_date):
    today = date.today()
    if saved_date > today:
        return True  # Not expired
    else:
        return False  # Expired

# Example usage
expiration_date = add_date()
print("Expiration Date:", expiration_date)

# Replace this with the date you want to check
saved_date = expiration_date  
if check_expi(saved_date):
    print("Not expired")
else:
    print("Expired")
