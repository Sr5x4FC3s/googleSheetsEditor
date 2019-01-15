from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import sys

#used to import data at runtime
sys.path.insert(0, '/Users/austinlau/Documents/GitHub/pythonApps/virtualenvPython/sprint/data/')
print(sys.path[0])

from data import SPREADSHEET_ID

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

# The ID and range of a spreadsheet.
SPREADSHEETID = SPREADSHEET_ID
RANGE_NAME = 'A1:Z9'

def obtain_credentials():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    # creds = None
    flags = tools.argparser.parse_args(args=[]) #added this to satisfy the three args that run_flow() is looking for to invoke the function
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store, flags)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    return creds

def write(token): 
    credentials = obtain_credentials()
    service = build('sheets', 'v4', http=credentials.authorize(Http()))

    checkpoint = None
    row = None
    letter = None
    #try catch block to check for type of input
    try: 
        value = int(token.inputRow)
        checkpoint = 'integer'
    except ValueError:
        #catch block notifies app that the input was not an integer
        pass 
        checkpoint = 'string'
    
    if checkpoint == 'string':
        #example A2
        #need to parse for the letter and the row 
        array = list(token.inputRow)
        for item in array:
            try:
                value = int(item)
                row = value 
            except ValueError:
                letter = item 
                pass 
            #if this finishes if should set a value to variable 'row'
    else:
        row = token.inputRow

    values = [
        [
            token.inputMake, token.inputModel, token.inputCost
        ],
    ]

    valuesLength = len(values[0])

    determineCellRange = determineRange(valuesLength, row) #format A1-C1
    

    Body = {
        'values' : values,
    }

    result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=determineCellRange, valueInputOption='RAW', body=Body).execute()

    print("Inserted Row")

#this function will write to the next available row in 
def append(token):
    credentials = obtain_credentials()
    service = build('sheets', 'v4', http=credentials.authorize(Http()))

    values = [
        [
            token.inputMake, token.inputModel, token.inputCost
        ]
    ]

    Body = {
        'values': values, 
    }

    result = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME, valueInputOption='RAW', body=Body).execute()
    print('Data has been written!')

def read(spreadsheet_id, range_name): 
    credentials = obtain_credentials()
    service = build('sheets', 'v4', http=credentials.authorize(Http()))

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=range_name).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return False
    else:
        return values

def clear(row):
    credentials = obtain_credentials()
    service = build('sheets', 'v4', http=credentials.authorize(Http()))

    Body = None
    determinedRow = 'a' + str(row) + ':' + 'c' + str(row)

    result = service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range=determinedRow, body=Body).execute()
    print('Desired row has been deleted')

def updateSheets():
    replace = raw_input('do you want to replace any cells on the spreadsheet? \n')

    if replace == 'yes':
        display = raw_input('what rows do you want to be displayed? Please enter values as shown - A1:K4 \n' )
        cellData = read(SPREADSHEET_ID, display)
        if cellData == False: 
            retry = raw_input('Did you want to search for a different cell? (yes/no) \n')
            if retry == 'yes':
                reattempt = raw_input('what rows do you want to be displayed? Please enter values as shown - A1:K4 \n' )
                cellData = read(SPREADSHEET_ID, reattempt)
            else:
                print('If you want to retry, please restart the application and try again') 
                sys.exit() #terminates the app 

        print('data is shown in order of the table - row numbers on the left, column starting from A-Z - if greater than  26, A2+ \n')
        for row in cellData:
            print(cellData.index(row) + 1, ':', row)
        row = raw_input('what row do you want to update? \n')
        make = raw_input('what make? \n')
        model = raw_input('what model? \n')
        cost = raw_input('what price point? \n')

        print('row: ', row)
        print('make: ', make)
        print('model: ', model)
        print('cost: ', cost)

        checkpoint = raw_input('Is this information correct? \n')

        if checkpoint == 'yes':
            #create object to hold our information and check boolean 
            class Token(object):
                inputRow = row
                inputMake = make
                inputModel = model
                inputCost = cost
                boolean = True

            return Token
        else: 
            class Token(object):
                boolean = False

            return Token
    else: 
        class Token(object):
            boolean = 'skipped'

        return Token

def position():
    top = raw_input('top or bottom? \n')

    tableData = read(SPREADSHEET_ID, RANGE_NAME)
    print('data is shown in order of the table - row numbers on the left, column starting from A-Z - if greater than  26, A2+ \n')
    for row in tableData:
        print(tableData.index(row) + 1, ':', row)

    if top == 'top':
        rowStart = 0 #index is 0, but the row is 1
        #need to get cell info from main()
        make = raw_input('what make?\n')
        model = raw_input('what model?\n')
        cost = raw_input('what price point?\n')

        print('make: ', make)
        print('model: ', model)
        print('cost: ', cost)

        checkpoint = raw_input('Is this information correct? (yes/no) \n')

        if checkpoint == 'yes':
            #create object to hold our information and check boolean 
            class Token(object):
                inputMake = make
                inputModel = model
                inputCost = cost
                boolean = True

            return Token
        else: 
            class Token(object):
                boolean = False

            return Token
    else:
        rowStart = len(tableData) 
        make = raw_input('what make?\n')
        model = raw_input('what model?\n')
        cost = raw_input('what price point?\n')

        print('make: ', make)
        print('model: ', model)
        print('cost: ', cost)

        checkpoint = raw_input('Is this information correct? (yes/no) \n')

        if checkpoint == 'yes':
            #create object to hold our information and check boolean 
            class Token(object):
                inputMake = make
                inputModel = model
                inputCost = cost
                boolean = True

            return Token
        else: 
            class Token(object):
                boolean = False

            return Token

def splicing():
    tableData = read(SPREADSHEET_ID, RANGE_NAME)
    print('data is shown in order of the table - row numbers on the left, column starting from A-Z - if greater than  26, A2+ \n')
    for row in tableData:
        print(tableData.index(row) + 1, ':', row)

    beginning = raw_input('what\'s the above row number?\n')
    end = raw_input('what\'s the bottom row number?\n')
    #need to move items around 
    make = raw_input('what make?\n')
    model = raw_input('what model?\n')
    cost = raw_input('what price point?\n')
    print(beginning)
    print(end)
    print(make)
    print(model)
    print(cost)

    checkpoint = raw_input('Is this information correct? (yes/no) \n')

    if checkpoint == 'yes':
        #create object to hold our information and check boolean 
        class Token(object):
            inputMake = make
            inputModel = model
            inputCost = cost
            boolean = True

        return Token
    else: 
        class Token(object):
            boolean = False

        return Token

def determineRange(integer, row): 
    alphabet = ['a','b','c','d','e','f','g', 'h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    concatValues = alphabet[0] + str(row) + ':' + alphabet[integer - 1] + str(row)
    return concatValues
 
def main():
    # Call the Sheets API
    credentials = obtain_credentials()
    print('Got the credentials without FAIL!')

    #prompt
    updatesheets = raw_input('do you want to update your sheet at this time? \n') #expecting yes or no 

    if updatesheets == 'yes':
        answer = updateSheets()
        
        if answer.boolean == True:
            # append(answer)
            write(answer)
        elif answer.boolean == False: 
            updateSheets()
        elif answer.boolean == 'skipped':
            print('No changes were made to any rows and no updates were made')


        startNew = raw_input('do you want to start inputting from the top of the page or the bottom? (yes/no) \n')

        if startNew == 'yes':
            answer = position()

            if answer.boolean == True:
                append(answer) 
            elif answer.boolean == False:
                position()


        splice = raw_input('any specific cells shift down and add a line? \n') 

        if splice == 'yes': 
            answer = splicing()

            if answer.boolean == True:
                #invoke write functions
                print(answer.boolean, answer.inputMake, answer.inputModel, answer.inputCost)
            elif answer.boolean == False:
                splicing()

        delete = raw_input('do you want to delete any data? \n')

        if delete == 'yes': 
            row = raw_input('what row do you want to delete? \n')
            clear(int(row))
        else:
            print('nothing will be deleted at this time')


#Refactor to take user input and also to get credential one time and make it reuseable 

if __name__ == '__main__':
    main()

