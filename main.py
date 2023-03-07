#-*- -*- -*- -*- -*- -*- -*- -*- coding:UTF-8 -*- -*- -*- -*- -*- -*- -*- -*- -
import discord
from discord import app_commands, Interaction, TextStyle
from discord.ui import TextInput, View, Modal
import os
#-*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])
CHECK_GUILD = int(os.environ["CHECK_GUILD"])
OPENAI_API = os.environ["OPENAI_TOKEN"]

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.typing = False

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)
set_guild = discord.Object(CHECK_GUILD)

# スラッシュコマンドを使えるサーバー列挙
notifyGuilds = [CHECK_GUILD]
set_member = None


@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="ver2.0.3"))
    await tree.sync()

# 役職を追加する
@tree.command(
    name = 'add_role',
    description = '通知される役職に登録します。'
)
async def add_role(inter):
    role = discord.utils.get(inter.guild.roles, name="notify") # サーバー内の「ロール名」というロールを取得
    member = inter.author
    await member.add_roles(role) # 上記で取得したロールを付与
    await inter.reply('役職を追加しました')


class Questionnaire(Modal):
    def __init__(self, title: str) -> None:
        super().__init__(title=title)
        self.answer = TextInput(label="質問を入力してください", style=TextStyle.long)
        self.add_item(self.answer)

    async def on_submit(self, interaction: Interaction) -> None:
        import openai
        openai.api_key = OPENAI_API

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{'role': 'user', 'content': self.answer.value}],
            temperature=0.0,
        )
        print(response['choices'][0]['message']['content'])
        msg = discord.Embed(title="Response", description=response['choices'][0]['message']['content'], colour=0x1e90ff)
        await interaction.response.send_message(embeds=msg, components=[LinkButton("ChatGPTより", "https://chat.openai.com/chat")])

@tree.command(
    name = 'chat',
    description = 'ChatGPTへ質問ができます',
)
async def chat(inter):
    modal = Questionnaire("ChatGPTへの質問")
    await inter.response.send_modal(modal)

# ボイスチャンネルのステータスが更新
@bot.event
async def on_voice_state_update(member, before, after):
    global set_member
    if member.guild.id == CHECK_GUILD and (before.channel != after.channel):
        alert_channel = bot.get_channel(CHANNEL_ID) # alertChannnel
        if before.channel is None:
            if after.channel.members is not None:
                if not set_member is member:
                    set_member = member
                    role = discord.utils.get(member.guild.roles, name="notify")
                    msg = f'{role.mention} {member.display_name} が {after.channel.name} に参加しました。'
                    await alert_channel.send(msg)


bot.run(DISCORD_TOKEN)