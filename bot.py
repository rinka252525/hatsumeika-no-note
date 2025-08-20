import discord
from discord.ext import commands
import os

# Bot設定
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.dm_messages = True
intents.guilds = True
intents.members = True  # on_member_join に必要
bot = commands.Bot(command_prefix="!", intents=intents)

# 正解リスト
answers = {
    "puzzle1": ["order"],  
    "puzzle2": ["ゾンネンボルフ博物館・天文台"],  
    "puzzle3": ["telescope", "望遠鏡"],  
    "puzzle4": ["Clairvoyant"],
}

# 進行状況をユーザーごとに記録
user_progress = {}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


# Botが新しいサーバーに参加したとき
@bot.event
async def on_guild_join(guild):
    # サーバーの最初のテキストチャンネルを探す
    channel = None
    for ch in guild.text_channels:
        if ch.permissions_for(guild.me).send_messages:
            channel = ch
            break
    
    if channel:
        await channel.send("こんにちは！招待ありがとう。準備ができました✨")


# スタートコマンドで謎1を送信
@bot.command()
async def start(ctx):
    user_progress[ctx.author.id] = "puzzle1"
    await ctx.send("「まずは並べ替えからお願いします」")
    await ctx.send(file=discord.File("puzzle1.png"))


# 回答チェック（キーワードで進む）
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = message.author.id
    progress = user_progress.get(user_id)

    if progress:
        possible_answers = answers.get(progress, [])
        if message.content.strip().lower() in [a.lower() for a in possible_answers]:
            await message.channel.send("✅ 正解！")

            if progress == "puzzle1":
                user_progress[user_id] = "puzzle2"
                await message.channel.send("「次の謎はこちら！」")
                await message.channel.send(file=discord.File("puzzle2-1.png"))

            elif progress == "puzzle2":
                user_progress[user_id] = "puzzle3"
                await message.channel.send("「部品が揃った！これは何になる？」")
                await message.channel.send(file=discord.File("puzzle3-1.png"))

            elif progress == "puzzle3":
                user_progress[user_id] = "puzzle4"
                await message.channel.send("「完成した！次の謎はこちら！」")
                await message.channel.send(file=discord.File("puzzle4.png"))

            elif progress == "puzzle4":
                user_progress[user_id] = "ending"
                await message.channel.send("「あなたがたはどうしたいですか？」")
                await message.channel.send("A：発明品を世に広める B：封印する C：独占する")
        else:
            await message.channel.send("❌ 不正解です。")

    # 他のコマンドも動くように必要
    await bot.process_commands(message)


# 実行
bot.run(os.getenv("DISCORD_TOKEN"))
