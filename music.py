import discord
from discord.ext import commands
from discord.ext import tasks

import youtube_dl
import ffmpeg


class music(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.replayF = False
		self.queue = list()


	@commands.command()
	async def join(self, ctx):
		if ctx.author.voice is None:
			await ctx.send("You are not in a voice channel")
		voice_channel = ctx.author.voice.channel
		if ctx.voice_client is None:
			await voice_channel.connect()
		else:
			await ctx.voice_client.move_to(voice_channel)

	@commands.command()
	async def leave(self, ctx):
		await ctx.voice_client.disconnect()


	@commands.command()
	async def queue(self, ctx, url):
		self.queue.append(url)
		await ctx.send(url + " Добавлено в очередь", delete_after=10)


	@commands.command()
	async def playnext(self, ctx):
		if ctx.author.voice is not None and ctx.voice_client is None:
			await ctx.author.voice.channel.connect()
		if len(self.queue)>0:
			await self.playSong(ctx, self.queue[0])
			self.queue.pop(0)

	@commands.command()
	async def skip(self, ctx):
		await ctx.voice_client.stop()
		if len(self.queue)>0:
			await self.playSong(ctx, self.queue[0])
			self.queue.pop(0)

	@commands.command()
	async def stop(self, ctx):
		if ctx.voice_client.is_playing():
			await ctx.voice_client.stop()
		else: await ctx.send("И так не играю")

	@commands.command()
	async def pause(self, ctx):
		ctx.voice_client.pause()
		await ctx.send("Pause")	
	
	@commands.command()
	async def resume(self, ctx):
		ctx.voice_client.resume()
		await ctx.send("Resume")	

	@commands.command()
	async def showqueue(self, ctx):
		urls = ""
		for url in self.queue:
			urls+=url
			urls+='\n'
		await ctx.send("Queue:")
		await ctx.send(urls)
	#@commands.command()
	#async def replay(self, ctx):
	#	if self.replayF == False: 
	#		self.replayF = True
	#		await ctx.send("Set replay to true")
	#	else:
	#		self.replayF = False
	#		await ctx.send("Set replay to false")

	async def playSong(self, ctx, url):
		FMMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
		YDL_OPTS = {'format': "bestaudio"}
		vc = ctx.voice_client
		with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
			info = ydl.extract_info(url, download=False)
			url2 = info['formats'][0]['url']
			source = await discord.FFmpegOpusAudio.from_probe(url2, **FMMPEG_OPTS)
			vc.play(source)
	@tasks.loop(seconds = 5.0)
	async def check_queue(self, ctx):
		if not ctx.voice_client.is_playing() and len(self.queue)>0:
			url = self.queue[0]
			self.queue.pop(0)
			await self.playSong(ctx, url)
			await ctx.send("Играет : " + url)

async def setup(client):
	await client.add_cog(music(client))