import discord
import json
import os

from pathlib import Path
from discord.ext import commands

cwd = Path(__file__).parents[0]
cwd = str(cwd)

def read_json(file_name):
    with open(f'/root/KeroBot/config/{file_name}.json', 'r') as file:
        data = json.load(file)
    return data

def write_json(file_name, data):
    with open(f'/root/KeroBot/config/{file_name}.json', 'w') as file:
        json.dump(data,file,indent=4)
    return data

def get_avatar(user, animate=True):
    if user.avatar_url:
        avatar = str(user.avatar_url).replace(".webp", ".png")
    else:
        avatar = str(user.default_avatar_url)
    if not animate:
        avatar = avatar.replace(".gif", ".png")
    return avatar