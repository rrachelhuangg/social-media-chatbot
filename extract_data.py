import subprocess
import os
import asyncio

USERNAME = ""

async def download_followers(username):
    followed_directory = "followed"
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
        hashtag = ht.strip().lower()
        command = f'instaloader --load-cookies chrome {USERNAME} "#{hashtag}" --dirname-pattern {ht}'
        try:
            process = await asyncio.create_subprocess_shell(command, shell = True, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout = 30)
            print("Process completed successfully.")
        except asyncio.TimeoutError:
            process.kill()
            print("Process was killed.")
