from discord.ext import commands
from dotenv import load_dotenv
from epicstore_api import EpicGamesStoreAPI, OfferData
import datetime, discord, json, os, random

load_dotenv()
bot = commands.Bot(command_prefix='!')

class FreeGame:
    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])

@bot.command()
async def egs(ctx):
    api = EpicGamesStoreAPI(country='AU')
    dict = api.get_free_games()
        
    elements = dict['data']['Catalog']['searchStore']['elements']
    free_games = []
    for element in elements:
        free_game = FreeGame(element)
        if not free_game.seller['name'] == 'Epic Dev Test Account': # remove developer related products
            free_games.append(free_game)
    await embed_games(ctx, free_games)

async def embed_games(ctx, free_games):
    today = datetime.date.today()
    if today.weekday() == 4:
        today += datetime.timedelta(1)
    friday = today + datetime.timedelta((4 - today.weekday()) % 7)
    format = 'day' if (friday - today).days == 1 else 'days'
    
    embed = discord.Embed(title='Epic Games Store | Free Games', description=f'Available for another {(friday - today).days} {format}', color=discord.Color.blurple())
    embed.set_image(url='https://static-assets-prod.epicgames.com/epic-store/static/webpack/../favicon.ico')
    for free_game in free_games:
        url = '' if free_game.url is None else f'[Link]({free_game.url})\n'
        name = free_game.seller['name']
        price = free_game.price['totalPrice']['fmtPrice']['originalPrice']
        
        embed.add_field(name=free_game.title, value=url + f'by *{name}*, **~~{price}~~**' + '\n' + free_game.description[:140] + (free_game.description[140:] and '...'), inline=random.choice([True, True, False]))
        
    await ctx.send(embed=embed)

bot.run(os.getenv('DISCORD_TOKEN'))