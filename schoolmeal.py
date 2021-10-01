#-*- coding:utf-8 -*-
import discord, asyncio, datetime, neispy, random
from discord.ext import commands, tasks
from os import environ
from itertools import cycle

client=commands.Bot(command_prefix='?')
client.remove_command('help')
client.load_extension("jishaku")
neis = neispy.Client(KEY=environ.get('APIKEY'), pSize=1)
status = cycle(['버그 제보: Dillot .𝙿#6079', '?도움 으로 명령어를 확인하세요!', '성남중학교 급식 알림봇입니다.'])
tz = datetime.timezone(datetime.timedelta(hours=9))

@client.command()
async def 도움(ctx):
    help = """
    <> = 필수 요소
    [] = 선택 요소
    
    **?도움**
    ㄴ 현재 보고 계신 도움말을 보여줍니다.

    **?급식 [학교명] [대상 날짜]**
    ㄴ 지정된 학교명*(나이스에 등록된 학교이면 초중고대 상관 없이 모두 가능)*과 대상 날짜에 해당하는 급식을 알려줍니다.
    ㄴ **참고:** 학교명이 없을 경우 `성남중학교`로 자동 지정 되며, 대상 날짜가 없을 경우 현재 날짜로 자동 지정 됩니다.
    ㄴ **참고:** 대상 날짜를 지정하시려면 꼭 학교명을 입력해 주셔야 합니다.
    ㄴ **참고:** 학교명 예시: `성남중학교`, 대상 날짜 예시: `20210930`
    """
    embed = discord.Embed(title='성남중급식알림봇 도움말', description=help, timestamp=datetime.datetime.now(tz=tz), color=0xD9FA39)
    getuseravatar(ctx.author, embed)
    try:
        await ctx.author.send(embed=embed)
        await ctx.message.add_reaction('✅')
    except:
        try:
            await ctx.send(embed=embed)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('❎')

@client.command()
async def 급식(ctx, school:str='성남중학교', dateinfo:str=''):
    await SendMeal(channelId=ctx.channel.id, schoolName=school, dateinfo=dateinfo, author=ctx.author)

async def GetMeal(schoolName, dateinfo=''):
    scinfo = await neis.schoolInfo(SCHUL_NM=schoolName)
    AE = scinfo[0].ATPT_OFCDC_SC_CODE  # 교육청코드
    SE = scinfo[0].SD_SCHUL_CODE  # 학교코드
    try:
        scmeal = await neis.mealServiceDietInfo(AE, SE, MLSV_YMD=dateinfo)
        meal = scmeal[0].DDISH_NM.replace("<br/>", "\n")  # 줄바꿈으로 만든뒤 출력
    except:
        meal = 'INFO-200'
    return meal

when=[datetime.time(8, 20, tzinfo=tz)]
@tasks.loop(time=when)
async def my_task():
    now = datetime.datetime.now(tz=tz)
    if now.hour != 7 and now.hour != 8 and now.hour != 9 and now.hour != 10 and now.hour != 11 and now.hour != 12:
        print("체킹시스템 작동. 태스크 엑세스 거부")
        return
    dateinfo=''
    channelId=834281229716684850
    schoolName='성남중학교'
    try:
        if not dateinfo:
            dateinfo = datetime.datetime.now(tz=tz).strftime('%Y%m%d')
        meals = await GetMeal(schoolName, dateinfo)
        meal = f"**[ 점심 ]**\n{meals}"
        embed = discord.Embed(title="오늘의 급식", description=meal, timestamp=datetime.datetime.now(tz=tz), color=0xff005d)
        embed.set_author(icon_url='https://open.neis.go.kr/img/np/C0001.png', name='알레르기 정보(클릭)', url='https://pastebin.com/bSvNRWH0')
        if meals == 'INFO-200':
            image = randomimage()
            embed = discord.Embed(title="오늘의 급식", description='오늘은 급식이 없다구욧', timestamp=datetime.datetime.now(tz=tz), color=0xff005d)
            embed.set_image(url=image)
        embed.set_footer(text='Automatic', icon_url="https://cdn.discordapp.com/avatars/793171487372476446/aaa65470ce891079474805a50e502359.webp")
        channel = client.get_channel(channelId)
        await channel.send(embed=embed)
        print("정기 알림 완료")
    except Exception as e:
        channel = client.get_channel(channelId)
        embed = discord.Embed(title="서비스 장애", description='서비스가 작동하는데 예외가 발생하였습니다.', color=0xe91e63, timestamp=datetime.datetime.now(tz=tz))
        embed.add_field(name='다음 오류코드와 함께 관리자에게 문의하십시오.', value=str(e))
        await channel.send(embed=embed)
        print("정기 알림 실패")

async def SendMeal(dateinfo, author, channelId, schoolName):
    try:
        if not dateinfo:
            dateinfo = datetime.datetime.now(tz=tz).strftime('%Y%m%d')
        meals = await GetMeal(schoolName, dateinfo)
        dateyear = dateinfo[0:4]
        datemonth = dateinfo[4:6]
        dateday = dateinfo[6:8]
        meal = f"**[ 점심 ] - {dateyear}년 {datemonth}월 {dateday}일**\n{meals}"
        embed = discord.Embed(title=f"{schoolName}의 급식", description=meal, timestamp=datetime.datetime.now(tz=tz), color=0xff005d)
        embed.set_author(icon_url='https://open.neis.go.kr/img/np/C0001.png', name='알레르기 정보(클릭)', url='https://pastebin.com/bSvNRWH0')
        if meals == 'INFO-200':
            image = randomimage()
            embed = discord.Embed(title=f"{schoolName}의 급식", description=f'{dateyear}년 {datemonth}월 {dateday}일에는 급식이 존재하지 않다구욧', timestamp=datetime.datetime.now(tz=tz), color=0xff005d)
            embed.set_image(url=image)
        embed = getuseravatar(author, embed)
        channel = client.get_channel(channelId)
        await channel.send(embed=embed)
    except Exception as e:
        channel = client.get_channel(channelId)
        embed = discord.Embed(title="서비스 장애", description='서비스가 작동하는데 예외가 발생하였습니다.', color=0xe91e63, timestamp=datetime.datetime.now(tz=tz))
        embed.add_field(name='다음 오류코드와 함께 관리자에게 문의하십시오.', value=str(e))
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
    avatar_type='.png'
    if author.avatar != None:
        if author.avatar.startswith('a_'):
            avatar_type='.gif'
        else:
            pass
        url=f'https://cdn.discordapp.com/avatars/{author.id}/{author.avatar}{avatar_type}'
    else:
        discriminator=int(author.discriminator) % 5
        url=f'https://cdn.discordapp.com/embed/avatars/{discriminator}.png'
    embed.set_footer(text=f'{author.display_name}', icon_url=url)
    return embed

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_connect():
    print("연결중")
    await client.change_presence(activity=discord.Game(name="봇 연결중..."))

@client.event
async def on_ready():
    print('준비중')
    await client.change_presence(activity=discord.Game(name="봇 작동중..."))
    my_task.start()
    change_status.start()
    print('준비 완료')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass

##연결##
try:
    client.run(environ.get('TOKEN'))
except discord.LoginFailure:
    input("유효하지 않은 토큰이 입력되어 로그인에 실패하였습니다.")
except discord.HTTPException:
    input("HTTP request 작업에 오류가 발생해 로그인에 실패하였습니다.")
except AttributeError:
    input("토큰 처리에 문제가 발생했습니다. 토큰 관련하여 손상이 되어있는지 확인해보세요.")
except Exception as e:
    input(f"로그인 도중 {e} 오류가 발생했습니다.")
