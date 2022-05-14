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
    while True: #repeats the condition each time the loop runs
        print('Please enter sales data from the last market.')
        print('Data should be six numbers, separated by commas.')
        print('Example: 10,20,30,40,50,60\n')

        data_str = input('Enther your data here: ')
        # print(f'The data provided is {data_str}') # just to check the string inp ut is being recieved correctly

        sales_data = data_str.split(',')
        # print(f'The data you provided converted into a list of strings is:\n{sales_data}')
        # validate_data(sales_data) # calls the function below and puts the .split() data into it

        # once we have confirmed our data is valid by calling the ValidateData() finction via an if statement, we can end the while loop with the break keyword:
        if validate_data(sales_data): # to confrim our data is valid
            print('Data is valid')
            break # while loop is stopped

    return sales_data # return the validated sales data

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
        return False # produce a False value and provides an input for our if statement to continue the while loop until we get the appropriate data
    
    return True # to produce a True value if no errors and provides an input for our if statement to end the while loop

data = get_sales_data() # defining 'data' as a variable and the place to put the returned, vaidated sales data

