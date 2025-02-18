import discord
import openai
import os
import random
import asyncio
import datetime
from dotenv import load_dotenv
from memory import add_to_memory, search_memory
from knowledge import load_knowledge, search_knowledge
from simplifier import make_more_human

load_dotenv()
USER_TOKEN = os.getenv("DISCORD_USER_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALLOWED_CHANNEL_ID = int(os.getenv("ALLOWED_CHANNEL_ID", "123456789012345678"))
START_HOUR = int(os.getenv("START_HOUR", "10"))
END_HOUR = int(os.getenv("END_HOUR", "22"))

openai.api_key = OPENAI_API_KEY
intents = discord.Intents.default()
client = discord.Client(intents=intents, self_bot=True)

def is_within_active_hours():
    now = datetime.datetime.now().time()
    return datetime.time(START_HOUR, 0) <= now <= datetime.time(END_HOUR, 0)

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.id != ALLOWED_CHANNEL_ID or not is_within_active_hours():
        return

    memory_results = search_memory(message.content)
    knowledge_results = search_knowledge(message.content)
    context = "\n".join(memory_results + knowledge_results)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Ты говоришь просто."},
                  {"role": "user", "content": context + "\n" + message.content}]
    )

    reply = make_more_human(response["choices"][0]["message"]["content"])
    add_to_memory(message.content)

    await asyncio.sleep(random.uniform(2, 6))
    await message.channel.send(reply)

client.run(USER_TOKEN, bot=False)
