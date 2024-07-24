import os
import time
import pickle
import requests
from colorama import Fore
from getpass import getpass
from module.random_fact import random_fact

SESSION_FILE = "login_session.pkl"
SESSION_EXPIRATION_TIME = 1800  # 30 minutes


def save_session(session):
    with open(SESSION_FILE, "wb") as f:
        pickle.dump(session, f)
    print(Fore.GREEN + "Phiên đăng nhập đã được lưu.")


def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "rb") as f:
            session = pickle.load(f)
        if time.time() - os.path.getmtime(SESSION_FILE) < SESSION_EXPIRATION_TIME:
            print(Fore.GREEN + "Đang sử dụng phiên đăng nhập trước đó.")
            return session
        else:
            os.remove(SESSION_FILE)
            print(Fore.YELLOW + "Phiên đăng nhập đã hết hạn. Cần đăng nhập lại.")
    return None


def login():
    while True:
        USER_NAME = input(Fore.BLUE + "Nhập MSSV: ")
        PASSWORD = getpass(
            Fore.BLUE + "Nhập mật khẩu(Khi nhập sẽ không hiện ra mật khẩu để bảo mật): "
        )
        url = "https://regist.vlu.edu.vn"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"username": USER_NAME, "password": PASSWORD}
        session = requests.Session()
        while True:
            print(Fore.YELLOW + f"Đang đăng nhập...-{random_fact()}")
            response = session.post(
                url, headers=headers, data=data, allow_redirects=False
            )
            if response.status_code == 302:
                print(Fore.GREEN + "Đăng nhập thành công")
                save_session(session)
                return session
            elif response.status_code == 500:
                print(Fore.RED + f"Lỗi server, đang thử lại...-{random_fact()}")
                time.sleep(1)
            else:
                print(
                    Fore.RED + "Đăng nhập thất bại. Hoặc đăng không mở đăng ký môn học."
                )
                try_again = input(
                    Fore.YELLOW + "Bạn có muốn đăng nhập lại không? (y/n): "
                )
                if try_again.lower() != "y":
                    print(Fore.MAGENTA + "Đã thoát chương trình.")
                    return None
