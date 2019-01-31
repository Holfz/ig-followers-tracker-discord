import discord
from discord.ext import commands
import asyncio
import mysql.connector
import instaloader
import datetime
import schedule

L = instaloader.Instaloader()
USER = 'usernamehere'

# Your preferred way of logging in:
L.load_session_from_file(USER, './session-' + USER)

db = mysql.connector.connect(
  host = "localhost",
  user  ="root",
  passwd = "",
  database = "igtracker"
)

cursor = db.cursor()

#today
today = datetime.datetime.now().strftime("%Y-%m-%d")

#yesterday
yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
yesterday = yesterday.strftime("%Y-%m-%d")

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.command(pass_context=True)
async def testembed(ctx):
    print(str(ctx.message.author) + " issued a command testembed")
    # https://stackoverflow.com/a/44863263
    # https://www.youtube.com/watch?v=XKQWxAaRgG0

    embed = discord.Embed(
        title = "Title",
        description = "Description",
        colour = discord.Colour.blue()
    )
    embed.add_field(name="Field1", value="hi\n123", inline=True)
    embed.add_field(name="Field2", value="hi2\n456", inline=True)

    await client.say(embed=embed)

@client.command(pass_context=True)
async def adduser(ctx, arg):
    print(str(ctx.message.author) + " issued a command adduser")
    # args = username
    sql = "SELECT * FROM user WHERE username = %s"
    adr = (arg,)

    cursor.execute(sql, adr)

    if not cursor.rowcount:
        PROFILE = arg
        profile = instaloader.Profile.from_username(L.context, PROFILE)
        sql = "INSERT INTO user (username, userid, image, discord_channel) VALUES (%s, %s, %s, %s)"
        val = (profile.username, str(profile.userid), profile.profile_pic_url, str(ctx.message.channel.id))
        cursor.execute(sql, val)
        db.commit()
        if (cursor.rowcount >= 1) :
            embed = discord.Embed(
                title = "Success",
                description = "Your Information was added to database.",
                colour = 0xBCF4E4
            )
            embed.add_field(name="Username", value=profile.username, inline=True)
            embed.add_field(name="Userid", value=str(profile.userid), inline=True)
            embed.add_field(name="Bound to Channel", value=str(ctx.message.channel.id), inline=True)
            embed.set_thumbnail(url=profile.profile_pic_url)
            await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title = "Failed",
                description = "Failed to add your username to database",
                colour = 0xECB4D3
            )
            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            title = "Failed",
            description = "Your account has already in a database.",
            colour = 0xECB4D3
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def check(ctx):
    print(str(ctx.message.author) + " issued a command check")
    await checkfollowers()

        
async def checkfollowers():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    print("checkfollowers function trigged")
    cursor.execute("SELECT * FROM user")
    results = cursor.fetchall()
    for result in results:
        #Load Profile
        PROFILE = result[1]
        profile = instaloader.Profile.from_username(L.context, PROFILE)
        followers = set(profile.get_followers())
        for follower in followers:
            sql = "INSERT INTO followers (username, userid, followed_to, insert_at) VALUES (%s, %s, %s, %s)"
            val = (follower.username, str(follower.userid), str(profile.userid), today)
            cursor.execute(sql, val)
            db.commit()
        await calculatefollower(result[2],result[4],profile)



#calculatefollower(userid,channelid):
async def calculatefollower(userid,channelid,profile):
    followers_list_today = []
    followers_list_yesterday = []
    #query today
    sql = "SELECT * FROM followers WHERE insert_at = %s AND followed_to = %s"
    adr = (today, userid)
    cursor.execute(sql, adr)
    result = cursor.fetchall()
    for result in result:
        followers_list_today.append(result[2])
    
    #query yesterday
    sql = "SELECT * FROM followers WHERE insert_at = %s AND followed_to = %s"
    adr = (yesterday, userid)
    cursor.execute(sql, adr)
    result = cursor.fetchall()
    for result in result:
        followers_list_yesterday.append(result[2])

    #ถ้ามีเมื่อวาน แสดงว่าอันฟอล
    #ถ้ามีวันนี้ แสดงว่าพึ่งฟอล
    follow = []
    unfollow = []
    differences = diff(followers_list_today, followers_list_yesterday)
    print(differences)
    for difference in differences:
        if (difference in followers_list_today):
            sql = "SELECT * FROM followers WHERE userid = %s ORDER BY id LIMIT 1"
            adr = (difference,)

            cursor.execute(sql, adr)
            result = cursor.fetchall()

            for x in result:
                follow.append(x[1] + " <" + difference + ">")

        elif (difference in followers_list_yesterday):
            sql = "SELECT * FROM followers WHERE userid = %s ORDER BY id LIMIT 1"
            adr = (difference,)

            cursor.execute(sql, adr)
            result = cursor.fetchall()

            for x in result:
                unfollow.append(x[1] + " <" + difference + ">")

    index = 0
    for i in unfollow:
        index += 1
        if(index == 1):
            unfollowemb = i
        else:
            unfollowemb += "\n" + i
    if (index == 0):
        unfollowemb = "-"
    index = 0
    for i in follow:
        index += 1
        if(index == 1):
            followemb = i
        else:
            followemb += "\n" + i
    if (index == 0):
        followemb = "-"

    embed = discord.Embed(
        title = "Your Instagram Daily Summary",
        colour = 0xBCF4E4
    )
    print(follow)
    print(unfollow)
    print(followemb)
    print(unfollowemb)
    embed.add_field(name="Username", value=profile.username, inline=True)
    embed.add_field(name="Userid", value=str(profile.userid), inline=True)
    embed.add_field(name="Your Follower Count Yesterday", value=str(len(followers_list_yesterday)), inline=False)
    embed.add_field(name="Your Follower Count Today", value=str(len(followers_list_today)), inline=False)
    embed.add_field(name="Who Unfollow You Today", value=unfollowemb, inline=True)
    embed.add_field(name="Who Follow You Today", value=followemb, inline=True)
    embed.set_thumbnail(url=profile.profile_pic_url)
    await client.send_message(discord.Object(id=str(channelid)), embed=embed)

client.run('token')
