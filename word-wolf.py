import os
from discord import Client
from typing import List

# 自分のBotのアクセストークンに置き換えてください
TOKEN: str = os.environ["DISCORD_API_TOKEN"]

# 接続に必要なオブジェクトを生成
client: Client = Client()


class メンバー集計クラス:
    集計カウント: int = 0
    参加者リスト: List = []
    集計フラグ: bool = False

    def __init__(self):
        print("メンバー集計クラスの__init__メソッド")
        self.集計カウント = 0
        self.参加者リスト = []
        self.集計フラグ = False

    def 集計中ですか(self):
        print(f"{self.集計フラグ=}")
        return self.集計フラグ


メンバー集計オブジェクト = メンバー集計クラス()


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print("ログインしました")


async def メンバー集計関数(message):
    global メンバー集計オブジェクト

    if メンバー集計オブジェクト.集計中ですか():
        s: str = f"現在集計中です"
        await message.channel.send(s)
        return

    # それぞれのプロパティを初期化
    メンバー集計オブジェクト.__init__()

    メンバー集計オブジェクト.集計フラグ = True
    channel = message.channel

    await channel.send(f"集計を開始します")
    await channel.send(f"現在の集計値：{メンバー集計オブジェクト.集計カウント}")

    def check(m):
        return "集計終了" in m.content and m.channel == channel

    msg = await client.wait_for("message", check=check)
    await channel.send(f"集計を終了しました".format(msg))
    print(f"集計を終了しました".format(msg))

    await channel.send(f"参加者リスト：")
    for 参加者 in メンバー集計オブジェクト.参加者リスト:
        await channel.send(参加者.name)

    メンバー集計オブジェクト.集計フラグ = False


async def メンバー参加関数(message):
    global メンバー集計オブジェクト

    if not メンバー集計オブジェクト.集計中ですか():
        s: str = f"現在集計しておりません"
        await message.channel.send(s)
    elif message.author in メンバー集計オブジェクト.参加者リスト:
        s: str = f"{message.author.name}さんは既に参加済みです"
        await message.channel.send(s)
        return
    else:
        s: str = f"{message.author.name}さんの参加を確認しました"
        await message.channel.send(s)
        メンバー集計オブジェクト.集計カウント += 1
        メンバー集計オブジェクト.参加者リスト.append(message.author)


async def メンバー一覧関数(message):
    global メンバー集計オブジェクト
    s: str = ""

    if 0 == メンバー集計オブジェクト.集計カウント:
        s = f"参加者は0人です"
        await message.channel.send(s)
        return

    s = f"参加者は"
    for 参加者 in メンバー集計オブジェクト.参加者リスト:
        s += "「" + 参加者.name + "さん」"
    s += "です"
    await message.channel.send(s)


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    global メンバー集計オブジェクト

    # botへのメンションのみで反応する
    if client.user not in message.mentions:
        return
    elif "集計開始" in message.content:
        await メンバー集計関数(message)
    elif "参加" in message.content:
        await メンバー参加関数(message)
    elif "一覧" in message.content:
        await メンバー一覧関数(message)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
