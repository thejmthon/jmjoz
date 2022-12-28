import os

def clear():
    os.system("clear")

def jmthon():
    print("NOW PUT YOUR VARS CORRECTLY")
    with open(".env", "w") as file:
        for var in [
            "ALIVE_NAME",
            "APP_ID",
            "API_HASH",
            "STRING_SESSION",
            "DATABASE_URL",
            "TG_BOT_TOKEN",
            "TZ",
        ]:
            inpr = input(f"Enter {var}: ")
            file.write(f"{var}={inpr}\n")
    print("* Created '.env' file successfully *")
    os.system("screen -S jmthon")
    os.system("python3 -m sbb_b")

clear()
jmthon()
