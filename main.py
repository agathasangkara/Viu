try:
    import requests as r
    import os
    from datetime import datetime
    import random
    import concurrent.futures as t
    from faker import Faker
    from colorama import Fore as F, init
except Exception:
    os.system("pip install requests faker colorama")

init(autoreset=True)

HOST = "https://chsangkara.my.id/viu/"

CONFIG = {
    "Author"   : "Agatha sangkara",
    "Github"   : "https://github.com/agathasangkara",
    "Version"  : "VIU 2.0",
    "Domain"   : "k.com",
    "Password" : "chsangkara",
    "Nomor"    : "628xxxxx",
    "Thread"   : 10,
    "Proxies"  : True
}

HEADERS = {
    "X-Apikey" : "chsangkara"
}

class Viu:
    
    def __init__(self, token=None, **kwargs) -> None:
        self.session = r.Session()
        self.domain = CONFIG['Domain']
        self.apikey = HEADERS['X-Apikey']
    
    def load_proxies(self):
        proxy_file = "proxies.txt"
        if not os.path.isfile(proxy_file):
            return []
        
        with open(proxy_file, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        
        return proxies
    
    def create_account(self, nomor: str, proxyless: int):
        query = {
            "nomor": nomor
        }

        if proxyless == 1:
            proxy_list = self.load_proxies()
            if not proxy_list:
                print(F.RED + "Proxy list is empty or file not found.")
                exit()
            
            proxy = random.choice(proxy_list)
            query['proxy'] = proxy
        
        create = self.session.get(
            HOST + "create",
            params=query,
            headers=HEADERS
        ).json()
        if create['success']:
            token = create['token']
            None
        else:
            print("\n" + F.RED + create['message'])
            exit(0)
        
        del query['nomor']
        HEADERS['Content-Type'] = 'application/x-www-form-urlencoded'
        data = {
            "token" : token
        }
        profile = self.session.post(
            HOST + "profile",
            data=data,
            params=query,
            headers=HEADERS
        ).json()
        if profile['data']['paymentStatus'] != "free":
            tokenv2 = profile['data']['token']
        else:
            print(F.YELLOW + nomor + F.WHITE + " => Paket :  " + F.RED + profile['data']['paymentStatus'])
            exit(0)
            
        data = {
            "token":tokenv2,
            "email":Faker("ID_id").name().replace(' ',"").replace(",","").replace(".","").lower() + str(random.randint(100,999)) + "@" + self.domain,
            "password":CONFIG["Password"],
            "name":Faker("ID_id").name().replace(' ',"").replace(",","").replace(".","").lower()
        }
        premium = self.session.post(
            HOST + "upgrade",
            data=data,
            params=query,
            headers=HEADERS
        ).json()
        if premium['success']:
            None
        else:
            print(F.RED + premium['message'])
            exit(0)
            
            
        data = {
            "token" : tokenv2
        }
        status = self.session.post(
            HOST + "profile",
            data=data,
            params=query,
            headers=HEADERS
        ).json()
        if status['success']:
            ts_exp = status['data']['plan']['partners'][0]['endDate'] / 1000
            exp = datetime.utcfromtimestamp(ts_exp).strftime('%d %B %Y')
            print(f"Email : {F.YELLOW}{status['data']['user']['username']}\n{F.RESET}Paket : {F.GREEN}{status['data']['additionalInfo']['offerId']}{F.WHITE}\nExp   : {F.GREEN}{exp}\n")
            with open("accounts_viu.txt", "a") as f:
                f.write(f"{status['data']['user']['username']}|{exp}\n")
        else:
            print(F.YELLOW + nomor + F.WHITE + " => Paket :  " + F.RED + status['data']['paymentStatus'] + "\n")

     
os.system('cls' if os.name == "nt" else 'clear')
print(f'''{F.YELLOW}
.;.       .-..-.
 `;     .'   `-'   ,  :
 ;;  .'    ;'    ;   ;
 ;;  ;   _.;:._..'`..:;._  {F.WHITE}https://t.me/chsangkara{F.YELLOW}
 `;.'
''')
index = Viu()
nomor = CONFIG['Nomor']
proxyless = int(input("1. Proxies (Use Proxy)\n2. Proxyless(Without Proxy)\n\nChoice : "))
print("\nPlease wait for your request to be processed !\n")
with t.ThreadPoolExecutor(max_workers=CONFIG['Thread']) as exec:
        t.wait([exec.submit(index.create_account, nomor, proxyless) for _ in range(CONFIG['Thread'])])

