import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# sales = SHEET.worksheet('sales') # just to check the sales sheet connection is working
# data = sales.get_all_values()
# print(data)

def get_sales_data():
    """ Get sales figures input from the user """
    print('Please enter sales data from the last market.')
    print('Data should be six numbers, separated by commas.')
    print('Example: 10,20,30,40,50,60\n')

    data_str = input('Enther your data here: ')
    # print(f'The data provided is {data_str}') # just to check the string inp ut is being recieved correctly

    sales_data = data_str.split(',')
    # print(f'The data you provided converted into a list of strings is:\n{sales_data}')
    validate_data(sales_data) # calls the function below and puts the .split() data into it

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int or
    if there are not exactly 6 values.
    """
    # print(f'The data you provided converted into a list of strings is:\n{values}')

    try:
        [int(value) for value in values] # list comprehension to convert 'strings' into integers. Syntax is [expression for item in iterable if condition == True]
        if len(values) !=6: #if the length of the values input 'does not equal' 6
            raise ValueError(
                f'`Exactly 6 values required, you provided {len(values)}'
            )
    # ValueError class contains the details of the error (as defined above). By using the 'as' keyword we are assigning the ValueError object to the variable 'e' meaning 'error':
    except ValueError as e:
        print(f'Invalid data : {e}, please try again.\n')

get_sales_data()