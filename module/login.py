import requests
from colorama import Fore
from getpass import getpass
from module.random_fact import random_fact


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
        response = session.post(url, headers=headers, data=data, allow_redirects=False)
        print(Fore.YELLOW + f"Đang đăng nhập...-{random_fact()}")
        if response.status_code == 302:
            print(Fore.GREEN + "Đăng nhập thành công")
            # Lưu cookie vào session
            session.cookies.update(response.cookies)
            return session
        else:
            print(Fore.RED + "Đăng nhập thất bại. Hoặc đăng không mở đăng ký môn học.")
            try_again = input(Fore.YELLOW + "Bạn có muốn đăng nhập lại không? (y/n): ")
            if try_again.lower() != "y":
                print(Fore.MAGENTA + "Đã thoát chương trình.")
                return None
