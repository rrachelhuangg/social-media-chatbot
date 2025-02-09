import subprocess

def run_command(username):
    command = f"instaloader --load-cookies chrome {username} {username} --tagged --dirname-pattern posts"
    process = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        print("Command executed successfully.")
        print(stdout.decode())
    else:
        print("Error executing command.")
        print(stderr.decode())