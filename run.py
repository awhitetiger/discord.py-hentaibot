import discord
import asyncio
import random
import requests
import json
import math
import urllib.request
import os
from pixivpy3 import *

client = discord.Client()
api = AppPixivAPI()
api.login("username","password")

@client.event
async def on_ready():
	print('HentaiBot Online')

@client.event
async def on_message(message):
	if message.content[:23] == 'https://exhentai.org/g/' or message.content[:23] == 'https://e-hentai.org/g/' and message.author.id != client.user.id:
		await client.delete_message(message)
		await gallery_details(message.content[23:], message.channel.id)
		await client.send_message(message.channel, '```' + message.content + '```')
	if message.content[:40] == 'https://www.pixiv.net/member_illust.php?':
		await client.delete_message(message)
		await gallery_details_p(message.content[40:], message.channel.id)
		await client.send_message(message.channel, '```' + message.content + '```')

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

async def gallery_details_p(id, channel):
	split = id.find("&illust_id=")
	size = id[5:split]
	illust_id = id[split+11:]
	galleryInfo = api.illust_detail(int(illust_id),req_auth=True)
	illust_url = galleryInfo.illust
	api.download(illust_url.image_urls[size], name="pixiv_" +str(illust_id)+ ".png")
	await client.send_file(discord.Object(id=channel), "pixiv_" +str(illust_id)+'.png')
	os.remove("pixiv_" +str(illust_id)+'.png')

client.run('discord bot api key here')
