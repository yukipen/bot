#-*- -*- -*- -*- -*- -*- -*- -*- coding:UTF-8 -*- -*- -*- -*- -*- -*- -*- -*- -
import discord
#-*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*
client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')


@client.event
async def on_voice_state_update(member, before, after):
    if member.guild.id == 839373430263906304:
        text_ch = client.get_channel(1152889779181068369)
        if before.channel is None:
            msg = f'{member.name} が {after.channel.name} に参加しました。'
            await text_ch.send(msg)

'''
botのトークン
'''
client.run("MTE1Mjg4NTkyMDMwMzk0Nzg4Ng.GpKsUN.CO2Cis6zP6JmZzCv7pGFcraH0hnQW_PZKwTAxk")
