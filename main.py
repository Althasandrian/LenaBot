from __future__ import print_function
import pickle
import os.path
import os
import discord
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from discord.ext import commands, tasks
from itertools import cycle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Get vars from file
with open('credentials.json', 'rb') as json_file:
    data = json.load(json_file)
    DISCORD_TOKEN = data.get('discord').get('token')
    MARKET_SPREADSHEET_ID = data.get('spreadsheets').get('market_sheet_id')
    ORE_RANGE = data.get('spreadsheets').get('ore_range')
    MINERAL_RANGE = data.get('spreadsheets').get('mineral_range')
    PLANETARY_RANGE = data.get('spreadsheets').get('planetary_range')
    SALVAGE_RANGE = data.get('spreadsheets').get('salvage_range')
    ORE_MARKET_RANGE = data.get('spreadsheets').get('ore_range')
    MINERAL_MARKET_RANGE = data.get('spreadsheets').get('mineral_market_range')
    PLANETARY_MARKET_RANGE = data.get('spreadsheets').get('planetary_market_range')
    SALVAGE_MARKET_RANGE = data.get('spreadsheets').get('salvage_market_range')

bot = commands.Bot(command_prefix='$')

def main():
    bot.run(DISCORD_TOKEN)

## Bot functions

@bot.event
async def on_ready():
    print("LenaBot has connected to Discord")

#@tasks.loop(minutes=10)
#async def updateStandings():
#    await ctx.send("asd")

@bot.command(name='prices')
async def prices(ctx):
    data = fetchSheetsData(MARKET_SPREADSHEET_ID, ORE_RANGE)
    response = 'Purchasing all ore at following prices. Contract any amount to **Lena70 Xiahou** at the listed Buy Order Price in **Berta, Maspah or Camal.**\n'
    for row in data:
        response = response + '{} {} \n'.format(row[0], row[3])
    await ctx.send(response)

@bot.command(name='ore-market-prices')
async def oreMarketPrices(ctx):
    data = fetchSheetsData(MARKET_SPREADSHEET_ID, ORE_MARKET_RANGE)
    response = 'List of current market prices for ores.\n'
    for row in data:
        response = response + '{} {} \n'.format(row[0], row[1])
    await ctx.send(response)

@bot.command(name='mineral-market-prices')
async def mineralMarketPrices(ctx):
    data = fetchSheetsData(MARKET_SPREADSHEET_ID, MINERAL_MARKET_RANGE)
    response = 'List of current market prices for minerals.\n'
    for row in data:
        response = response + '{} {} \n'.format(row[0], row[1])
    await ctx.send(response)

@bot.command(name='planetary-market-prices')
async def planetaryMarketPrices(ctx):
    data = fetchSheetsData(MARKET_SPREADSHEET_ID, PLANETARY_MARKET_RANGE)
    response = 'List of current market prices for planetary products.\n'
    for row in data:
        response = response + '{} {} \n'.format(row[0], row[1])
    await ctx.send(response)

@bot.command(name='salvage-market-prices')
async def salvageMarketPrices(ctx):
    data = fetchSheetsData(MARKET_SPREADSHEET_ID, SALVAGE_MARKET_RANGE)
    response = 'List of current market prices for salvaged materials.\n'
    for row in data:
        response = response + '{} {} \n'.format(row[0], row[1])
    await ctx.send(response)

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