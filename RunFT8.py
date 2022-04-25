import os
import discord
import shutil
from dotenv import load_dotenv
from string import ascii_letters, digits

TestModeEnabled = input('Would you like to enable test mode?: ')
if TestModeEnabled == 'y':
    TestModeStatus = True
if TestModeEnabled == 'n':
    TestModeStatus = False
else:
    print('Wrong command entered, assuming TestMode')
    TestModeStatus = True

#Input DiscordID of owner here:
OWNER = []

def FindLine(MapName):
    df = open(MapName)
    read = df.read()
    df.seek(0)
    global arr
    arr = []
    line = 1
    for word in read:
        if word == '\n':
            line += 1

    for i in range(line):
        arr.append(df.readline())

    ##print(arr)
    df.close
    word = '8'

    global ExportCord
    global ExportUpper
    global ExportMid
    global ExportLower
    global XLocal
    global YLocal


    for i in range(len(arr)):
        if word in arr[i]:
            YLocal = i+1
            Up = arr[i-1]
            Mid = arr[i]
            Down = arr[i+1]
            XLocal = Mid.find(word)
            LowerBounds = int(XLocal - 1)
            UpperBounds = int(XLocal + 2)
            #print(Location)
            #print("("+str(XLocal) + ",-" + str(YLocal)+")")
            #print(Up[LowerBounds:UpperBounds])
            #print(Mid[LowerBounds:UpperBounds])
            #print(Down[LowerBounds:UpperBounds])
            ExportCord = ("("+str(XLocal) + ",-" + str(YLocal)+")")
            ExportUpper = (Up[LowerBounds:UpperBounds])
            ExportMid = (Mid[LowerBounds:UpperBounds])
            ExportLower = (Down[LowerBounds:UpperBounds])
            return ExportCord, ExportUpper, ExportMid, ExportLower, XLocal, YLocal

def StrtUpName(DnDMPSrtupMC):
    global Name
    Name = DnDMPSrtupMC
    Name = Name[14:]

def ReplaceTile(i, arr, XLocal):
    Mid = arr[i]
    MidList = list(Mid)
    MidList[XLocal] = "0"
    Mid = ''.join(MidList)
    arr[i] = Mid
    #print(arr)
    return arr

def WMover(word, arr, XLocal):
    for i in range(len(arr)):
        if word in arr[i]:
            Up = arr[i-1]
            UpList = list(Up)
            UpList[XLocal] = "8"
            Up = ''.join(UpList)
            #print(Up)
            arr[i-1] = Up
            #print(arr)
            Mid = arr[i]
            MidList = list(Mid)
            MidList[XLocal] = "0"
            Mid = ''.join(MidList)
            arr[i] = Mid
            #print(arr)
            ReplaceTile(i, arr, XLocal)

def SMover(word, arr, XLocal):
    for i in range(len(arr)):
        if word in arr[i]:
            #print(i)
            Down = arr[i+1]
            DownList = list(Down)
            DownList[XLocal] = "8"
            Down = ''.join(DownList)
            #print(Down)
            arr[i+1] = Down
            #print(arr)
            Mid = arr[i]
            MidList = list(Mid)
            MidList[XLocal] = "0"
            Mid = ''.join(MidList)
            arr[i] = Mid
            #print(arr)
            ReplaceTile(i, arr, XLocal)
            return

def AMover(word, arr, XLocal):
    for i in range(len(arr)):
        if word in arr[i]:
            Left = arr[i]
            LeftList = list(Left)
            LeftList[XLocal-1] = "8"
            Left = ''.join(LeftList)
            #print(Left)
            arr[i] = Left
            #print(arr)
            Mid = arr[i]
            MidList = list(Mid)
            MidList[XLocal] = "0"
            Mid = ''.join(MidList)
            arr[i] = Mid
            #print(arr) 
            ReplaceTile(i, arr, XLocal)

def DMover(word, arr, XLocal):
    for i in range(len(arr)):
        if word in arr[i]:
            Right = arr[i]
            RightList = list(Right)
            RightList[XLocal+1] = "8"
            Right = ''.join(RightList)
            #print(Right)
            arr[i] = Right
            #print(arr)
            Mid = arr[i]
            MidList = list(Mid)
            MidList[XLocal] = "0"
            Mid = ''.join(MidList)
            arr[i] = Mid
            #print(arr)
            ReplaceTile(i, arr, XLocal)

def SaveMap(MapName, arr):
    SaveMap = open(MapName,'w')
    EditedMap = ''.join(arr)
    #print(EditedMap)
    SaveMap.write(EditedMap)
    SaveMap.close

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    if TestModeStatus == True:
        await client.change_presence(activity=discord.Game(name="with settings."))
    if TestModeStatus == False:
        await client.change_presence(activity=discord.Game(name="with friends."))
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if '!DnDMPStartup' in message.content:
        if str(message.author.id) == str(discord.utils.get(message.guild.categories, name=str(message.author.id))):
            await message.channel.send("You are currently unable to use this command.")
        else:
            DnDMPSrtupMC = message.content
            if set(str(DnDMPSrtupMC[14:])).difference(ascii_letters + digits):
                await message.channel.send('Please use a normal name.')
                return
            else:
                StrtUpName(DnDMPSrtupMC)
                await message.channel.send('Chaning nick to: ' + Name) 
                await message.author.edit(nick=Name)
                StrtCatName = message.author.id
                category = await message.guild.create_category(StrtCatName)
                guild = message.channel.guild
                role = await guild.create_role(name = Name)
                overwrites = {
                                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                            }
                await category.edit(overwrites=overwrites)
                await guild.create_text_channel('Bot', category = category, sync_permissions=True, slowmode_delay=10)
                await guild.create_text_channel(Name, category = category, sync_permissions=True)
                await message.channel.send('Created Private Category and Channels')
                member = message.author
                await member.add_roles(role)
                await message.channel.send('Applied Role')
                src = 'TestMap.txt'
                dst = ("./Maps/" + str(message.author.id)+'.txt')
                shutil.copy2(src,dst)
                await message.channel.send('Map: ' + dst + ' has been created.')
                await message.channel.send('Have fun!')
                
    if '!TestUtils' in message.content:
        await message.channel.send('This does nothing atm')
            
    if message.content == '!TestComd':
        print(str(message.channel))
            
    if message.content == '!Where':
        if str(message.channel) == "bot":
            MapName = ("./Maps/" + str(message.author.id)+'.txt')
            df = open(MapName)
            read = df.read()
            df.seek(0)
            arr = []
            line = 1
            for word in read:
                if word == '\n':
                    line += 1

            for i in range(line):
                arr.append(df.readline())
            
            df.close
            word = '8'
            
            global ExportCord
            global ExportUpper
            global ExportMid
            global ExportLower
            
            
            for i in range(len(arr)):
                if word in arr[i]:
                    YLocal = i+1
                    Up = arr[i-1]
                    Mid = arr[i]
                    Down = arr[i+1]
                    XLocal = Mid.find(word)
                    LowerBounds = int(XLocal - 1)
                    UpperBounds = int(XLocal + 2)
                    ExportCord = ("("+str(XLocal) + ",-" + str(YLocal)+")")
                    ExportUpper = (Up[LowerBounds:UpperBounds])
                    ExportMid = (Mid[LowerBounds:UpperBounds])
                    ExportLower = (Down[LowerBounds:UpperBounds])
            
            await message.channel.send(ExportCord)
            await message.channel.send(ExportUpper)
            await message.channel.send(ExportMid)
            await message.channel.send(ExportLower)
        else:
            await message.channel.send('You can not use that command here.')
    
    if '!Move' in message.content:
        if str(message.channel) == 'bot':
            Direction = message.content[6:]
            MapName = ("./Maps/" + str(message.author.id)+'.txt')
            df = open(MapName)
            read = df.read()
            df.seek(0)
            arr = []
            line = 1
            for word in read:
                if word == '\n':
                    line += 1

            for i in range(line):
                arr.append(df.readline())

            df.close
            word = '8'

            for i in range(len(arr)):
                if word in arr[i]:
                    YLocal = i+1
                    Up = arr[i-1]
                    Mid = arr[i]
                    Down = arr[i+1]
                    XLocal = Mid.find(word)
                    LowerBounds = int(XLocal - 1)
                    UpperBounds = int(XLocal + 2)
                    ExportCord = ("("+str(XLocal) + ",-" + str(YLocal)+")")
                    ExportUpper = (Up[LowerBounds:UpperBounds])
                    ExportMid = (Mid[LowerBounds:UpperBounds])
                    ExportLower = (Down[LowerBounds:UpperBounds])
            word = '8'
            if Direction == 'w':
                await message.channel.send('You are moving up.')
                YLocal = YLocal - 1
                UpCheck = arr[YLocal-1]
                UpCheckList = list(UpCheck)
                WDirecCheck1 = UpCheckList[XLocal]
                if WDirecCheck1 == '1':
                    await message.channel.send('You can not move there, there is a wall there.')
                    return
                else:
                    await message.channel.send("You are moving to: " + "("+str(XLocal) + ",-" + str(YLocal-1)+")")
                    WMover(word, arr, XLocal)
                    SaveMap(MapName, arr)
                    await message.channel.send('You have moved up.')
                    return
            
            if Direction == 's':
                await message.channel.send('You are moving down.')
                YLocal = YLocal - 1
                DownCheck = arr[YLocal+1]
                DownCheckList = list(DownCheck)
                SDirecCheck1 = DownCheckList[XLocal]
                if SDirecCheck1 == '1':
                    await message.channel.send('You can not move there, there is a wall there.')
                    return
                else:
                    await message.channel.send("You are moving to: " + "("+str(XLocal) + ",-" + str(YLocal+1)+")")
                    SMover(word, arr, XLocal)
                    SaveMap(MapName, arr)
                    await message.channel.send('You have moved down.')
                    return
            
            if Direction == 'a':
                await message.channel.send('You are moving left.')
                YLocal = YLocal - 1
                LeftCheck = arr[YLocal]
                LeftCheckList = list(LeftCheck)
                ADirecCheck1 = LeftCheckList[XLocal-1]
                if ADirecCheck1 == '1':
                    await message.channel.send('You can not move there, there is a wall there.')
                    return
                else:
                    await message.channel.send("You are moving to: " + "("+str(XLocal-1) + ",-" + str(YLocal)+")")
                    AMover(word, arr, XLocal)
                    SaveMap(MapName, arr)
                    await message.channel.send('You have moved left.')
                    return
            
            if Direction == 'd':
                await message.channel.send('You are moving right.')
                YLocal = YLocal - 1
                RightCheck = arr[YLocal]
                RightCheckList = list(RightCheck)
                DDirecCheck1 = RightCheckList[XLocal+1]
                if DDirecCheck1 == '1':
                    await message.channel.send('You can not move there, there is a wall there.')
                    return
                else:
                    await message.channel.send("You are moving to: " + "("+str(XLocal+1) + ",-" + str(YLocal)+")")
                    DMover(word, arr, XLocal)
                    SaveMap(MapName, arr)
                    await message.channel.send('You have moved right.')
                    return
        else:
            await message.channel.send('You can not use that command here')

client.run(TOKEN)