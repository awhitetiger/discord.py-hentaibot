import discord
import asyncio
import random
import requests
import json
import math
import urllib.request
import os
import basc_py4chan
import sqlite3
from pixivpy3 import *

client = discord.Client()
conn = sqlite3.connect('bounties.db')
api = AppPixivAPI()
api.login("pixivid","pixivpassword")

@client.event
async def on_ready():
	print('HentaiBot Online')

@client.event
async def on_message(message):
	if message.channel.name != None and message.channel.name[:5] == 'nsfw-' and message.author.id != client.user.id:
		if message.content[:23] == 'https://exhentai.org/g/' or message.content[:23] == 'https://e-hentai.org/g/':
			await client.delete_message(message)
			await gallery_details(message.content[23:], message.channel.id)
			await client.send_message(message.channel, '```' + message.content + '```')
		if message.content[:40] == 'https://www.pixiv.net/member_illust.php?':
			await client.delete_message(message)
			await gallery_details_p(message.content[40:], message.channel.id)
			await client.send_message(message.channel, '```' + message.content + '```')
		if message.content[:3] == '!h_':
			await get_image_h(message.content[3:].lower(), message.channel.id)
		if message.content[:6] == '!sauce' and message.channel.name[5:] == 'sauce':
			if await user_check(message.author.id) == 1:
				await client.delete_message(message)
				await create_bounty(message.author.id, message.content[7:], message.channel.id)
		if message.content[:11] == '!give_sauce' and message.channel.name[5:] == 'sauce':
			split = message.content.find('http')
			await claim_bounty(message.content[12:split-1],message.content[split:],message.author.id,message.channel.id)
			await client.delete_message(message)
		if message.content[:9] == '!confirm_' and message.channel.name[5:] == 'sauce':
			await confirm_bounty(message.content[9:], message.channel.id, message.author.id)
			await client.delete_message(message)
#start of ehentai and exhentai
async def gallery_details(slug, channel):
	id = slug[:-12]
	token = slug[-12:][1:-1]
	await request_gallery(id, token, channel)

async def request_gallery(id, token, channel):
	post_data = {
		"method": "gdata", 
		"gidlist": [
			[int(id),token]
		],
		"namespace": 1}
	headers = {"Content-type": "application/json", "Accept": "text/plain"}
	galleryData = requests.post("https://api.e-hentai.org/api.php", data=json.dumps(post_data), headers=headers)
	galleryData = json.loads(galleryData.content)
	galleryData = await sort_gallery(galleryData)
	await send_gallery(galleryData, channel)

async def sort_gallery(galleryData):
#galleryInfo = [type, name, author, rating, pages, tags, parody, characters, thumb]
	galleryInfo = [galleryData["gmetadata"][0]["category"], galleryData["gmetadata"][0]["title"], [], galleryData["gmetadata"][0]["rating"], galleryData["gmetadata"][0]["filecount"], galleryData["gmetadata"][0]["tags"], 'n/a', [], galleryData["gmetadata"][0]["thumb"]]
	for x in range(len(galleryInfo[5])-1):
		if galleryInfo[5][x][:7] == 'artist:':
			galleryInfo[5][x] = galleryInfo[5][x][7:]
			galleryInfo[2].append(galleryInfo[5][x])
		elif galleryInfo[5][x][:7] == 'female:':
			galleryInfo[5][x] = galleryInfo[5][x][7:]
		elif galleryInfo[5][x][:5] == 'male:':
			galleryInfo[5][x] = galleryInfo[5][x][5:]
		elif galleryInfo[5][x][:7] == 'parody:':
			galleryInfo[5][x] = galleryInfo[5][x][7:]
			galleryInfo[6] = galleryInfo[5][x]
		elif galleryInfo[5][x][:10] == 'character:':
			galleryInfo[5][x] = galleryInfo[5][x][10:]
			galleryInfo[7].append(galleryInfo[5][x])
		elif galleryInfo[5][x][:6] == 'group:':
			galleryInfo[5][x] = galleryInfo[5][x][6:]
		elif galleryInfo[5][x][:9] == 'language:':
			galleryInfo[5][x] = galleryInfo[5][x][9:]
	galleryInfo[2] = ', '.join(galleryInfo[2])
	galleryInfo[5] = ', '.join(galleryInfo[5])
	galleryInfo[7] = ', '.join(galleryInfo[7])
	galleryInfo[3] = round(float(galleryInfo[3]))
	galleryInfo[3] = '★' * galleryInfo[3]
	return(galleryInfo)

async def send_gallery(galleryData, channel):
	gallery_info = galleryData
	urllib.request.urlretrieve(galleryData[8], "download.png")
	await client.send_file(discord.Object(id=channel), 'download.png')
	await client.send_message(discord.Object(id=channel), '```\nType: ' + gallery_info[0] + '\n\nName: ' + gallery_info[1] + '\n\nAuthor: ' + gallery_info[2] + '\n\nRating: ' + gallery_info[3] + '\n\nPages: ' + gallery_info[4] + '\n\nTags: ' + gallery_info[5] + '\n\nParody: ' + gallery_info[6] + '\n\nCharacters: ' + gallery_info[7] + '```')
	os.remove("download.png")
#end of e-hentai & exhentai
#pixiv get
async def gallery_details_p(id, channel):
	split = id.find("&illust_id=")
	size = id[5:split]
	illust_id = id[split+11:]
	galleryInfo = api.illust_detail(int(illust_id),req_auth=True)
	illust_url = galleryInfo.illust
	api.download(illust_url.image_urls[size], name="pixiv_" +str(illust_id)+ ".png")
	await client.send_file(discord.Object(id=channel), "pixiv_" +str(illust_id)+'.png')
	os.remove("pixiv_" +str(illust_id)+'.png')
#end of pixiv
#/h/ search
async def get_image_h(search, channel):
	board = basc_py4chan.Board('h')
	thread_ids = board.get_all_thread_ids()
	for x in range(len(thread_ids)):
		thread = board.get_thread(thread_ids[x])
		topic = thread.topic
		if topic.subject == None:
			if search in topic.comment.lower():
				image = random.choice(list(thread.file_objects())).file_url
				await client.send_message(discord.Object(id=channel), image)
				break
		else:
			if search in topic.subject.lower():
				image = random.choice(list(thread.file_objects())).file_url
				await client.send_message(discord.Object(id=channel), image)
				break
#end of /h/ search
#sauce bounty
async def user_check(id):
	c = conn.cursor()
	c.execute('SELECT * FROM users WHERE user_id=' + id)
	if c.fetchone() == None:
		c.execute('INSERT INTO users VALUES('+id+',0,0)')
		conn.commit()
		return(1)
	else:
		return(1)

async def create_bounty(id, image, channel):
	c = conn.cursor()
	bounty_id = c.execute('SELECT * FROM bounties')
	bounty_id = str(len(c.fetchall()))
	c.execute('INSERT INTO bounties VALUES('+bounty_id+','+id+','+id+')')
	conn.commit()
	await post_bounty(bounty_id, channel, id, image)

async def post_bounty(id, channel, user_id, image):
	poster = await client.get_user_info(user_id)
	await client.send_message(discord.Object(id=channel), image+'\n```\nSauce Bounty\n\nBounty ID: '+id+'```'+'Poster: '+poster.mention+'\n\nType !give_sauce '+id+' http://sauce to sauce this bounty!')

async def claim_bounty(bounty_id, sauce_url, id, channel):
	c = conn.cursor()
	c.execute('SELECT poster_id FROM bounties WHERE bounty_id='+bounty_id)
	notify_user = await client.get_user_info(c.fetchone()[0])
	sender = await client.get_user_info(id)
	c.execute('UPDATE bounties SET saucer='+id+' WHERE poster_id='+notify_user.id+'')
	conn.commit()
	await client.send_message(notify_user, sender.name+' has sauced your bounty!\nSauce: '+sauce_url+'\nType !confirm_'+bounty_id+' in the bounties channel if this is correct!')

async def confirm_bounty(bounty_id, channel, id):
	c = conn.cursor()
	c.execute("SELECT poster_id FROM bounties WHERE bounty_id="+bounty_id)
	poster = await client.get_user_info(c.fetchone()[0])
	c.execute("SELECT saucer FROM bounties WHERE bounty_id="+bounty_id)
	saucer = await client.get_user_info(c.fetchone()[0])
	if poster.id == id:
		async for message in client.logs_from(discord.Object(id=channel), limit=500):
			if '```\nSauce Bounty\n\nBounty ID: '+bounty_id+'```'+'Poster: '+poster.mention in message.content:
				await client.delete_message(message)
				await client.send_message(discord.Object(id=channel), saucer.mention+' just sauced '+poster.mention+'!')
				break
#end of bounty
client.run('discord bot api key here')
