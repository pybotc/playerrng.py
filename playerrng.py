import random
from roblox import Client
import asyncio
import robloxpy
from art import text2art
import climage
import requests
from roblox import AvatarThumbnailType
from PIL import Image
import glob
import os
from pathlib import Path
from termcolor import colored
import threading
import subprocess

client = Client()
done = False
stars = 0
messag = 0

user1 = []
randomid = []

def profileimage(image_url):
    try:
        img_data = requests.get(image_url).content
        with open('noFilter.png', 'wb') as write:
            write.write(img_data)
        im = Image.open("noFilter.png")
        newsize = (25, 25)
        im = im.resize(newsize)
        im.save('noFilter.png')
        output = climage.convert('noFilter.png', is_unicode=True, width=25)
        return output
    except:
        return "Image failed to load."

def get_player_info(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    response = requests.get(url)
    if response.status_code == 200:
        player_data = response.json()
        return player_data
    else:
        return None

def get_player_badges(user_id):
    url = f"https://accountinformation.roblox.com/v1/users/{user_id}/roblox-badges"
    response = requests.get(url)
    if response.status_code == 200:
        player_data = response.json()
        return player_data
    else:
        return None

def get_follower_count(user_id):
    url = f"https://friends.roblox.com/v1/users/{user_id}/followers/count"
    response = requests.get(url)
    if response.status_code == 200:
        player_data = response.json()
        return player_data
    else:
        return None

def get_player_games(user_id):
    url = f"https://games.roblox.com/v2/users/{user_id}/games?sortOrder=Asc&limit=50"
    response = requests.get(url)
    if response.status_code == 200:
        player_data = response.json()
        return player_data["data"]
    else:
        return None

def save(image_url, filename):
    try:
        img_data = requests.get(image_url).content
        with open(f'Saved Accounts/{filename}', 'wb') as saved:
            saved.write(img_data)
        return f'Saved Accounts/{filename}'
    except:
        with open(f'Saved Accounts/{filename}', 'wb') as saved:
            saved.close()
        return f'Saved Accounts/{filename}'

def retry_id(amoutcool):
    bling = []
    co2 = False
    for i in range(amoutcool):
        bling.append(str(random.randint(1,9)))
    bling = "".join(bling)
    bling = int(bling)
    return bling

def threaded_account(idra):
    global stars
    info = get_player_info(idra)
    username = info["name"]
    userncount = len(username)
    if userncount == 5:
        stars+= 10
    if userncount == 4:
        stars+= 35
    if userncount == 4:
        stars+= 50
    verified = info["hasVerifiedBadge"]
    if verified == True:
        stars+= 30
def threaded_badge(idra):
    global stars
    badges = get_player_badges(idra)
    for b in badges:
        badge = b["id"]
        badge = int(badge)
        if badge == 1:
            # admin
            stars = stars + 50
        elif badge == 2:
            stars = stars + 5
        elif badge == 3:
            stars = stars + 5
        elif badge == 4:
            stars = stars + 10
        elif badge == 5:
            stars = stars + 20
        elif badge == 6:
            stars = stars + 5
        elif badge == 7:
            stars = stars + 10
        elif badge == 8:
            stars = stars + 15
        elif badge == 9:
            stars = stars + 10
        elif badge == 17:
            stars = stars + 60
        elif badge == 18:
            # welcome to the club
            stars = stars + 5
    return stars

def threaded_visits(idaaa):
    global stars
    fawd = get_player_games(idaaa)
    visitstotal = 0
    for place in fawd:
        placevisits = place["placeVisits"]
        placevisits = int(placevisits)
        visitstotal = visitstotal + placevisits
    if visitstotal > 1000000000:
        stars = stars + 70
    elif visitstotal > 100000000:
        stars = stars + 60
    elif visitstotal > 10000000:
        stars = stars + 50
    elif visitstotal > 1000000:
        stars = stars + 40
    elif visitstotal > 100000:
        stars = stars + 30
    elif visitstotal > 10000:
        stars = stars + 20
    elif visitstotal > 100:
        stars = stars + 10
    return stars
def random_id(user1):
    global stars
    global randomid
    rarities = [
        "Legendary: " + str(random.randint(1,6)),
        "Rare: 7",
        "Uncommon: " + str(random.randint(8,9)),
        "Common: 10"
    ]
    frequency = {
        'Legendary': 5,
        'Rare': 20,
        'Uncommon': 100,
        'Common': 150
    }
    types = [skin.split(':')[0] for skin in rarities]
    # map types onto weightings
    weightings = [frequency[type] for type in types]
    useramount = random.choices(rarities, weightings, k=1)
    useramount = useramount[0]
    user1 = []
    randomid = []

    for letters in useramount:
        if letters.isnumeric():
            user1.append(letters)
    user1 = "".join(user1)
    user1 = int(user1)
    co2 = False
    for i in range(user1):
        randomid.append(str(random.randint(1,9)))
    randomid = "".join(randomid)
    randomid = int(randomid)
    thing = robloxpy.User.External.Isbanned(randomid)
    if thing == "User not found":
        while True:
            randomid = retry_id(user1)
            thing = robloxpy.User.External.Isbanned(randomid)
            if thing == "User not found":
                continue
            elif thing == True:
                continue
            else:
                break
    elif thing == True:
        while True:
            randomid = retry_id(useramount=useramount)
            thing = robloxpy.User.External.Isbanned(randomid)
            if thing == "User not found":
                continue
            elif thing == True:
                continue
            else:
                break
    if randomid < 1000000:
        stars = stars + 30
    elif randomid < 5000000:
        stars = stars + 25
    elif randomid < 10000000:
        stars = stars + 20
    elif randomid < 50000000:
        stars = stars + 15
    elif randomid < 100000000:
        stars = stars + 10
    threading.Thread(target=threaded_badge, args=(randomid,)).start()
    threading.Thread(target=threaded_account, args=(randomid,)).start()
    threading.Thread(target=threaded_visits, args=(randomid,)).start()
    follows = get_follower_count(randomid)["count"]
    if follows > 10000000:
        stars = stars + 50
    elif follows > 1000000:
        stars = stars + 40
    elif follows > 100000:
        stars = stars + 30
    elif follows > 100000:
        stars = stars + 20
    elif follows > 10000:
        stars = stars + 10
    elif follows > 1000:
        stars = stars + 5

    return randomid, stars


async def main():
    user1 = []
    randomuser = random_id(user1)
    randomid = randomuser[0]
    stars = randomuser[1]
    user = await client.get_user(randomid)
    info = get_player_info(randomid)
    verified = info["hasVerifiedBadge"]
    user_thumbnails = await client.thumbnails.get_user_avatar_thumbnails(
        users=[user],
        type=AvatarThumbnailType.headshot,
        size=(420, 420)
    )

    if len(user_thumbnails) > 0:
        user_thumbnail = user_thumbnails[0]
        if user_thumbnail.image_url == None:
            while True:
                user_thumbnails = await client.thumbnails.get_user_avatar_thumbnails(
                    users=[user],
                    type=AvatarThumbnailType.headshot,
                    size=(420, 420)
                )

                if len(user_thumbnails) > 0:
                    user_thumbnail = user_thumbnails[0]
                    if not user_thumbnail.image_url == None:
                        break

    profile = profileimage(user_thumbnail.image_url)
    username = await client.get_user_by_username(user.name, True)
    creationdate = robloxpy.User.External.CreationDate(randomid)
    if stars > 39:
        print(colored(text2art("LEGENDARY", font="small"),'yellow'))
        files = glob.glob('Saved Accounts/*.rng')
        for f in files:
            os.remove(f)
        save(user_thumbnail.image_url, f"{user.name} (LEGENDARY).rng")
    elif stars > 29:
        print(colored(text2art("EPIC", font="small"),'magenta'))
        files = glob.glob('Saved Accounts/*.rng')
        for f in files:
            os.remove(f)
        save(user_thumbnail.image_url, f"{user.name} (LEGENDARY).rng")
    elif stars > 19:
        print(colored(text2art("RARE", font="small"),'cyan'))
        files = glob.glob('Saved Accounts/*.rng')
        for f in files:
            os.remove(f)
        save(user_thumbnail.image_url, f"{user.name} (RARE).rng")
    elif stars > 9:
        print(colored(text2art("UNCOMMON", font="small"),'green'))
        files = glob.glob('Saved Accounts/*.rng')
        for f in files:
            os.remove(f)
        save(user_thumbnail.image_url, f"{user.name} (UNCOMMON).rng")
    elif stars < 10:
        print(text2art("COMMON", font="small"))
        files = glob.glob('Saved Accounts/*.rng')
        for f in files:
            os.remove(f)
        save(user_thumbnail.image_url, f"{user.name} (COMMON).rng")
        
    print("Username: " + user.name)
    print("ID: " + str(randomid))
    print("Stars: " + str(stars))
    print("Creation Date: " + creationdate)
    print(profile)

if not os.path.isdir('Saved Accounts/'):
    os.mkdir('Saved Accounts')
print("Welcome to the PLAYERRNG.PY")
print("Type 'roll' to ROLL THE DICE!")
print("If you found an interesting account, you can save it by typing 'save'!")
while True:
    user1 = []
    randomid = []
    stars = 0
    reply = input()
    if reply == "exit":
        break
    elif reply == "save":
        file = glob.glob("Saved Accounts/*.rng")[0]
        filename = Path(file).stem
        os.rename(f'Saved Accounts/{filename}.rng', f'Saved Accounts/{filename}.png')
    if messag == 0:
        message = random.randint(1,100)
        if message == 75:
            print("If you found an interesting account, you can save it by typing 'save'!")
            messag = 1
    asyncio.get_event_loop().run_until_complete(main())