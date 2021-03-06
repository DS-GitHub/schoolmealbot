#-*- coding:utf-8 -*-
import discord, asyncio, datetime, random
from discord.ext import commands, tasks
from os import environ
from itertools import cycle
from neispy import Neispy

client=commands.Bot(command_prefix='?')
client.remove_command('help')
client.load_extension("jishaku")
status = cycle(['λ²κ·Έ μ λ³΄: Dillot .πΏ#6079', '?λμ μΌλ‘ λͺλ Ήμ΄λ₯Ό νμΈνμΈμ!', 'μ±λ¨μ€νκ΅ κΈμ μλ¦Όλ΄μλλ€.'])
tz = datetime.timezone(datetime.timedelta(hours=9))

@client.command()
async def λμ(ctx):
    help = """
    <> = νμ μμ
    [] = μ ν μμ
    
    **?λμ**
    γ΄ νμ¬ λ³΄κ³  κ³μ  λμλ§μ λ³΄μ¬μ€λλ€.

    **?κΈμ [νκ΅λͺ] [λμ λ μ§]**
    γ΄ μ§μ λ νκ΅λͺ*(λμ΄μ€μ λ±λ‘λ νκ΅μ΄λ©΄ μ΄μ€κ³ λ μκ΄ μμ΄ λͺ¨λ κ°λ₯)*κ³Ό λμ λ μ§μ ν΄λΉνλ κΈμμ μλ €μ€λλ€.
    γ΄ **μ°Έκ³ :** νκ΅λͺμ΄ μμ κ²½μ° `μ±λ¨μ€νκ΅`λ‘ μλ μ§μ  λλ©°, λμ λ μ§κ° μμ κ²½μ° νμ¬ λ μ§λ‘ μλ μ§μ  λ©λλ€.
    γ΄ **μ°Έκ³ :** λμ λ μ§λ₯Ό μ§μ νμλ €λ©΄ κΌ­ νκ΅λͺμ μλ ₯ν΄ μ£ΌμμΌ ν©λλ€.
    γ΄ **μ°Έκ³ :** νκ΅λͺ μμ: `μ±λ¨μ€νκ΅`, λμ λ μ§ μμ: `20210930`
    """
    embed = discord.Embed(title='μ±λ¨μ€κΈμμλ¦Όλ΄ λμλ§', description=help, timestamp=datetime.datetime.now(tz=tz), color=0xD9FA39)
    getuseravatar(ctx.author, embed)
    try:
        await ctx.author.send(embed=embed)
        await ctx.message.add_reaction('β')
    except:
        try:
            await ctx.send(embed=embed)
            await ctx.message.add_reaction('β')
        except:
            await ctx.message.add_reaction('β')

@client.command()
async def κΈμ(ctx, school:str='μ±λ¨μ€νκ΅', dateinfo:str=''):
    await SendMeal(channelId=ctx.channel.id, schoolName=school, dateinfo=dateinfo, author=ctx.author)

async def GetMeal(schoolName, dateinfo=''):
    async with Neispy(KEY=environ.get('APIKEY'), pSize=1) as neis:
        scinfo = await neis.schoolInfo(SCHUL_NM=schoolName)
        AE = scinfo[0].ATPT_OFCDC_SC_CODE  # κ΅μ‘μ²­μ½λ
        SE = scinfo[0].SD_SCHUL_CODE  # νκ΅μ½λ
        try:
            scmeal = await neis.mealServiceDietInfo(AE, SE, MLSV_YMD=dateinfo)
            meal = scmeal[0].DDISH_NM.replace("<br/>", "\n")  # μ€λ°κΏμΌλ‘ λ§λ λ€ μΆλ ₯
        except:
            meal = 'INFO-200'
        return meal

@tasks.loop(hours=24)
async def my_task():
    dateinfo=''
    channelId=834281229716684850
    schoolName='μ±λ¨μ€νκ΅'
    try:
        if not dateinfo:
            dateinfo = datetime.datetime.now(tz=tz).strftime('%Y%m%d')
        meals = await GetMeal(schoolName, dateinfo)
        meal = f"**[ μ μ¬ ]**\n{meals}"
        embed = discord.Embed(title="μ€λμ κΈμ", description=meal, timestamp=datetime.datetime.now(tz=tz), color=0xff005d)
        embed.set_author(icon_url='https://open.neis.go.kr/img/np/C0001.png', name='μλ λ₯΄κΈ° μ λ³΄(ν΄λ¦­)', url='https://pastebin.com/bSvNRWH0')
        if meals == 'INFO-200':
            image = randomimage()
            embed = discord.Embed(title="μ€λμ κΈμ", description='μ€λμ κΈμμ΄ μλ€κ΅¬μ§', timestamp=datetime.datetime.now(tz=tz), color=0xff005d)
            embed.set_image(url=image)
        embed.set_footer(text='Automatic', icon_url="https://cdn.discordapp.com/avatars/793171487372476446/aaa65470ce891079474805a50e502359.webp")
        channel = client.get_channel(channelId)
        await channel.send(embed=embed)
        print("μ κΈ° μλ¦Ό μλ£")
    except Exception as e:
        channel = client.get_channel(channelId)
        embed = discord.Embed(title="μλΉμ€ μ₯μ ", description='μλΉμ€κ° μλνλλ° μμΈκ° λ°μνμμ΅λλ€.', color=0xe91e63, timestamp=datetime.datetime.now(tz=tz))
        embed.add_field(name='λ€μ μ€λ₯μ½λμ ν¨κ» κ΄λ¦¬μμκ² λ¬Έμνμ­μμ€.', value=str(e))
        await channel.send(embed=embed)
        print("μ κΈ° μλ¦Ό μ€ν¨")

async def SendMeal(dateinfo, author, channelId, schoolName):
    try:
        if not dateinfo:
            dateinfo = datetime.datetime.now(tz=tz).strftime('%Y%m%d')
        meals = await GetMeal(schoolName, dateinfo)
        dateyear = dateinfo[0:4]
        datemonth = dateinfo[4:6]
        dateday = dateinfo[6:8]
        meal = f"**[ μ μ¬ ] - {dateyear}λ {datemonth}μ {dateday}μΌ**\n{meals}"
        embed = discord.Embed(title=f"{schoolName}μ κΈμ", description=meal, timestamp=datetime.datetime.now(tz=tz), color=0xff005d)
        embed.set_author(icon_url='https://open.neis.go.kr/img/np/C0001.png', name='μλ λ₯΄κΈ° μ λ³΄(ν΄λ¦­)', url='https://pastebin.com/bSvNRWH0')
        if meals == 'INFO-200':
            image = randomimage()
            embed = discord.Embed(title=f"{schoolName}μ κΈμ", description=f'{dateyear}λ {datemonth}μ {dateday}μΌμλ κΈμμ΄ μ‘΄μ¬νμ§ μλ€κ΅¬μ§', timestamp=datetime.datetime.now(tz=tz), color=0xff005d)
            embed.set_image(url=image)
        embed = getuseravatar(author, embed)
        channel = client.get_channel(channelId)
        await channel.send(embed=embed)
    except Exception as e:
        channel = client.get_channel(channelId)
        embed = discord.Embed(title="μλΉμ€ μ₯μ ", description='μλΉμ€κ° μλνλλ° μμΈκ° λ°μνμμ΅λλ€.', color=0xe91e63, timestamp=datetime.datetime.now(tz=tz))
        embed.add_field(name='λ€μ μ€λ₯μ½λμ ν¨κ» κ΄λ¦¬μμκ² λ¬Έμνμ­μμ€.', value=str(e))
        await channel.send(embed=embed)

def randomimage():
    r = [ 
            'https://media.discordapp.net/attachments/778892732856139786/834460635848769586/132.png',
            'https://media.discordapp.net/attachments/834260946423513109/834595677488283678/e0acf729ba838080.png',
            'https://media.discordapp.net/attachments/834260946423513109/834594513930420234/KakaoTalk_20210308_000701755.png',
            'https://media.discordapp.net/attachments/834260946423513109/834594030998126632/image0.png',
            'https://media.discordapp.net/attachments/834460263943241739/834595667933790228/received_771292416922507.jpeg',
            'https://media.discordapp.net/attachments/725664502619832410/833630804139049000/image0.jpg',
            'https://media.discordapp.net/attachments/725664502619832410/823342682772340776/image0.png',
            'https://media.discordapp.net/attachments/725664502619832410/834600446907514970/ezgif.com-gif-maker_4.gif',
            'https://media.discordapp.net/attachments/725664502619832410/820680320063635476/image0.jpg',
            'https://media.discordapp.net/attachments/725664502619832410/834600535818371082/ezgif.com-gif-maker_5.gif',
            'https://media.discordapp.net/attachments/725664502619832410/817229146824376320/image0.jpg'
        ]
    return random.choice(r)

def getuseravatar(author, embed):
    if author.avatar != None:
        url=author.avatar
    else:
        discriminator=int(author.discriminator) % 5
        url=f'https://cdn.discordapp.com/embed/avatars/{discriminator}.png'
    embed.set_footer(text=f'{author.display_name}', icon_url=url)
    return embed

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@my_task.before_loop
async def wait():
    # this will use the machine's timezone
    # to use a specific timezone use `.now(timezone)` without `.astimezone()`
    # timezones can be acquired using any of
    # `datetime.timezone.utc`
    # `datetime.timezone(offset_timedelta)`
    # `pytz.timezone(name)` (third-party package)
    now = datetime.datetime.now(tz=tz)
    next_run = now.replace(hour=8, minute=0, second=0)
    if next_run < now:
        next_run += datetime.timedelta(days=1)
    await discord.utils.sleep_until(next_run)

@client.event
async def on_connect():
    print("μ°κ²°μ€")
    await client.change_presence(activity=discord.Game(name="λ΄ μ°κ²°μ€..."))

@client.event
async def on_ready():
    print('μ€λΉ μλ£')
    try:
        change_status.start()
        my_task.start()
    except RuntimeError:
        print("νμ€ν¬κ° μ΄λ―Έ μ€νμ€μ΄μ΄μ νμ€ν¬λ₯Ό μμν  μ μμ΅λλ€.")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass

##μ°κ²°##
try:
    client.run(environ.get('TOKEN'))
except discord.LoginFailure:
    input("μ ν¨νμ§ μμ ν ν°μ΄ μλ ₯λμ΄ λ‘κ·ΈμΈμ μ€ν¨νμμ΅λλ€.")
except discord.HTTPException:
    input("HTTP request μμμ μ€λ₯κ° λ°μν΄ λ‘κ·ΈμΈμ μ€ν¨νμμ΅λλ€.")
except AttributeError:
    input("ν ν° μ²λ¦¬μ λ¬Έμ κ° λ°μνμ΅λλ€. ν ν° κ΄λ ¨νμ¬ μμμ΄ λμ΄μλμ§ νμΈν΄λ³΄μΈμ.")
except Exception as e:
    input(f"λ‘κ·ΈμΈ λμ€ {e} μ€λ₯κ° λ°μνμ΅λλ€.")
