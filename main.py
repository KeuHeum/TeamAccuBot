import Aconfig
import discord
import asyncio
import sys
import traceback
import datetime
from discord.ext.tasks import loop
import random
import requests
from bs4 import BeautifulSoup
import re
from twilio.rest import Client

INTENTS = discord.Intents.all()
client = discord.Client(intents=INTENTS)

token = Aconfig.config["token"]

color = Aconfig.config["color"]

staff = list(["604983644733440001", "700222381058293793", "527500397645004800", "458528026645495808", "636830106907705344"])

################################임베드 설정################################
helpembed=discord.Embed(title="TEAM ACCU 도움말!", description=f"모든 명령어의 접두사는 `아큐야`입니다!", color=color)
helpembed.set_thumbnail(url="https://cdn.discordapp.com/icons/837169375027003493/e3975b67a94c7f1188f2100548f76753.webp?size=1024")
helpembed.add_field(name="안녕", value="아큐봇이 인사를 받아줘요!", inline=False)
helpembed.add_field(name="핑", value="현재 핑을 알려줍니다!", inline=False)
helpembed.add_field(name="버전", value="현재 버전을 알려줍니다!", inline=False)
helpembed.add_field(name="초대링크 <수>", value="현재 서버의 초대 링크를 알려줍니다!", inline=False)
helpembed.add_field(name="프사 <맨션>", value="맨션을 했다면 맨션한 사람의 프사를, 아니라면 자신의 프사를 보여줘요!", inline=False)
helpembed.add_field(name="서버인원", value="현재 서버의 인원을 알려줘요!", inline=False)
helpembed.add_field(name="티켓", value="신고 전용 채널을 만들어 줘요!", inline=False)
helpembed.add_field(name="티엠아이", value="TMI를 알려줍니다!", inline=False)
helpembed.set_footer(text="[]는 필수, <>는 선택입니다.")

prefix = "아큐야 "
gamenum = 0

tmi = [
    "이 서버는 `2021.4.30/오후 12시 32분 12초`에 만들어졌습니다.",
    "TMI는 총 15개입니다.",
    "아큐봇의 코드는 오픈코드입니다.", 
    "이 서버는 두번째 서버입니다. 원래 서버였던곳은 현재 이곳의 팀원인 크흠이 실친 개발자와 노는 공간이 되었습니다.",
    "이 봇은 2일만에 만들어졌으며 1일차-약 7시간, 2일차 약 11시간을 써서 만든 봇입니다.",
    "이 서버는 초기(개설한지 1일후) `유저2, 관리자5(개발자4, 포럼관리자1), 봇5` 였습니다",
    "#역할받기에서 유저의 역할은 취소해도 사라지지 않지만, 공지받기는 취소하면 사라집니다.",
    "이곳의 팀원인 크흠은 아래와 같은 말을 한적이 있다 - 제보 새우님(팀원)\nhttps://cdn.discordapp.com/attachments/837887004091613185/838053929140224020/2021_05_01_23_06_04_335.png",
    "JMC50님과 새우님은 서로 매우 친한 사이다. 아래의 내용은 서로의 벌칙 사진이다.||욕설은 지움처리를 하였습니다.||\nhttps://cdn.discordapp.com/attachments/789854387429441537/838790093052444753/ffa251f628fd9171.png\nhttps://cdn.discordapp.com/attachments/789854387429441537/838790083485368340/3.png",
    "아큐봇의 공개기능은 총 9개, 비공개 기능은 6개입니다",
    "크흠봇은 크흠봇으로 시작하는 말중 대답하지 않은것을 기록합니다.",
    "이 서버의 로고는 그림판으로 만들어졌습니다",
    "팀원인 브루니님은 중국어를 싫어합니다.",
    "크흠님은 바부입니다."
]

hello = [
    "안녕하세요",
    "안녕",
    "하이요",
    "하염",
    "하위하위",
    "안농",
    "누가 불렀니?",
    "누구야!",
    "누구세요",
    "?",
    "반가워요!",
    "방가방가",
    "ㅎㅇ!",
    "안녕하신가요!!!!!",
    "¿"
]

################################봇이 준비됨################################
@client.event
async def on_ready():
    presence_loop.start()
    print(client.user.name + "봇이 시작됨")
    print(f'{len(client.guilds)}개의 서버에 참여중')
    print(f'{client.guilds[0].member_count}명이 이용중')
    print(f"{Aconfig.now_time()}에 봇이 켜졌습니다.")
    print('=====================================')
    
################################루프################################
@loop(count=None, seconds=7)
async def presence_loop():
    global gamenum
    games = [f'아큐봇 - {prefix}도움 입력', 'Team Accu의 팀원을 모집합니다!', f'{client.guilds[0].member_count}명의 사용자와 함께']
    if gamenum == len(games)-1:
        gamenum = 0
    else:
        gamenum += 1
    await client.change_presence(activity=discord.Game(games[gamenum]), status=discord.Status.online)

################################메인################################
@client.event
async def on_message(message):
    if message.author.id == 604983644733440001 and message.content == "아큐야 강제종료":
        await message.channel.send("강제종료 완료")
        exit()
        
    elif message.author.bot:
        return None

    elif message.author.system:
        return None

    elif message.channel.type == discord.ChannelType.group:
        return None

    elif message.channel.type == discord.ChannelType.private:
        return None

    elif message.content.startswith(f"{prefix}안녕"):
        x = random.randint(1, len(hello)+1)
        try:
            await message.channel.send(hello[x])
        except:
            await message.channel.send(f"안녕하세요 {message.author.name}님!")
            
    elif message.content.startswith(f"{prefix}티엠아이"):
        x = random.randint(1, len(tmi)+1)
        try:
            await message.channel.send(tmi[x])
        except:
            date = datetime.datetime.utcfromtimestamp(((int(message.author.id) >> 22) + 1420070400000) / 1000)
            await message.channel.send(f"디스코드 봇은 생각보다 얻을 수 있는 정보가 많습니다. 예를들자면, 당신의 디스코드 서버 가입일은 {date.year}년 {date.month}월 {date.day}일입니다!")

    elif message.content.startswith(f"{prefix}버전"):
        await message.channel.send("현재 아큐봇의 버전은 `1.0.0` 입니다!")
    
    elif message.content.startswith(f"{prefix}서버인원"):
        human = 0
        bot = 0
        for i in message.guild.members:
            if i.bot == True:
                bot = bot + 1
            else:
                human = human + 1
        await message.channel.send(f"현재 서버의 멤버수는 {message.author.guild.member_count}명 입니다!```봇 : {bot}명, 사람 : {human}명```")

    elif message.content.startswith(f"{prefix}프사"):
        try:
            message.content.split(" ")[2]
            try:
                userid = re.findall("\d+", message.content.split(" ")[2])
                user = client.get_user(int(userid[0]))
                await message.channel.send(user.avatar_url)
            except:
                await message.channel.send("맨션이 잘 되었는지 다시 한번 확인해주세요")
        except:
            await message.channel.send(message.author.avatar_url)

    elif message.content.startswith(f"{prefix}도움"):
        helpembed.set_author(name="제작자 - Team Accu", url="https://www.youtube.com/channel/UCGv_lxHyiMib0IzFhJEfVvg", icon_url=client.get_user(604983644733440001).avatar_url)
        response = await message.channel.send(content="이 메시지는 15초 후 없어집니다", embed=helpembed)
        await asyncio.sleep(15)
        embed=discord.Embed(title="TEAM ACCU 도움말!", description=f"모든 명령어의 접두사는 `아큐야`입니다!", color=color)
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/837169375027003493/e3975b67a94c7f1188f2100548f76753.webp?size=1024")
        embed.add_field(name="명령어", value="`핑, 버전, 초대링크 <수>, 프사 <맨션>, 서버인원, 티켓`", inline=False)
        embed.set_footer(text="[]는 필수, <>는 선택입니다.")
        await response.edit(content="",embed=embed)

    elif message.content.startswith(f'{prefix}핑'):
        ping1 = round(client.latency*1000,2)
        if ping1 <= 100: pinglevel1 = '🔵 매우좋음'
        elif ping1 <= 250: pinglevel1 = '🟢 양호함'
        elif ping1 <= 400: pinglevel1 = '🟡 보통'
        elif ping1 <= 550: pinglevel1 = '🔴 나쁨'
        else: pinglevel1 = '⚪ 매우나쁨'
        embed=discord.Embed(title='🏓 퐁!', description=f'디스코드 지연시간: {ping1}ms - {pinglevel1}\n디스코드 지연시간은 디스코드 웹소켓 프로토콜의 지연 시간(latency)을 뜻합니다.', color=color, timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
        await message.channel.send(embed=embed)

    elif message.content == f"{prefix}전체통계":
        req = requests.get("https://search.naver.com/search.naver?where=nexearch&sm=top_sug.pre&fbm=1&acr=1&acq=zhfhsk&qdt=0&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98")
        soup = BeautifulSoup(req.text, "html.parser")
        today = datetime.datetime.now().strftime('%Y년 %m월 %d일')
        embed=discord.Embed(title="Team Accu", description="코로나 한국 확진자 전체통계!", color=color, timestamp=datetime.datetime.utcnow())
        embed.add_field(name=f"확진자 - {soup.find('li' , class_='info_01').text.split(' ')[3]}명", value=f"전체 확진자 - {soup.find('li' , class_='info_01').text.split(' ')[2]}명", inline=True)
        embed.add_field(name=f"검사중 - {soup.find('li' , class_='info_02').text.split(' ')[3]}명", value=f"전체 검사중 - {soup.find('li' , class_='info_02').text.split(' ')[2]}명", inline=True)
        embed.add_field(name=f"격리해제 - {soup.find('li' , class_='info_03').text.split(' ')[3]}명", value=f"전체 격리해제 - {soup.find('li' , class_='info_03').text.split(' ')[2]}명", inline=True)
        embed.add_field(name=f"사망자 - {soup.find('li' , class_='info_04').text.split(' ')[3]}명", value=f"전체 사망자 - {soup.find('li' , class_='info_04').text.split(' ')[2]}명", inline=True)
        embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
        await message.channel.send(embed=embed)

    elif message.content.startswith(f"{prefix}밴"):
        if message.author.guild_permissions.ban_members:
            try:
                reason = message.content[(len(message.content.split(" ")[3]) + 29):]
            except:
                reason = None
            user_id = re.findall("\d+", message.content.split(" ")[2])
            try:
                userban = message.guild.get_member(int((str(user_id[0]))[:18]))
            except:
                embed=discord.Embed(title="**⛔오류발생**", description = "해당 멤버를 찾을 수 없습니다.", timestamp=datetime.datetime.utcnow(), color =color)
                embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
            else:
                await message.guild.ban(userban, reason=reason)
                
                embed=discord.Embed(title="**✅밴 성공**", description = f"{userban.mention}님은 현재 서버에서 밴당하셨습니다.\n사유:`{reason}`", timestamp=datetime.datetime.utcnow(), color = color)
                embed.set_footer(text="처리자 - " + message.author)
                await message.channel.send(embed=embed)

                author = await client.get_user(int((str(user_id[0]))[:18])).create_dm()
                embed=discord.Embed(title="**추방알림**", description = f"{userban.mention}님은 {message.guild.name}서버에서 밴당하셨습니다.\n사유:`{reason}`", timestamp=datetime.datetime.utcnow(), color = color)
                embed.set_footer(text="처리자 - " + message.author)
                await author.send(embed=embed)
        else:
            embed=discord.Embed(title='**⛔오류발생!**', description=f'{message.author.mention}님은 유저를 밴 할 수 있는 권한이 없습니다.', color=color, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed)

    elif message.content.startswith(f"{prefix}킥"):
        if message.author.guild_permissions.kick_members:
            try:
                reason = message.content[(len(message.content.split(" ")[3]) + 29):]
            except:
                reason = None
                user_id = re.findall("\d+", message.content.split(" ")[2])
            try:
                userkick = message.guild.get_member(int((str(user_id[0]))[:18]))
            except:
                embed=discord.Embed(title="**⛔오류발생**", description = "해당 멤버를 찾을 수 없습니다.", timestamp=datetime.datetime.utcnow(),color = color)
                embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
            else:
                await message.guild.ban(userkick, reason=reason)
                
                embed=discord.Embed(title="**✅킥 성공**", description = f"{userkick.mention}님은 현재 서버에서 킥당하셨습니다.\n사유:`{reason}`", timestamp=datetime.datetime.utcnow(), color =color)
                embed.set_footer(text="처리자 - " + message.author)
                await message.channel.send(embed=embed)

                author = await client.get_user(int((str(user_id[0]))[:18])).create_dm()
                embed=discord.Embed(title="**추방알림**", description = f"{userkick.mention}님은 {message.guild.name}서버에서 킥당하셨습니다.\n사유:`{reason}`", timestamp=datetime.datetime.utcnow(), color = color)
                embed.set_footer(text="처리자 - " + message.author)
                await author.send(embed=embed)
        else:
            embed=discord.Embed(title='**⛔오류발생!**', description=f'{message.author.mention}님은 유저를 킥 할 수 있는 권한이 없습니다.', color=color, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed)
    

    elif message.content.startswith(f"{prefix}초대링크"):
        try:
            message.content.split(" ")[2]
        except:
            invitelink = await message.channel.create_invite(max_uses=0,unique=True)
            await message.channel.send(f"참! 명령어 뒤에 사용수를 넣으면 최대사용수가 정해진답니다 다 알고 있었죠?\n{invitelink}")
        else:
            try:
                int(message.content.split(" ")[2])
            except:
                await message.channel.send(f"명령어 뒤에는 숫자만 넣어주세요!")
            else:
                if int(message.content.split(" ")[2]) < 0:
                    await message.channel.send("사용수는 1~100사이 또는 무한을 원하신다면 0을 적으셔야 합니다. (기본은 무한!)")
                elif int(message.content.split(" ")[2]) > 100:
                    await message.channel.send("사용수는 1~100사이 또는 무한을 원하신다면 0을 적으셔야 합니다. (기본은 무한!)")
                else:
                    use = message.content.split(" ")[2]
                    invitelink = await message.channel.create_invite(max_uses=use,unique=True)
                    await message.channel.send(f"참! 명령어 뒤에 사용수를 넣으면 최대사용수가 정해진답니다. 다 알고 있었죠?\n{invitelink}")

    elif message.content.startswith(f"{prefix}공지"):
        for i in staff:
            if i == message.author.id:
                await message.delete()
                embed=discord.Embed(title='Team Accu 공지', description=message.content[7:], color=color, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"{message.author} - 인증됨", icon_url=message.author.avatar_url)
                await message.channel.send(content=message.guild.get_role(837169375027003499).mention,embed=embed)

    elif message.content.startswith(f"{prefix}청소"):
        if message.author.guild_permissions.manage_messages:
            try:
                amount = int(message.content.split(" ")[2])
                if amount <= 0:
                    await message.channel.send("자연수만 사용하실 수 있습니다.")
                    return
            except:
                embed = discord.Embed(title="오류",description=f"'{prefix}청소 갯수'로 사용하실수 있습니다. EX)!청소 3", color=Aconfig.config['error'], timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
                return
            try:
                await message.channel.purge(limit = amount)
                embed = discord.Embed(title="청소!",description=f"{message.author.mention}에 의해 {amount}개가 청소되었습니다.", color=Aconfig.config['error'], timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
                message = await message.channel.send(embed=embed)
                await asyncio.sleep(5)
                await message.delete()
                return
            except discord.Forbidden:
                embed = discord.Embed(title="오류",description=str(message.channel) + "의 권한이 부족합니다.\n아큐봇의 '메세지 관리'권한을 부여해주세요.", color=Aconfig.config['error'], timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
                return
        else:
            embed = discord.Embed(title="오류",description=f"{message.author.mention}님의 메시지 삭제 권한이 없습니다.", color=Aconfig.config['error'], timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed)

    elif message.content.startswith(f"{prefix}티켓"):
        content = ""
        channel_name = (f'{str(message.author).lower()}님_채널').replace("#", "")
        for channel in message.guild.text_channels:
            if str(channel.name) == str(channel_name):
                content = f"이미 {message.author.mention}님이 요청하신 채널({channel.mention})이 있습니다."
        if content != "":
            await message.channel.send(content)
        else:
            overwrites = {
            message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            message.author: discord.PermissionOverwrite(read_messages=True)
            }

            channel = await message.guild.create_text_channel(channel_name, overwrites=overwrites)
            embed = discord.Embed(title="채널생성",description="신고사항, 건의사항등을 말씀하여주시기 바랍니다", color=Aconfig.config['color'], timestamp=datetime.datetime.utcnow())
            await channel.send(content="@here", embed=embed)

    elif message.content.startswith(f"{prefix}채널삭제"):
        if message.author.guild_permissions.manage_channels:
            if message.channel.name.endswith("님_채널") == False:
                await message.channel.send("티켓 채널이 아니라면, 삭제할 수 없습니다.")
            else:
                embed = discord.Embed(title="채널삭제",description="채널을 삭제하시겠습니까?", color=Aconfig.config['error'], timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
                checkembed = await message.channel.send(embed=embed)
                for emoji in ['⭕', '❌']:
                    await checkembed.add_reaction(emoji)
                def auditcheck(reaction, user):
                    return user == message.author and (str(reaction.emoji) == '⭕' or str(reaction.emoji) == '❌')
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=auditcheck)
                except asyncio.TimeoutError:
                    embed=discord.Embed(title=f'⛔ 시간이 초과되었습니다.', color=Aconfig.config['error'])
                    await message.channel.send(embed=embed)
                else:
                    if reaction.emoji == '⭕':
                        embed=discord.Embed(title=f'✅ 3초후 채널이 삭제됩니다', color=Aconfig.config['color'])
                        await checkembed.edit(embed=embed)
                        await asyncio.sleep(3)
                        await message.channel.delete()

                    elif reaction.emoji == '❌':
                        embed=discord.Embed(title=f'✅ 취소되었습니다.', color=Aconfig.config['color'])
                        await checkembed.edit(embed=embed)
        else:
            await message.channel.send(f"{message.author.mention}님은 채널삭제 권한이 없습니다")

    else:
        if message.content.startswith(prefix):
            content = ""
            x = random.randint(1, 3)
            if x == 1:
                content = "`에엥?`"
            elif x == 2:
                content = "`흐음?`"
            else:
                content = "`그게 뭐지?`"

            if "<@" in message.content:
                await message.channel.send(content)
            else:
                if len(message.content) <= 15:
                    await message.channel.send(f"`{message.content}?`")
                else:
                    await message.channel.send(content)

################################이모지 클릭################################
@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 837971122359369749:
        if payload.emoji.name == '1️⃣':
            await payload.member.guild.get_member(int(payload.user_id)).add_roles(payload.member.guild.get_role(837169375027003496), reason="이모지 클릭")
        elif payload.emoji.name == '2️⃣':
            await payload.member.guild.get_member(int(payload.user_id)).add_roles(payload.member.guild.get_role(837169375027003499), reason="이모지 클릭")

@client.event
async def on_raw_reaction_remove(payload):  
    if payload.message_id == 837971122359369749:
        if payload.emoji.name == '2️⃣':
            await client.get_guild(int(payload.guild_id)).get_member(int(payload.user_id)).remove_roles(client.get_guild(int(payload.guild_id)).get_role(837169375027003499), reason="이모지 클릭")


################################멤버 입, 퇴장################################
@client.event
async def on_member_join(member):
    await member.guild.get_member(int(member.id)).add_roles(member.guild.get_role(837169375027003496), reason="서버에 들어옴")
    embed=discord.Embed(title="환영합니다!", description=f"{member.mention}님, Team Accu에 오신것을 환영합니다!", color=color, timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=member)
    await client.get_channel(837169375352979522).send(embed=embed)

@client.event
async def on_member_remove(member):
    embed=discord.Embed(title="멤버퇴장", description=f"{member}님이 서버에서 나가셨습니다", color=Aconfig.config['error'], timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=member)
    await client.get_channel(837169375352979522).send(embed=embed)

################################오류################################
@client.event
async def on_error(event, *args, **kwargs):
    excinfo = sys.exc_info()
    if event == "on_message":
        embed = discord.Embed(title='⛔ 오류발생!', description=f'흠..오류가 발생한것 같으니, 체크를 해봐야겠어요..', color=Aconfig.config['error'])
        await args[0].channel.send(embed = embed)
    
    errstr = f'{"".join(traceback.format_tb(excinfo[2]))}{excinfo[0].__name__}: {excinfo[1]}'
    await client.get_channel(837955404314050571).send(f"\n**[오류발생]** \n타입 : {event}\n내용 : {errstr}//{Aconfig.now_time()}")


client.run(token)
