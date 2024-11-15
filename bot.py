import requests
import json
import os
from colorama import *
from datetime import datetime, timedelta, timezone
import time
import pytz

wib = pytz.timezone('Asia/Jakarta')

class MoneyDOGS:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'api.moneydogs-ton.com',
            'Origin': 'https://app.moneydogs-ton.com',
            'Pragma': 'no-cache',
            'Referer': 'https://app.moneydogs-ton.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Money DOGS - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def get_token(self, query: str):
        url = 'https://api.moneydogs-ton.com/sessions'
        data = json.dumps({'encodedMessage':query, 'retentionCode':'48cdRxLi'})
        self.headers.update({
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        })

        response = self.session.post(url, headers=self.headers, data=data)
        data = response.json()
        if response.status_code == 200:
            return data['token']
        else:
            return None
        
    def user_info(self, token: str):
        url = 'https://api.moneydogs-ton.com/mdogs-deposits'
        self.headers.update({
            'Content-Length': '0',
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        })

        response = self.session.get(url, headers=self.headers)
        data = response.json()
        if response.status_code == 200:
            return data
        else:
            return None
        
    def daily_checkin(self, token: str):
        url = 'https://api.moneydogs-ton.com/daily-check-in'
        self.headers.update({
            'Content-Length': '0',
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        })

        response = self.session.post(url, headers=self.headers)
        data = response.json()
        if response.status_code == 200:
            return data
        else:
            return None
        
    def get_tasks(self, token: str, task_type: str = 'all'):
        base_url = 'https://api.moneydogs-ton.com/tasks'
        url = f"{base_url}?isFeatured=true" if task_type == 'featured' else base_url
        self.headers.update({
            'Content-Length': '0',
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        })

        response = self.session.get(url, headers=self.headers)
        data = response.json()
        if response.status_code == 200:
            return data
        else:
            return None
        
    def complete_tasks(self, token: str, task_id: str):
        url = f'https://api.moneydogs-ton.com/tasks/{task_id}/verify'
        self.headers.update({
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        })

        response = self.session.post(url, headers=self.headers)
        if response.status_code in [200, 201]:
            return True
        else:
            return None
        
    def process_query(self, query: str):
        token = self.get_token(query)
        if not token:
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT} Query ID Isn't Valid {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
            )
            return

        if token:
            user = self.user_info(token)
            if user:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {user['user']['firstName']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {user['remainingAmount']:.4f} $MDOGS {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )
                time.sleep(2)

                checkin = self.daily_checkin(token)
                if checkin:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Check-in{Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {checkin['rewardMdogs']} $MDOGS {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                else:
                    now = datetime.now(timezone.utc)
                    checkin_time = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(wib).strftime('%x %X %Z')
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Check-in{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Not Time to Claim {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [ Next Claim at{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {checkin_time} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(2)

                for type in ['featured', 'all']:
                    tasks = self.get_tasks(token, type)
                    if tasks is not None:
                        for task in tasks:
                            task_id = str(task['id'])

                            if task is not None:
                                verify = self.complete_tasks(token, task_id)
                                if verify:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {task['title']} {Style.RESET_ALL}"
                                        f"{Fore.GREEN + Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {task['rewardMdogs']:.1f} $MDOGS {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {task['title']} {Style.RESET_ALL}"
                                        f"{Fore.RED + Style.BRIGHT}Isn't Completed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                time.sleep(1)
                    else:
                        if tasks == 'featured':
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Partner Tasks{Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT} Is Completed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ General Tasks{Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT} Is Completed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                            )
            else:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )
            
    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                for query in queries:
                    query = query.strip()
                    if query:
                        self.process_query(query)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                        time.sleep(3)

                seconds = 1800
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    time.sleep(1)
                    seconds -= 1

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Money DOGS - BOT{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    moneydogs = MoneyDOGS()
    moneydogs.main()