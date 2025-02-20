import subprocess
import os
import asyncio

USERNAME = ""

async def download_followers(username):
    followed_directory = "followed"
    stories_directory = "stories"
    followed_usernames = "followed.txt"
    USERNAME = username
    #takes ~3 minutes right now to download all 1007 usernames followed and output to txt file
    if not os.path.isdir(followed_directory):
        os.mkdir(followed_directory)
        command = f"instaloader --load-cookies chrome {username} @{username} --no-posts --no-profile-pic --no-metadata-json --dirname-pattern {followed_directory}"
        process = await asyncio.create_subprocess_shell(command, shell = True, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = await process.communicate()
        with open(followed_usernames,"w") as f:
            for file_name in os.listdir(followed_directory):
                f.write(file_name[:-3]+"\n")
    
async def download_hashtags(hashtags):
    hashtag_list = hashtags.split(",")
    for ht in hashtag_list:
        if not os.path.isdir(ht):
            hashtag = ht.strip().lower()
            command = f'instaloader --load-cookies chrome {USERNAME} "#{hashtag}" --dirname-pattern {ht}'
            try:
                process = await asyncio.create_subprocess_shell(command, shell = True, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout = 30)
                print("Process completed successfully.")
            except asyncio.TimeoutError:
                process.kill()
                print("Process was killed.")

async def download_stories():
    #want metadata json right? with location data and a bunch of other extra info that can come in handy later - try to 
    #get as much info as possible
    stories_directory = "stories"
    if not os.path.isdir(stories_directory):
        os.mkdir(stories_directory)
        command = f"instaloader --load-cookies chrome {USERNAME} :stories --dirname-pattern {stories_directory}"
        process = await asyncio.create_subprocess_shell(command, shell = True, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = await process.communicate()

async def download_saved():
    #need to group captions and each post's pictures together to sort..
    saved_directory = "saved"
    if not os.path.isdir(saved_directory):
        os.mkdir(saved_directory)
        command = f"instaloader --load-cookies chrome {USERNAME} :saved --dirname-pattern {saved_directory}"
        try:
            process = await asyncio.create_subprocess_shell(command, shell = True, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout = 30)
            print("Process completed successfully.")
        except asyncio.TimeoutError:
            process.kill()
            print("Process was killed.")
