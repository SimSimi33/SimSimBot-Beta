import discord
from discord.ext import commands
from random import randint
import asyncio
import re
import requests
import random
import time
import os

client = commands.Bot(command_prefix = "ssb")

def moneyfix(user, moneyindex):
	fmoney = open("C:/SSBData/moneylist.txt", "r")
	line = fmoney.readlines()
	lines = 0
	while True:
		if lines + 1 > len(line):
			fmoney.close()
			fmoney = open("C:/SSBData/moneylist.txt", "a")
			fmoney.write("%s %s\n" % (user.id,str(moneyindex)))
			return moneyindex
		line0 = line[lines].split()
		data0 = ""
		if line0[0] == str(user.id):
			money_def = int(line0[1]) + moneyindex
			line[lines] = "%s %s" % (user.id, money_def)
			fmoney.close()
			fmoney = open("C:/SSBData/moneylist.txt", "w")
			for data in line:
				if len(data) > 3:
					# If line is blank, program does not duplicate line to data.
					data0 += "%s\n" % data
			fmoney.write(data0)
			fmoney.close()
			return money_def
		lines += 1

def dailyupdate(user):
	fmoney = open("C:/SSBData/dailyupdate.txt", "r")
	line = fmoney.readlines()
	lines = 0
	ftime = time.time()
	while True:
		if lines + 1 > len(line):
			fmoney.close()
			fmoney = open("C:/SSBData/dailyupdate.txt", "a")
			fmoney.write("%s %s\n" % (user.id,ftime))
			return 1
		line0 = line[lines].split()
		data0 = ""
		if line0[0] == str(user.id):
			if float(line0[1]) > ftime - 60:
				return 0
			line[lines] = "%s %s" % (user.id,ftime)
			fmoney.close()
			fmoney = open("C:/SSBData/dailyupdate.txt", "w")
			for data in line:
				if len(data) > 3:
					# If line is blank, program does not duplicate line to data.
					data0 += "%s\n" % data
			fmoney.write(data0)
			fmoney.close()
			return 1
		lines += 1

async def ping(user, mch, msg):
	fping = open("C:/SSBData/pingcount.txt", "r")
	line = fping.readlines()
	lines = 0
	while True:
		if lines + 1 > len(line):
			fping.close()
			fping = open("C:/SSBData/pingcount.txt", "a")
			fping.write("%s 1\n" % user.id)
			break
		line0 = line[lines].split(" ")
		data0 = ""
		if line0[0] == str(user.id):
			pingcount = int(line0[1]) + 1
			line[lines] = "%s %s" % (user.id,pingcount)
			fping.close()
			fping = open("C:/SSBData/.txt", "w")
			for data in line:
				if len(data) > 3:
					# If line is blank, program does not duplicate line to data.
					data0 += "%s\n" % data
			fping.write(data0)
			fping.close()
			break
		lines += 1
	print(pingcount)
	if pingcount == 10:
		await client.send_message(mch, "<@%s>, You just reached 10 pings in total!" % user.id)
	elif pingcount == 100:
		await client.send_message(mch, "<@%s>, You just reached 100 pings! Keep going! Keep going!" % user.id)
	elif pingcount == 333:
		await client.send_message(mch, "<@%s>, 333 is a special number, isn't it? You just reached 333 pings!" % user.id)
	elif pingcount == 1000:
		await client.send_message(mch, "<@%s>, 1000 pings? Thank you for loving SimSimBot, Sincerely. By SSB Team." % user.id)
	else:
		if msg[1].upper() == "PING":
			await client.send_message(mch, "<@%s> pong!" % user.id)
		if msg[1].upper() == "PONG":
			await client.send_message(mch, "<@%s> ping!" % user.id)

async def help(mch):
	fhelp = open("C:/SSBData/helptext.txt", "r")
	embed = discord.Embed(title="SSB Command List", description = fhelp.read(), color=0x25DFE4)
	fhelp.close()
	await client.send_message(mch, embed = embed)

async def help_kor(mch):
	fhelp = open("C:/SSBData/helptext_kor.txt", "r")
	embed = discord.Embed(title="심심봇 도움말", description = fhelp.read(), color=0x25DFE4)
	fhelp.close()
	await client.send_message(mch, embed = embed)

async def latestupdate(mch):
	fupdate = open("C:/SSBData/latestupdate.txt", "r")
	embed = discord.Embed(title="SSB Latest Update", description = fupdate.read(), color=0x25DFE4)
	fupdate.close()
	await client.send_message(mch, embed = embed)

async def latestupdate_kor(mch):
	fupdate = open("C:/SSBData/latestupdate_kor.txt", "r")
	embed = discord.Embed(title="심심봇 최신 업데이트 내용", description = fupdate.read(), color=0x25DFE4)
	fupdate.close()
	await client.send_message(mch, embed = embed)

async def myinfo(user, mch):
	embed = discord.Embed(title="{} Info".format(user.name), description="slice of information of {}".format(user.name), color=0x25DFE4)
	embed.add_field(name="Name", value=user.name, inline=True)
	embed.add_field(name="ID", value=user.id, inline=True)
	embed.add_field(name="Joined at Server", value=user.joined_at, inline=True)
	embed.add_field(name="Role", value=user.top_role, inline=True)
	embed.add_field(name="Status", value=user.status, inline=True)
	embed.set_thumbnail(url=user.avatar_url)
	await client.send_message(mch, embed = embed)

async def serverinfo(server, mch):
	embed = discord.Embed(title="{} Info".format(server.name), description="slice of information of {}".format(server.name), color=0x25DFE4)
	embed.add_field(name="Created at", value=server.created_at, inline=True)
	embed.add_field(name="ID", value=server.id, inline=True)
	embed.add_field(name="Members", value=server.member_count, inline=True)
	embed.add_field(name="Server Owner", value=server.owner.name, inline=True)
	embed.add_field(name="Role Count", value=len(server.roles), inline=True)
	embed.add_field(name="Emoji Count", value=len(server.emojis), inline=True)
	embed.set_thumbnail(url=server.icon_url)
	await client.send_message(mch, embed = embed)

async def neko(mch):
	neko = re.compile('<meta property="og:image" content="(.+)"/>', re.S)
	nekoreq = requests.get('https://nekos.life/').text
	nekourl = neko.search(nekoreq)
	await client.send_message(mch,"Here is a neko for you!\n%s" % nekourl.group(1))

async def neko19(mch):
	neko = re.compile('<img src="(.+?)"')
	nekoreq = requests.get('https://nekos.life/lewd').text
	nekourl = neko.search(nekoreq)
	await client.send_message(mch,"Here is a neko for you! ~~Look Behind you...~~\n%s" % nekourl.group(1))

async def gelbooru(mch, msg):
	try:
		if len(msg) == 2:
			gelnum = randint(4000000, 4175000)
			neko = re.compile('src="(https://simg3\.gelbooru\.com/.+?)"', re.S)
			gelreq = requests.get('https://gelbooru.com/index.php?page=post&s=view&id=%s' % gelnum).text
			gelurl = neko.search(gelreq)
			await client.send_message(mch,"Here is a random gelbooru image for you!(image number: %d)\n%s" % (gelnum,gelurl.group(1)))
		else:
			tag = " ".join(msg[2:])
			pagenum = randint(0,10) * 42
			tagneko = re.compile('<span id="s([0-9]+)"')
			tagreq = requests.get('https://gelbooru.com/index.php?page=post&s=list&tags=%s&pid=%s' % (tag,pagenum)).text
			tagurl = tagneko.findall(tagreq)
			if tagurl:
				gelnum = tagurl.pop()
				print(gelnum)
				neko = re.compile('src="(https://simg3\.gelbooru\.com/.+?)"', re.S)
				gelreq = requests.get('https://gelbooru.com/index.php?page=post&s=view&id=%s' % gelnum).text
				gelurl = neko.search(gelreq)
				await client.send_message(mch,"Random **tag:%s** gelbooru image for you!(image number: %s)\n%s" % (tag,gelnum,gelurl.group(1)))
			else:
				await client.send_message(mch,"Sorry, But I can't find the tag:**%s**" % tag)
	except:
		await client.send_message(mch,"Sorry, But please try again in a few seconds.")
async def danbooru(mch):
	gelnum = randint(3000000, 3070000)
	neko = re.compile('<meta property="og:image" content="(.+)">', re.S)
	gelreq = requests.get('https://danbooru.donmai.us/posts/%s' % gelnum).text
	print(gelreq)
	gelurl = neko.search(gelreq)
	print(gelurl)
	await client.send_message(mch,"Here is a random danbooru image for you!\n%s" % gelurl.group(1))

async def memo(tomsg, mch, msg, user):
	memolist = os.listdir('C:/SSBData/memo')
	if re.compile("^SSB MEMO CREATE (.+)$", re.S).search(tomsg.upper()):
		m = re.compile("^SSB MEMO CREATE .+$", re.S).search(tomsg.upper())
		while True:
			memonum = str(randint(1000, 9999))
			if '%s.txt' % memonum in memolist:
				print("Memo #%s is already exist." % memonum)
			else:
				fmemo = open("C:/SSBData/memo/%s.txt" % memonum, "w")
				fmemo.write(" ".join(msg[3:]))
				fmemo.close()
				await client.send_message(mch, ":desktop: **Memo #%s was successfully created**, <@%s>!" % (memonum, user.id))
				break
	elif re.compile("^SSB MEMO(| CALL) ([0-9]+)$", re.S).search(tomsg.upper()):
		m = re.compile("^SSB MEMO(| CALL) ([0-9]+)$", re.S).search(tomsg.upper())
		if "%s.txt" % m.group(2) in memolist:
			fmemo = open("C:/SSBData/memo/%s.txt" % m.group(2), "r")
			await client.send_message(mch, "**Memo #%s**\n\n%s" % (m.group(2), fmemo.read()))
		else:
			await client.send_message(mch, "<@%s> Sorry, but Memo #%s does not exist!" % (user.id, m.group(2)))

async def wiki(mch, msg, user, nomsg):
	if len(msg) == 2:
		await client.send_message(mch, "<@%s>, Welcome to SSB wiki.\n\n`ssb wiki <article name> <view/edit/revision> <edit/revision number>`" % user.id)
	wikilist = os.listdir('C:/SSBData/wiki')
	if re.compile("^SSB WIKI (.+) (EDIT|HISTORY|VIEW|REVISION) (.+?)$", re.S | re.I).search(nomsg):
		m = re.compile("SSB WIKI (.+) (EDIT|HISTORY|VIEW|REVISION) (.+?)$", re.S | re.I).search(nomsg)
		fwikiver = open("C:/SSBData/wikiver/%s.txt" % m.group(1), "a")
		fver = open("C:/SSBData/wikiver.txt", "r")
		if m.group(2).upper() == 'EDIT':
			fwiki = open("C:/SSBData/wiki/%s.txt" % m.group(1), "w")
			if '%s.txt' % m.group(1) in wikilist:
				line = fver.readlines()
				lines = 0
				while True:
					if lines + 1 > len(line):
						fver.close()
						fver = open("C:/SSBData/wikiver.txt", "a")
						fver.write("%s 1\n" % m.group(1))
						break
					line0 = line[lines].split(" ")
					data0 = ""
					if line0[0] == m.group(1):
						vercount = int(line0[1]) + 1
						line[lines] = "%s %s" % (m.group(1),vercount)
						fver.close()
						fver = open("C:/SSBData/wikiver.txt", "w")
						for data in line:
							if len(data) > 3:
								# If line is blank, program does not duplicate line to data.
								data0 += "%s\n" % data
						fver.write(data0)
						fver.close()
						break
					lines += 1
				fwikiver.write('<version %d>\n%s\n%s\n' % (vercount,user.name,m.group(3)))
				fwiki.write('%s' % m.group(3))
			else:
				vercount = 1
				fver.close()
				fver = open("C:/SSBData/wikiver.txt", "a")
				fver.write("%s 1\n" % m.group(1))
				fwikiver.write('<version 1>\n%s\n%s\n' % (user.name,m.group(3)))
				fwiki.write('%s' % m.group(3))
			await client.send_message(mch, "Article **%s** was successfully edited by <@%s>!" % (m.group(1),user.id))
		elif m.group(2).upper() == 'HISTORY':
			await client.send_message(mch, "Sorry, but we are still working for this, so please wait for a while.")
		elif m.group(2).upper() == 'REVISION':
			if '%s.txt' % m.group(1) in wikilist:
				frevision = open("C:/SSBData/wikiver/%s.txt" % m.group(1), "r")
				redata = frevision.read()
				print(redata)
				redata = redata.split("\n")
				row = 0
				data = ""
				for i in redata:
					if i == "<version %s>" % int(m.group(3)):
						print(redata[row])
						print(len(redata))
						author = redata[row+1]
						row += 2
						while True:
							data += "\n%s" % redata[row]
							print(data)
							row += 1
							if row >= len(redata):
								embed = discord.Embed(title="SSB Wiki:%s Revision %s" % (m.group(1),m.group(3)), description="Edited by %s%s" % (author, data), color=0x25DFE4)
								await client.send_message(mch, embed = embed)
								break
							elif redata[row] == "<version %s>" % str(int(m.group(3)) + 1):
								embed = discord.Embed(title="SSB Wiki:%s Revision %s" % (m.group(1),m.group(3)), description="Edited by %s%s" % (author, data), color=0x25DFE4)
								await client.send_message(mch, embed = embed)
								break
					elif row == len(redata):
						await client.send_message(mch, "Sorry, but revision **<%s>** does not exist!" % m.group(3))
					row += 1
			else: await client.send_message(mch, "Sorry, but article **<%s>** does not exist!" % m.group(1))
	elif re.compile("^SSB WIKI (.+) VIEW", re.S | re.I).search(nomsg):
		m = re.compile("^SSB WIKI (.+) VIEW", re.S | re.I).search(nomsg)
		if '%s.txt' % m.group(1) in wikilist:
			fwiki = open("C:/SSBData/wiki/%s.txt" % m.group(1), "r")
			embed = discord.Embed(title="SSB Wiki:%s" % m.group(1), description=fwiki.read(), color=0x25DFE4)
			fwiki.close()
			await client.send_message(mch, embed = embed)
		else: await client.send_message(mch, "Sorry, but article **<%s>** does not exist!" % m.group(1))

async def dice(mch, nomsg, user):
	m = re.compile("^SSB ([0-9]+)D([0-9]+)$", re.I).search(nomsg)
	numlist = []
	maxnum = int(m.group(2))
	if int(m.group(1)) > 300:
		await client.send_message(mch, "<@%s> Sorry, but maximum number count is 300." % user.id)
	else:
		reptotal = int(m.group(1))
		rep = 0
		plus = 0
		while True:
			if rep < reptotal:
				rand = randint(1, maxnum)
				plus += rand
				numlist.append(str(rand))
				rep += 1
			else:
				avr = plus / reptotal
				await client.send_message(mch, ":game_die:**Result for %sd%s**\n\n```%s\nTotal: %s  Average: %s```" % (m.group(1), m.group(2), " ".join(numlist[0:]), str(plus), str(avr)))
				break

async def imgur(mch, msg, user):
	try:
		if len(msg) == 2:
			await client.send_message(mch, "<@%s>, Please use search keyword for imgur search!" % user.id)
		else:
			tag = " ".join(msg[2:])
			search = "+".join(msg[2:])
			neko = re.compile('<a class="image-list-link" href="(.+?)" data-page="0">', re.S)
			gelreq = requests.get('https://imgur.com/search/score?q=%s' % search).text
			imgurl = neko.findall(gelreq)
			if imgurl:
				imgid = imgurl[randint(0,len(imgurl))]
				gelurl = 'http://imgur.com%s' % imgid
				await client.send_message(mch,"Random **%s** imgur image for you!\n%s" % (tag,gelurl))
			else:
				await client.send_message(mch,"Sorry, But I can't find the image for **%s**" % tag)
	except:
		await client.send_message(mch,"Sorry, But please try again in a few seconds.")

async def credit(mch, server):
	embed = discord.Embed(title="Invite SSB Now!", description="Programmed by SimSimBot Team\nSpecial thanks to 심심의화신\n\nSimSimBot Beta 1.1.6(Build 410)", colour=discord.Colour.blue(), url = "https://discordapp.com/api/oauth2/authorize?client_id=421303509263056896&permissions=473167955&scope=bot", color=0x25DFE4)
	embed.set_thumbnail(url=server.icon_url)
	await client.send_message(mch, embed = embed)


@client.event
async def on_ready():
	print("bot is connecting...")

@client.event
async def on_message(message):
	msg = message.content.split(" ")
	tomsg = message.content.upper()
	nomsg = message.content
	user = message.author
	mch = message.channel
	server = message.server
	print(nomsg)
	if message.author == client.user:
		return
	elif re.compile("^SSB (PING|PONG)$", re.I).search(tomsg):
		await ping(user, mch, msg)
	elif re.compile("^SSB HELP", re.I).search(tomsg):
		await help(mch)
	elif re.compile("^SSB (도움|도움말|헬프)", re.I).search(tomsg):
		await help_kor(mch)
	elif re.compile("^SSB (ECHO|MIRROR)").search(tomsg):
		msg = message.content.split(" ")
		print("%s" % (" ".join(msg[2:])))
		await client.send_message(message.channel, ":eye: Mirroring what you've said!\n\n%s" % (" ".join(msg[2:])))
	elif re.compile("^SSB (MYINFO|USERINFO)", re.I).search(tomsg):
		await myinfo(user, mch)
	elif re.compile("^SSB (SERVER|SERVERINFO|MYSERVER)", re.I).search(tomsg):
		await serverinfo(server, mch)
	elif re.compile("^SSB (NEKO|NEKOIMG|NEKOIMAGE)$", re.I).search(tomsg):
		await neko(mch)
	elif re.compile("^SSB (NEKO19|PUSSYNEKO|NEKOLEWD|LEWDNEKO)$", re.I).search(tomsg):
		await neko19(mch)
	elif re.compile("^SSB GELBOORU", re.I).search(tomsg):
		await gelbooru(mch, msg)
	elif re.compile("^SSB DANBOORU", re.I).search(tomsg):
		await danbooru(mch)
	elif re.compile("^SSB SEARCH", re.I).search(tomsg):
		site = msg[2]
		m = re.compile("^SSB (SEARCH|FIND) .+ (IN|AT|ON) .+$", re.I).match(tomsg)
		if m:
			await client.send_message(message.channel, "We are still working for this, so please wait for a while.")
		else:
			await client.send_message(message.channel, "Here is a Google link for you!\n( https://www.google.co.kr/search?q=%s )" % (" ".join(msg[2:])))
	elif re.compile("^SSB MEMO", re.I).search(tomsg):
		await memo(tomsg, mch, msg, user)
	elif re.compile("^SSB WIKI", re.I).search(tomsg):
		await wiki(mch, msg, user, nomsg)
	elif re.compile("^SSB (CREDITS|CREDIT)", re.I).search(tomsg):
		await credit(mch, server)
	elif re.compile("^SSB (UPDATE|LATESTUPDATE)", re.I).search(tomsg):
		await latestupdate(mch)
	elif re.compile("^SSB (업데이트|최근업데이트|최신업데이트|최신업뎃)", re.I).search(tomsg):
		await latestupdate_kor(mch)
	elif re.compile("^SSB (SAY|SPEAK)", re.I).search(tomsg):
		await client.send_message(message.channel, "%s" % " ".join(msg[2:]))
	elif re.compile("^SSB [0-9]+D[0-9]+$", re.I).search(tomsg):
		await dice(mch, nomsg, user)
	elif re.compile("^SSB (IMGUR|IMGURIMAGE)", re.I).search(tomsg):
		await imgur(mch, msg, user)
	elif re.compile("^SSB (DAILY|DAILYMONEY)", re.I).search(tomsg):
		if dailyupdate(user):
			money = moneyfix(user, 10)
			await client.send_message(message.channel, "SSB Money test. You received $10!\n\nYou have total of $%s." % money)
		else: await client.send_message(message.channel, "<@%s>, You have to wait 1 minute to receive money again." % user.id)
