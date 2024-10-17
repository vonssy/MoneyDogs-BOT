import requests
import json
import os
from colorama import *
from datetime import datetime
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
        data = json.dumps({ 'encodedMessage': query })
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
        url = 'https://api.moneydogs-ton.com/rankings/deposits/me'
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
        
    def get_tasks(self, token: str):
        url = 'https://api.moneydogs-ton.com/tasks'
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
        if response.status_code == 201:
            return True
        elif response.status_code == 200:
            try:
                data = response.json()
                return data
            except ValueError:
                return True
        else:
            return False
        
    def process_query(self, query: str):
        token = self.get_token(query)

        user_info = self.user_info(token)
        if user_info:
            first_name = user_info['firstName']
            balance = f"{user_info['score']:.4f}"
            self.log(
                f"{Fore.CYAN + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {first_name} {Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT}] {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}[ Balance{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {balance} MDOGS {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
            )
        else:
            self.log(f"[ User Not Found ]")

        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.YELLOW + Style.BRIGHT}[ Get Daily Check-in... ]{Style.RESET_ALL}",
            end="\r",
            flush=True
        )
        time.sleep(1.5)
        checkin = self.daily_checkin(token)
        if checkin:
            reward = checkin['rewardMdogs']
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Check-in{Style.RESET_ALL}"
                f"{Fore.GREEN + Style.BRIGHT} Success {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {reward} MDOGS {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
            )
        else:
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Check-in{Style.RESET_ALL}"
                f"{Fore.YELLOW + Style.BRIGHT} Already Check-in Today {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}      "
            )

        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.YELLOW + Style.BRIGHT}[ Get Available Tasks... ]{Style.RESET_ALL}",
            end="\r",
            flush=True
        )
        time.sleep(1.5)
        tasks = self.get_tasks(token)
        manual_task = False
        if tasks:
            for task in tasks:
                task_id = task['id']
                title = task['title']

                if task['code'] is None:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Task{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}is Strarting...{Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                    complete_task = self.complete_tasks(token, task_id)

                    if complete_task:
                        reward = int(task['rewardMdogs'])
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Task{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}is Completed{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {reward} MDOGS {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}          "
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Task{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT}is Failed{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}                          "
                        )
                else:
                    manual_task = True

            if manual_task:
                self.log(f"{Fore.YELLOW + Style.BRIGHT}[ Tersisa Manual Task ]{Style.RESET_ALL}                       ")
            
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
                self.log(f"{Fore.CYAN + Style.BRIGHT}-----------------------------------------------------------------------{Style.RESET_ALL}")

                for query in queries:
                    query = query.strip()
                    if query:
                        print(f"{Fore.YELLOW+Style.BRIGHT}[ Getting User Query... ]{Style.RESET_ALL}", end="\r", flush=True)
                        time.sleep(1.5)
                        self.process_query(query)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-----------------------------------------------------------------------{Style.RESET_ALL}")

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