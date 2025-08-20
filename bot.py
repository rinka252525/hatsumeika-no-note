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
        await channel.send("「こんにちは！僕は普段機械の開発研究をしているんだけど博士の設計図を解読できず、解読班である君たちにお願いしたいと思って連絡させてもらったんだ。\n"
                           "準備が出来たら `!start` で教えてね！")
        

# スタートコマンドで謎1を送信
@bot.command()
async def start(ctx):
    user_progress[ctx.author.id] = "puzzle1"
    await ctx.send("「博士のごちゃごちゃの部屋で管理していたので順番がばらばらになっちゃったんだ。\n"
                   "まずは並べ替えからお願いしていいかな？それぞれの紙にこんな丸があるから、これが順番を表していると思うんだけど…」")
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
            await message.channel.send("「わあありがとう！たしかにこの順番みたいだ！」")

            if progress == "puzzle1":
                user_progress[user_id] = "puzzle2"
                await message.channel.send("「でも、博士はいらずら好きだったから大切な部品を隠しちゃったんだ。どこに隠したかわかる？」")
                await message.channel.send(file=discord.File("puzzle2-1.png","puzzle2-2.png","puzzle2-3.png","puzzle2-4.png"))

            elif progress == "puzzle2":
                user_progress[user_id] = "puzzle3"
                await message.channel.send("「部品が揃った！完成品は何になる？」")
                await message.channel.send(file=discord.File("puzzle3.png"))

            elif progress == "puzzle3":
                user_progress[user_id] = "puzzle4"
                await message.channel.send("「すごい！なるほど、望遠鏡だったのか！折角なので覗いてみてください！」/n"
                                          "「この望遠鏡は肉眼じゃなくても君たちのPCから見れるようにしたよ。」")
                await message.channel.send("そう言って彼は望遠鏡をさしだす。街の灯り、星の瞬き、すべてがある色で染まっていく。")
                await message.channel.send(file=discord.File("puzzle4.png"))
                await message.channel.send(file=discord.File("puzzle4.mp3"))

            elif progress == "puzzle4":
                user_progress[user_id] = "ending"
                await message.channel.send("「ええ！？望遠鏡で見ると違った世界が見える…あ、これ設計書によると未来が見える望遠鏡のようですね。」/n"
                                           "「未来で何があるんだろう…」")
                await message.channel.send("'!ending' A：発明品を世に広める B：封印する C：独占する")
        else:
            await message.channel.send("❌ 不正解です。")


    # 他のコマンドも動くように必要
    await bot.process_commands(message)

@bot.command()
async def ending(ctx, choice: str):
    choice = choice.upper()

    if choice == "A":
        file = discord.File("ending_A.png", filename="ending_A.png")
        await ctx.send("✨祝福のメッセージ✨", file=file)

    elif choice == "B":
        file = discord.File("ending_B.png", filename="ending_B.png")
        await ctx.send("📓暗転したノートの表紙が現れた…", file=file)

    elif choice == "C":
        file = discord.File("ending_C.png", filename="ending_C.png")
        await ctx.send("📜怪しい契約書が差し出された…", file=file)

    else:
        await ctx.send("選択肢は A / B / C から選んでください！")


# 実行
bot.run(os.getenv("DISCORD_TOKEN"))
