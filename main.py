from __future__ import print_function
import pickle
import os.path
import os
import discord
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from discord.ext import commands

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Get vars from file
with open('credentials.json', 'rb') as json_file:
    data = json.load(json_file)
    DISCORD_TOKEN = data.get('discord').get('token')
    SPREADSHEET_ID = data.get('spreadsheets').get('sheet_id')
    ORE_RANGE = data.get('spreadsheets').get('ore_range')

bot = commands.Bot(command_prefix='$')

def main():
    bot.run(DISCORD_TOKEN)

@bot.event
async def on_ready():
    print("LenaBot has connected to Discord")

@bot.command(name='prices')
async def prices(ctx):
    data = updatePrices()

    response = 'Purchasing all ore at following prices. Contract any amount to Lena70 Xiahou at the listed Buy Order Price in Berta, Maspah or Camal.\n\
{} {} \n{} {} \n{} {} \n{} {} \n\
{} {} \n{} {} \n{} {} \n{} {} \n\
{} {} \n{} {} \n{} {} \n{} {} \n\
{} {} \n{} {} \n{} {} \n{} {} \n'.format(\
data[0][0], data[0][3], data[1][0], data[1][3], data[2][0], data[2][3], data[3][0], data[3][3],\
data[4][0], data[4][3], data[5][0], data[5][3], data[6][0], data[6][3], data[7][0], data[7][3],\
data[8][0], data[8][3], data[9][0], data[9][3], data[10][0], data[10][3], data[11][0], data[11][3],\
data[12][0], data[12][3], data[13][0], data[13][3], data[14][0], data[14][3], data[15][0], data[15][3])
    await ctx.send(response)

def formatPrices(data):
    result = data
    return result

def updatePrices():
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

    service = build('sheets', 'v4', credentials=creds)
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=ORE_RANGE).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        return values

if __name__ == '__main__':
    main()