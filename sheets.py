from __future__ import print_function
import pickle
import os.path
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def main():
    print("This is not main.py")

## Sheets functions

#Construct authentication and the service for sheets.
def getSheetsService():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('sheets', 'v4', credentials=creds)

# Get data from sheets
def fetchSheetsData(sheets_id, range):
    service = getSheetsService()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheets_id, range=range).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        return values

#main is main
if __name__ == '__main__':
    main()
    