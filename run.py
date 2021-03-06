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
    """ 
    Get sales figures input from the user. 
    Run a while loop to collect a valid string of data from the user via the terminal. which must be a string of 6 numbers separated by commas. The loop will repeatedly request data, until it is in a valid format.
    """
    while True: #repeats the condition each time the loop runs
        print('Please enter sales data from the last market.')
        print('Data should be six numbers, separated by commas.')
        print('Example: 10,20,30,40,50,60\n')

        data_str = input('Enther your data here:\n')
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




# # function to insert sales data into our google sale worksheet:
# def update_sales_worksheet(data):
#     """
#     Update sales google worksheet, add new row with the list data provided
#     """
#     print('Updating sales worksheet...\n')
#     sales_worksheet = SHEET.worksheet('sales') # accessing our sales_worksheet from our google sheet
#     sales_worksheet.append_row(data) # adds a new row in the google worksheet selected
#     print('Sales worksheet updated successfully!\n')

# # function to insert sales data into our google surplus worksheet:
# def update_surplus_worksheet(data):
#     """
#     Function to update surplus google worksheet, add new row with the list data provided
#     """
#     print('Updating surplus worksheet...\n')
#     surplus_worksheet = SHEET.worksheet('surplus')
#     surplus_worksheet.append_row(data)

#     print('Surplus worksheet updated successfully!\n')

# need to update stock worksheet - however can remove the repetition of code by refactoring:

def update_worksheet(data, worksheet_name):
    """
    Recieves a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f'Updating {worksheet_name} worksheet...')
    worksheet_to_update = SHEET.worksheet(worksheet_name)
    worksheet_to_update.append_row(data)

    print(f'{worksheet_name} worksheet updated successfully!\n')



# function to calculate surplus / deficit data
def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock: 
    - Positive indicates waste
    - Negative indicates sold out state and an increased demand over what was projected.
    """
    print('Calculating surplus data...')
    stock = SHEET.worksheet('stock').get_all_values() # gets all of the cells from our stock worksheet
    # pprint(stock) # easier to read data than print(), however it needs to be installed at top of the file "from pprint import pprint"
    stock_row = stock[-1] # using a slice will 'slice' the final items from the list and return it to the new stock varibale'
    # print(f'Stock row: {stock_row}')
    # print(f'Sales row: {sales_row}')

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row): # zip function that allows us to access two separate lists at the same time
        surplus = int(stock) - sales # here we have used another method to change the sock 'string' value into an 'integer' value as alternative to [int(num) of num in (stock_data)]
        surplus_data.append(surplus)
    # print(surplus_data)
    return surplus_data



def get_last_5_entries_sales():
    """
    Collects coloumns of data from sales worksheet, for the last 
    5 entries for each sandwich class and returns the data as 
    a list of lists.
    """
    sales = SHEET.worksheet('sales')
    # coloumn = sales.col_values(3)
    coloums = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        coloums.append(column[-5:])
    return coloums


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print('Calculating stock data...')

    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column] # creates a list of integers from strings using list comprehension
        average = sum(int_column) / len(int_column) # the average sales calculation
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num)) # append the average number to the new_stock_data list outside the for loop
    # print(new_stock_data)
    return new_stock_data

def main():
    """
    Run all program functions
    """
    data = get_sales_data() # defining 'data' as a variable and the place to put the returned, 'vaidated' get_sales_data()
    sales_data = [int(num) for num in data] # new variable to convert values in 'data' output (which is in string format) into integers with a loop in list comprension format.
    # update_sales_worksheet(sales_data) # to call the function and pass it sales_data list
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data) # to call the function and pass it sales_data list
    # print(new_surplus_data)
    # update_surplus_worksheet(new_surplus_data)
    update_worksheet(new_surplus_data, 'surplus')
    sales_columns = get_last_5_entries_sales() 
    stock_data = calculate_stock_data(sales_columns) # passing the calculate_stock_data function the returned data from the get_last_5_entries_sales function as the information to calculate from
    update_worksheet(stock_data, 'stock')
    
print('Welcome to Love Sandwiches data Automation\n')
main() # functions must be called below where they are defined

def get_stock_values(data):
    """
    Builds a dictionary, where the keys are the sandwich headings pulled from the spreadsheet, and the values are the calculated stock data.Request data from a worksheet

    Requests data from a worksheet
    Builds a dictionary
    Print the dictionary to the terminal for the user
    """
    headings = SHEET.worksheet('sales').row_values(1) # Requests data from a worksheet
    dictionary = {key:value for key,value in zip(headings,stock_data)} # Builds a dictionary using dictionary comprehension syntax
    return dictionary

stock_values = get_stock_values(stock_data) 
print(stock_values) # Prints the dictionary to the terminal for the user