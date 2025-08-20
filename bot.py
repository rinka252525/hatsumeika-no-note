import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 正解リスト
answers = {
    "puzzle1": ["order"],  
    "puzzle2": ["ゾンネンボルフ博物館・天文台"],  
    "puzzle3": ["telescope", "望遠鏡"],  # 複数回答OK
    "puzzle4": ["Clairvoyant"],
}

# 進行状況をユーザーごとに記録
user_progress = {}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# スタートコマンドで謎1を送信
@bot.command()
async def start(ctx):
    user_progress[ctx.author.id] = "puzzle1"
    await ctx.send("「こんにちは！博士の設計図を解読してほしいんだ！」")
    await ctx.send("「まずは並べ替えからお願いします」")
    await ctx.send(file=discord.File("puzzle1.png"))


# メッセージから回答を判定する
@bot.event
async def on_message(message):
    # Botのメッセージは無視
    if message.author.bot:
        return

    user_id = message.author.id
    progress = user_progress.get(user_id)

    if progress:  # 進行中の謎がある場合
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
            # 不正解でも反応は返す
            await message.channel.send("❌ 不正解です。")

    # コマンドも使えるようにする
    await bot.process_commands(message)


# 実行
bot.run(os.getenv("DISCORD_TOKEN"))
