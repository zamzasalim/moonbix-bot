import os, requests, time, crayons, json, threading

def print_banner():
    print(crayons.blue(''))
    print(crayons.blue('   █████████   █████ ███████████   ██████████   ███████████      ███████    ███████████       █████████    █████████    █████████'))
    print(crayons.blue('  ███░░░░░███ ░░███ ░░███░░░░░███ ░░███░░░░███ ░░███░░░░░███   ███░░░░░███ ░░███░░░░░███     ███░░░░░███  ███░░░░░███  ███░░░░░███'))
    print(crayons.blue(' ░███    ░███  ░███  ░███    ░███  ░███   ░░███ ░███    ░███  ███     ░░███ ░███    ░███    ░███    ░███ ░███    ░░░  ███     ░░░'))
    print(crayons.blue(' ░███████████  ░███  ░██████████   ░███    ░███ ░██████████  ░███      ░███ ░██████████     ░███████████ ░░█████████ ░███         '))
    print(crayons.blue(' ░███░░░░░███  ░███  ░███░░░░░███  ░███    ░███ ░███░░░░░███ ░███      ░███ ░███░░░░░░      ░███░░░░░███  ░░░░░░░░███░███         '))
    print(crayons.blue(' ░███    ░███  ░███  ░███    ░███  ░███    ███  ░███    ░███ ░░███     ███  ░███            ░███    ░███  ███    ░███░░███     ███'))
    print(crayons.blue(' █████   █████ █████ █████   █████ ██████████   █████   █████ ░░░███████░   █████           █████   █████░░█████████  ░░█████████'))
    print(crayons.blue(' ░░░░░   ░░░░░ ░░░░░ ░░░░░   ░░░░░ ░░░░░░░░░░   ░░░░░   ░░░░░    ░░░░░░░    ░░░░░           ░░░░░   ░░░░░  ░░░░░░░░░    ░░░░░░░░░  '))
    print(crayons.blue('=============================================='))
    print(crayons.blue('Telegram Channel : @airdropasc               '))
    print(crayons.blue('Telegram Group   : @autosultan_group         '))
    print(crayons.blue('=============================================='))

def log(message, level="INFO"):
    levels = {
        "INFO": crayons.cyan,
        "ERROR": crayons.red,
        "SUCCESS": crayons.green,
        "WARNING": crayons.yellow
    }
    # Print the log message without the timestamp
    print(f"{levels.get(level, crayons.cyan)(level)} | {message}")

class MoonBix:
    def __init__(self, token, proxy=None):
        self.session = requests.session()
        self.session.headers.update({
            'authority': 'www.binance.info',
            'accept': '*/*',
            'accept-language': 'en-EG,en;q=0.9,ar-EG;q=0.8,ar;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'clienttype': 'web',
            'content-type': 'application/json',
            'lang': 'en',
            'origin': 'https://www.binance.info',
            'referer': 'https://www.binance.info/en/game/tg/moon-bix',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        })
        
        if proxy:
            self.session.proxies.update({'http': proxy, 'https': proxy})

        self.token = token
        self.game_response = None

    def login(self):
        try:
            response = self.session.post(
                'https://www.binance.info/bapi/growth/v1/friendly/growth-paas/third-party/access/accessToken',
                json={'queryString': self.token, 'socialType': 'telegram'},
            )
            if response.status_code == 200:
                self.session.headers['x-growth-token'] = response.json()['data']['accessToken']
                log("Logged in success!!", level="SUCCESS")
                return True
            else:
                log("Failed to login", level="ERROR")
                return False
        except Exception as e:
            log(f"Error during login: {e}", level="ERROR")

    def user_info(self):
        try:
            response = self.session.post(
                'https://www.binance.info/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/user/user-info',
                json={'resourceId': 2056},
            )
            return response.json()
        
        except Exception as e:
            log(f"Error during get info: {e}", level="ERROR")

    def game_data(self):
        try:
            while True:
                responses = requests.post('https://app.winsnip.xyz/play', json=self.game_response).text
                try:
                    response = json.loads(responses)
                except json.JSONDecodeError:
                    continue
                if response['message'] == 'success' and response['game']['log'] >= 100:
                    self.game = response['game']
                    return True
        except Exception as e:
            log(f"Error getting game data: {e}", level="ERROR")

    def complete_game(self):
        try:
            response = self.session.post(
                'https://www.binance.info/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/game/complete',
                json={'resourceId': 2056, 'payload': self.game['payload'], 'log': self.game['log']},
            )
            if response.json()['success']:
                log(f"Game completed! Earned + {self.game['log']}", level="SUCCESS")
            return response.json()['success']
        except Exception as e:
            log(f"Error during complete game: {e}", level="ERROR")

    def start_game(self):
        try:
            while True:
                response = self.session.post(
                    'https://www.binance.info/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/game/start',
                    json={'resourceId': 2056},
                )
                self.game_response = response.json()
                if self.game_response['code'] == '000000':
                    log("Game started success!!", level="INFO")
                    return True
                elif self.game_response['code'] == '116002':
                    log('Attempts not enough! Switching to the next account.', level="WARNING")
                    return False
                log("ERROR! Cannot start game.", level="ERROR")
                return False
        except Exception as e:
            log(f"Error during start game: {e}", level="ERROR")

    def start(self):
        if not self.login():
            log("Login failed.", level="ERROR")
            return
        if not self.user_info():
            log("Failed to get user data.", level="ERROR")
            return
        while self.start_game():
            if not self.game_data():
                log("Failed to generate game data!", level="ERROR")
                return
            sleep(45)
            if not self.complete_game():
                log("Failed to complete game", level="ERROR")
            sleep(15)

def sleep(seconds):
    while seconds > 0:
        time_str = time.strftime('%H:%M:%S', time.gmtime(seconds))
        time.sleep(1)
        seconds -= 1
        print(f'\rWaiting {time_str}', end='', flush=True)
    print()

def run_account(index, token, proxy=None):
    log(f"Account {index} |", level="INFO")
    x = MoonBix(token, proxy)
    x.start()
    log(f"Account {index} Done |", level="SUCCESS")
    sleep(15)

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    
    proxies = [line.strip() for line in open('proxy.txt') if line.strip()]
    tokens = [line.strip() for line in open('data.txt')]

    threads = []
    
    for index, token in enumerate(tokens):
        proxy = proxies[index % len(proxies)]  # Cycle through proxies
        thread = threading.Thread(target=run_account, args=(index + 1, token, proxy))
        thread.start()
        threads.append(thread)
        time.sleep(1)  # Adding a slight delay to stagger thread starts

    for thread in threads:
        thread.join()  # Wait for all threads to finish
