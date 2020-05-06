import os
import discord
from discord import Client
from typing import List

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

    def メンバ追加(self, メンバ名):
        self.集計カウント += 1
        self.参加者リスト.append(メンバ名)
        return True

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
        メンバー集計オブジェクト.メンバ追加(message.author)
        s: str = f"{message.author.name}さんの参加を確認しました"
        await message.channel.send(s)

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


async def 指定ロール付与関数(message, ロール名):
    global メンバー集計オブジェクト
    s = ""
    if 0 == メンバー集計オブジェクト.集計カウント:
        s = "参加者は0人です"
        await message.channel.send(s)
        return

    ロール = discord.utils.get(message.guild.roles, name=ロール名)
    for 参加者 in メンバー集計オブジェクト.参加者リスト:
        await 参加者.add_roles(ロール)
        s = 参加者.name + f"さんに役職{ロール名}を追加しました"
        await message.channel.send(s)


async def 指定ロール解除関数(message, ロール名):
    global メンバー集計オブジェクト
    s = ""

    ロール = discord.utils.get(message.guild.roles, name=ロール名)
    for 参加者 in message.guild.members:
        if ロール in 参加者.roles:
            await 参加者.remove_roles(ロール)
            s = 参加者.name + f"さんの役職{ロール名}を解除しました"
            await message.channel.send(s)


async def 秘匿チャンネル設定関数(message):
    global メンバー集計オブジェクト
    s: str = ""

    if 0 == メンバー集計オブジェクト.集計カウント:
        s = f"参加者は0人です"
        await message.channel.send(s)
        return

    print("番号を取得しつつforをまわす")
    for i, 参加者 in enumerate(メンバー集計オブジェクト.参加者リスト):
        print(f"{i=}")
        print(f"{参加者.name=}")
        ロール名 = "join0" + str(i)
        print(f"{ロール名}")
        ロール = discord.utils.get(message.guild.roles, name=ロール名)

        await 参加者.add_roles(ロール)
        s = 参加者.name + f"さんに役職{ロール名}を追加しました"
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
    elif "join付与" in message.content:
        await 指定ロール付与関数(message, "join-member")
    elif "join解除" in message.content:
        await 指定ロール解除関数(message, "join-member")
    elif "秘匿" in message.content:
        await 秘匿チャンネル設定関数(message)


# Botの起動とDiscordサーバーへの接続
if __name__ == '__main__':

    メンバー集計オブジェクト = メンバー集計クラス()

    # 自分のBotのアクセストークンに置き換えてください
    TOKEN: str = os.environ["DISCORD_API_TOKEN"]
    client.run(TOKEN)
