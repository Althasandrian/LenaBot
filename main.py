from __future__ import print_function
import os.path
import os
import discord
import json
import math
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
    EVE_ECHOES_MARKET_DUMP_RANGE = data.get('spreadsheets').get('eve_echoes_market_dump')
    ORE_REPROCESSING_RANGE = data.get('spreadsheets').get('ore_reprosessing_range')

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

@bot.command(name='reprocess')
async def checkReprocess(ctx):
    msg = ctx.message.content
    data = fetchSheetsData(MARKET_SPREADSHEET_ID, ORE_REPROCESSING_RANGE)
    ore = msg.split(" ", 2)
    amount = int(math.floor(float(ore[2])/100))
    for row in data:
        if row[0].lower() == ore[1].lower():
            response = "Reprocessing {} {} yields:\n".format(amount * 100, row[0])
            if len(row) >= 3:
                if row[2] != "":
                    response = response + "Tritanium: {}\n".format(amount * float(row[2]))
            if len(row) >= 4:
                if row[3] != "":
                    response = response + "Pyerite: {}\n".format(amount * float(row[3]))
            if len(row) >= 5:
                if row[4] != "":
                    response = response + "Mexallon: {}\n".format(amount * float(row[4]))
            if len(row) >= 6:
                if row[5] != "":
                    response = response + "Isogen: {}\n".format(amount * float(row[5]))
            if len(row) >= 7:
                if row[6] != "":
                    response = response + "Nocxium: {}\n".format(amount * float(row[6]))
            if len(row) >= 8:
                if row[7] != "":
                    response = response + "Zydrine: {}\n".format(amount * float(row[7]))
            if len(row) >= 9:
                if row[8] != "":
                    response = response + "Megacyte: {}\n".format(amount * float(row[8]))
            if len(row) >= 10:
                if row[9] != "":
                    response = response + "Morphite: {}\n".format(amount * float(row[9]))
            break
        else:
            response = "Queried item not found."
    await ctx.send(response)

@bot.command(name='check')
async def checkPrice(ctx):
    msg = ctx.message.content
    data = fetchSheetsData(MARKET_SPREADSHEET_ID, EVE_ECHOES_MARKET_DUMP_RANGE)
    query = msg.split(" ", 1)
    for row in data:
        if row[1].lower() == query[1].lower():
            response = '{}\n Sell: {}\n Buy: {}'.format(row[1], row[3], row[4])
            break
        else:
            response = "Queried item not found."
    await ctx.send(response)

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