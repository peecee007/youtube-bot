import asyncio
import discord
from discord.ext import commands

# ------------------- CONFIG -------------------
TOKEN = "YOUR_BOT_TOKEN"
PREFIX = "!"
# ---------------------------------------------

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Simple FIFO queue for URLs
queue = asyncio.Queue()
playing = False          # flag to avoid starting several players


async def player(voice_client: discord.VoiceClient):
    """Consume URLs from the queue and stream them one‑by‑one."""
    global playing
    playing = True

    while not queue.empty():
        url = await queue.get()
        try:
            # FFmpegOpusAudio streams the URL directly; Discord encodes it to Opus.
            source = discord.FFmpegOpusAudio(url)
            voice_client.play(source, after=lambda e: print(e) if e else None)

            # Wait until the track finishes (or is stopped)
            while voice_client.is_playing():
                await asyncio.sleep(0.5)

        except Exception as exc:
            await voice_client.channel.send(f"Error playing {url}: {exc}")
        finally:
            queue.task_done()

    playing = False


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def join(ctx: commands.Context):
    """Make the bot join the voice channel you’re in."""
    if not ctx.author.voice:
        return await ctx.send("You’re not in a voice channel!")

    channel = ctx.author.voice.channel
    voice = await channel.connect()

    # If a player isn’t already running, start one
    if not playing:
        bot.loop.create_task(player(voice))


@bot.command()
async def play(ctx: commands.Context, *, url: str):
    """Add a URL (Audiomack, YouTube, direct MP3, …) to the queue."""
    if not ctx.voice_client:
        return await ctx.send("I’m not in a voice channel. Use `!join` first.")

    await queue.put(url)
    await ctx.send(f"Queued: {url}")

    # If the player isn’t already running, start it
    if not playing:
        bot.loop.create_task(player(ctx.voice_client))


@bot.command()
async def leave(ctx: commands.Context):
    """Disconnect the bot from the voice channel."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Bye!")