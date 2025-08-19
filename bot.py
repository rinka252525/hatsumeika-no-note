import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 正解リスト
answers = {
    "puzzle1": "order",  # !answer order が正解
    "puzzle2": "future", # 例：謎2の答え
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
    await ctx.send("「こんにちは！僕は普段機械の開発研究をしているんだけど師匠の設計図を解読できず、解読班である君たちにお願いしたいと思って連絡させてもらったんだ。」")
    await ctx.send("「博士のごちゃごちゃの部屋で管理していたので順番がばらばらになってしまいました。まずは並べ替えからお願いします。それぞれの紙にこんなマークがあるので、これが順番を表していると思うのですが…」")
    await ctx.send(file=discord.File("puzzle1.png"))

# 解答コマンド
@bot.command()
async def answer(ctx, *, user_answer: str):
    progress = user_progress.get(ctx.author.id)

    if not progress:
        await ctx.send("⚠️ まずは `!start` でゲームを始めてください。")
        return

    correct_answer = answers.get(progress)

    if user_answer.lower() == correct_answer.lower():
        await ctx.send("✅ 正解！")

        if progress == "puzzle1":
            # 次の謎へ
            user_progress[ctx.author.id] = "puzzle2"
            await ctx.send("次の謎はこちらです👇")
            await ctx.send(file=discord.File("puzzle2.png"))

        elif progress == "puzzle2":
            await ctx.send("🎉 全問正解！おめでとうございます！")

    else:
        await ctx.send("❌ 不正解です。もう一度挑戦してみてください。")

# 実行
bot.run(os.getenv("DISCORD_TOKEN"))

