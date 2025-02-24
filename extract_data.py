import subprocess
import os
import asyncio

async def download_general(username):
    #want metadata though
    directories = {
    "followed":f"instaloader --load-cookies chrome {username} @{username} --no-posts --no-profile-pic --no-metadata-json --dirname-pattern followed",
    "stories": f"instaloader --load-cookies chrome {username} :stories --dirname-pattern stories",
    "saved": f"instaloader --load-cookies chrome {username} :saved --dirname-pattern saved"
    }
    for dir in directories:
        if not os.path.isdir(dir):
            os.mkdir(dir)
            command = directories[dir]
            if dir in ["saved"]:
                try:
                    process = await asyncio.create_subprocess_shell(command, shell = True, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = await asyncio.wait_for(process.communicate(), timeout = 30)
                except asyncio.TimeoutError:
                    process.kill()
            else:
                process = await asyncio.create_subprocess_shell(command, shell = True, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = await process.communicate()
                if dir == "followed":
                    with open("followed.txt","w") as f:
                        for file_name in os.listdir(dir):
                            f.write(file_name[:-3]+"\n")

# async def download_hashtags(hashtags):
#     hashtag_list = hashtags.split(",")
#     for ht in hashtag_list:
#         if not os.path.isdir(ht):
#             hashtag = ht.strip().lower()
#             command = f'instaloader --load-cookies chrome {USERNAME} "#{hashtag}" --dirname-pattern {ht}'
#             try:
#                 process = await asyncio.create_subprocess_shell(command, shell = True, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
#                 stdout, stderr = await asyncio.wait_for(process.communicate(), timeout = 30)
#                 print("Process completed successfully.")
#             except asyncio.TimeoutError:
#                 process.kill()
#                 print("Process was killed.")