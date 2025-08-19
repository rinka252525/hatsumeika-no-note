import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 正解リスト
answers = {
    "puzzle1": "order",  # !answer order が正解
    "puzzle2": "ゾンネンボルフ博物館・天文台", # 謎2の答え
    "puzzle3": "telescope"," 望遠鏡",
    "puzzle4": "Clairvoyant",
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
    await ctx.send("「こんにちは！僕は普段機械の開発研究をしているんだけど博士の設計図を解読できず、解読班である君たちにお願いしたいと思って連絡させていただきました。」")
    await ctx.send("「博士のごちゃごちゃの部屋で管理していたので順番がばらばらになってしまいました。まずは並べ替えからお願いします。それぞれの紙にこんなマークがあるので、これが順番を表していると思うのですが…」")
    await ctx.send(file=discord.File("puzzle1.png"))

# 解答コマンド
@bot.command()
async def answer1(ctx, *, user_answer: str):
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
            await ctx.send("「わあ！たしかにこの順番のようです！」")
            await ctx.send("「あれ、でも、博士はいらずら好きだったので大切な部品を隠したみたいです。どこに隠したかわかりますか？」")
            await ctx.send(file=discord.File("puzzle2-1.png"))
            await ctx.send(file=discord.File("puzzle2-2.png"))
            await ctx.send(file=discord.File("puzzle2-3.png"))
            await ctx.send(file=discord.File("puzzle2-4.png"))

    else:
        await ctx.send("❌ 不正解です。もう一度挑戦してみてください。")


@bot.command()
async def answer2(ctx, *, user_answer: str):
    progress = user_progress.get(ctx.author.id)

    if not progress:
        await ctx.send("⚠️ まずは `!start` でゲームを始めてください。")
        return

    correct_answer = answers.get(progress)

    if user_answer.lower() == correct_answer.lower():
        await ctx.send("「なんと！近くにいるので探してみます！」")
        await ctx.send(file=discord.File("dig.png"))
        await ctx.send("「・・・ありました！」")

        if progress == "puzzle2":
            # 次の謎へ
            user_progress[ctx.author.id] = "puzzle3"
            await ctx.send("「部品が揃ったので組み立てたいと思います。完成品は何になりそうですか？」")
            await ctx.send(file=discord.File("puzzle3-1.png"))
            await ctx.send(file=discord.File("puzzle3-3.png"))

    else:
        await ctx.send("❌ 不正解です。もう一度挑戦してみてください。")


@bot.command()
async def answer3(ctx, *, user_answer: str):
    progress = user_progress.get(ctx.author.id)

    if not progress:
        await ctx.send("⚠️ まずは `!start` でゲームを始めてください。")
        return

    correct_answer = answers.get(progress)

    if user_answer.lower() == correct_answer.lower():
        await ctx.send("「すごい！本当に完成したんですね。折角なので覗いてみてください。」")
        await ctx.send("そう言って彼は望遠鏡をさしだす。街の灯り、星の瞬き、すべてがある色で染まっていく。")

        if progress == "puzzle3":
            # 次の謎へ
            user_progress[ctx.author.id] = "puzzle4"
            await ctx.send("次の謎はこちらです👇")
            await ctx.send(file=discord.File("puzzle4.mp3"))
            await ctx.send(file=discord.File("puzzle4.png"))
            
    else:
        await ctx.send("❌ 不正解です。もう一度挑戦してみてください。")




@bot.command()
async def answer4(ctx, *, user_answer: str):
    progress = user_progress.get(ctx.author.id)

    if not progress:
        await ctx.send("⚠️ まずは `!start` でゲームを始めてください。")
        return

    correct_answer = answers.get(progress)

    if user_answer.lower() == correct_answer.lower():
        await ctx.send("「ええ！？望遠鏡で見ると違った世界が見える…あ、これ設計書によると未来が見える望遠鏡のようですね。」")
        await ctx.send("「未来で何があるんだろう…」")

        if progress == "puzzle4":
            # 次の謎へ
            user_progress[ctx.author.id] = "ending"
            await ctx.send("「あなたがたはどうしたいですか？」")
            await ctx.send("A：発明品を世に広める B：封印する C：自分たちで独占する")

    else:
        await ctx.send("❌ 不正解です。もう一度挑戦してみてください。")



@bot.command()
async def end(ctx, *, user_answer: str):
    progress = user_progress.get(ctx.author.id)

    if not progress:
        await ctx.send("⚠️ まずは `!start` でゲームを始めてください。")
        return

    correct_answer = answers.get(progress)

    if user_answer.lower() == correct_answer.lower():
        await ctx.send("「ええ！？望遠鏡で見ると違った世界が見える…あ、これ設計書によると未来が見える望遠鏡のようですね。」")
        await ctx.send("「未来で何があるんだろう…」")

        if progress == "puzzle4":
            # 次の謎へ
            user_progress[ctx.author.id] = "ending"
            await ctx.send("「あなたがたはどうしたいですか？」")
            await ctx.send("A：発明品を世に広める B：封印する C：自分たちで独占する")

    else:
        await ctx.send("❌ 不正解です。もう一度挑戦してみてください。")
# 実行
bot.run(os.getenv("DISCORD_TOKEN"))

