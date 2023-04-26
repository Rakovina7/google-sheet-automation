import gspread
from google.oauth2.service_account import Credentials
from datetime import date

# Set up the credentials
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('json file here path', scopes=scope)

# Connect to Google Sheets
client = gspread.authorize(creds)

# Open the Google Sheet using its name or ID
sheet = client.open_by_key('sheet key').sheet1

# Set the column index of the phone numbers (0-based index)
phone_number_column = 0

# Set the column index of the "Last Updated" column (0-based index)
last_updated_column = 1

# Get the current date
today = date.today().strftime('%Y-%m-%d')

# Get all values in the phone number column
phone_numbers = sheet.col_values(phone_number_column + 1)

# Prepare the update requests
requests = []
for row, phone_number in enumerate(phone_numbers, start=1):
    if phone_number:
        requests.append({
            'range': sheet.cell(row, last_updated_column + 1).address,
            'values': [[today]]
        })
    else:
        break

# Update the cells using a single batch request
if requests:
    sheet.batch_update(requests)
