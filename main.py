from __future__ import print_function
import os.path
import os
import discord
import json
from discord.ext import commands, tasks
from itertools import cycle
from sheets import fetchSheetsData

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

#main is main
if __name__ == '__main__':
    main()