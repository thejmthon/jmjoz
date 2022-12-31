import os
import random
import string

JMTHON = "\nJMTHON USERBOT DEPLOY ON VPS"
JMTHON += "\n "
JMTHON += "\n "
JMTHON += "\n★ Channel: @JMTHON ★"
JMTHON += "\n★ Support: @jmthon_support ★"
JMTHON += "\n "
ROZ = "\n "
print(JMTHON)
print(ROZ)
print("WAIT ...")
print(ROZ)

# Update and install dependencies
os.system("sudo apt update && upgrade -y")
os.system("sudo apt install postgresql postgresql-contrib")
os.system("sudo apt install --no-install-recommends -y \\")
os.system("curl \\")
os.system("git \\")
os.system("libffi-dev \\")
os.system("libjpeg-dev \\")
os.system("libwebp-dev \\")
os.system("python3-lxml \\")
os.system("python3-psycopg2 \\")
os.system("libpq-dev \\")
os.system("libcurl4-openssl-dev \\")
os.system("libxml2-dev \\")
os.system("libxslt1-dev \\")
os.system("python3-pip \\")
os.system("python3-sqlalchemy \\")
os.system("openssl \\")
os.system("wget \\")
os.system("python3 \\")
os.system("python3-dev \\")
os.system("libreadline-dev \\")
os.system("libyaml-dev \\")
os.system("gcc \\")
os.system("zlib1g \\")
os.system("ffmpeg \\")
os.system("libssl-dev \\")
os.system("libgconf-2-4 \\")
os.system("libxi6 \\")
os.system("unzip \\")
os.system("libopus0 \\")
os.system("libopus-dev \\")
os.system("python3-venv \\")
os.system("libmagickwand-dev \\")
os.system("pv \\")
os.system("tree \\")
os.system("mediainfo \\")
os.system("nano \\")
os.system("nodejs")
print("⚙️ Github Installer")
print(ROZ)
print(JMTHON)
print(ROZ)
print("Cloning jmthon Userbot")
print(ROZ)
os.system("git clone -b bro https://github.com/thejmthon/sbb_b0")
print(JMTHON)
print(ROZ)
print("runing jmthon now")
print(ROZ)
os.chdir("sbb_b0")

# Rename sample_config.py to config.py
os.rename("jmthon.py", "config.py")
print("⚙️ Environment ")
print(ROZ)

import os
import random

# Generate a random password
password = "".join(random.choices(string.ascii_letters + string.digits, k=32))

# Connect to the PostgreSQL interactive terminal
os.system(f"sudo su - postgres -c 'psql' <<EOF")
os.system(f"ALTER USER postgres WITH PASSWORD '{password}';")
os.system("CREATE DATABASE jmthon;")
os.system("\q")
os.system("exit")
os.system("EOF")

# database
database_url = f"postgresql://postgres:{password}@localhost:5432/jmthon"

# Ask the user for some environment variables and add them to .env
if not os.path.exists(".env"):
    open(".env", "w").close()

alive_name = input("Enter your name:")
app_id = input("Enter app id:")
api_hash = input("Enter your api hash:")
session = input("Enter your session:")
token = input("Enter your bot token:")

with open(".env", "a") as f:
    f.write(f"ALIVE_NAME={alive_name}")
    f.write(f"APP_ID={app_id}")
    f.write(f"API_HASH={api_hash}")
    f.write(f"STRING_SESSION={session}")
    f.write(f"TG_BOT_TOKEN={token}")
    f.write(f"DATABASE_URL={database_url}")

# Run the command in a detached screen
os.system(
    "screen -S jmthon bash -c 'virtualenv venv && source venv/bin/activate && pip3 install -r requirements.txt && clear && python3 -m sbb_b'"
)
