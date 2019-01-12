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
RANGE_NAME = 'A1:K4'

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

def write(make, model, price, row, row2, position): 
    credentials = obtain_credentials()
    service = build('sheets', 'v4', http=credentials.authorize(Http()))
    values = [
        [
            make, model, price
        ],
    ]

    Body = {
    'values' : values,
    }

    result = service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id, range=range_name,
    valueInputOption='RAW', body=Body).execute()

    print("Writing OK!!")

def read(spreadsheet_id, range_name): 
    credentials = obtain_credentials()
    service = build('sheets', 'v4', http=credentials.authorize(Http()))

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=range_name).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        return values

def updateSheets():
    replace = raw_input('do you want to replace any cells on the spreadsheet?')

    if replace == 'yes':
        cellData = read(SPREADSHEET_ID, RANGE_NAME)
        print('data is shown in order of the table - row numbers on the left, column starting from A-Z - if greater than  26, A2+ ')
        for row in cellData:
            print(cellData.index(row) + 1, ':', row)
        row = raw_input('what row do you want to update?')
        make = raw_input('what make?')
        model = raw_input('what model?')
        cost = raw_input('what price point?')

        print('row: ', row)
        print('make: ', make)
        print('model: ', model)
        print('cost: ', cost)

        checkpoint = raw_input('Is this information correct?')

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
    top = raw_input('top or bottom?')

    tableData = read(SPREADSHEET_ID, RANGE_NAME)
    print('data is shown in order of the table - row numbers on the left, column starting from A-Z - if greater than  26, A2+ ')
    for row in tableData:
        print(tableData.index(row) + 1, ':', row)

    if top == 'top':
        rowStart = 0 #index is 0, but the row is 1
        #need to get cell info from main()
        make = raw_input('what make?')
        model = raw_input('what model?')
        cost = raw_input('what price point?')

        print('make: ', make)
        print('model: ', model)
        print('cost: ', cost)

        checkpoint = raw_input('Is this information correct? (yes/no) ')

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
        make = raw_input('what make?')
        model = raw_input('what model?')
        cost = raw_input('what price point?')

        print('make: ', make)
        print('model: ', model)
        print('cost: ', cost)

        checkpoint = raw_input('Is this information correct? (yes/no) ')

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
    print('data is shown in order of the table - row numbers on the left, column starting from A-Z - if greater than  26, A2+ ')
    for row in tableData:
        print(tableData.index(row) + 1, ':', row)

    beginning = raw_input('what\'s the above row number?')
    end = raw_input('what\'s the bottom row number?')
    #need to move items around 
    make = raw_input('what make?')
    model = raw_input('what model?')
    cost = raw_input('what price point?')
    print(beginning)
    print(end)
    print(make)
    print(model)
    print(cost)

    checkpoint = raw_input('Is this information correct? (yes/no) ')

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
 
def main(spreadsheet_id, range_name):
    # Call the Sheets API
    credentials = obtain_credentials()
    print('Got the credentials without FAIL!')

    #prompt
    updatesheets = raw_input('do you want to update your sheet at this time?') #expecting yes or no 

    if updatesheets == 'yes':
        answer = updateSheets()
        
        if answer.boolean == True:
            #invoke write func
            print(answer.boolean, answer.inputRow, answer.inputMake, answer.inputModel, answer.inputCost)
        elif answer.boolean == False: 
            updateSheets()
        elif answer.boolean == 'skipped':
            print('No changes were made to any rows and no updates were made')


        startNew = raw_input('do you want to start inputting from the top of the page or the bottom? (yes/no)')

        if startNew == 'yes':
            answer = position()

            if answer.boolean == True:
                #invoke write functions
                print(answer.boolean, answer.inputMake, answer.inputModel, answer.inputCost)
            elif answer.boolean == False:
                position()


        splice = raw_input('any specific cells shift down and add a line?') 

        if splice == 'yes': 
            answer = splicing()

            if answer.boolean == True:
                #invoke write functions
                print(answer.boolean, answer.inputMake, answer.inputModel, answer.inputCost)
            elif answer.boolean == False:
                splicing()

        delete = raw_input('do you want to delete any data?')

        if delete == 'yes': 
            row = raw_input('what row do you want to delete?')
            print(row)
            #write new func for this
        else:
            print('nothing will be deleted at this time')


#Refactor to take user input and also to get credential one time and make it reuseable 

if __name__ == '__main__':
    main(SPREADSHEET_ID, RANGE_NAME)
    # write(SPREADSHEET_ID, RANGE_NAME)
