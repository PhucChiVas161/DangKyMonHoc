from colorama import Style, Fore
import json
import time


def register_course(session, url_regist_class_id):
    user_asked = False
    continue_register = True
    while continue_register:
        print(Style.RESET_ALL)
        response = session.get(url_regist_class_id)

        # If server response is 200, print the message and check its content
        if response.status_code == 200:
            json_server = json.loads(response.text)
            msg = json_server["Msg"]
            if msg == "Đăng ký thành công ...":
                print(Fore.GREEN + Style.BRIGHT + f"{msg}")
                break
            else:
                print(Fore.YELLOW + Style.BRIGHT + f"{msg}")
                time.sleep(0.2)
                if (
                    not user_asked
                ):  # Hỏi người dùng chỉ một lần nếu điều kiện không thỏa mãn
                    ask_user = (
                        input("Bạn có muốn đăng ký lại không? (y/n): ").strip().lower()
                    )
                    user_asked = True
                    if ask_user == "phuc":
                        continue_register = True  # Tiếp tục vòng lặp vô hạn
                    elif ask_user == "y":
                        continue_register = (
                            True  # Tiếp tục vòng lặp và sẽ hỏi lại sau mỗi lần thất bại
                        )
                    elif ask_user == "n":
                        continue_register = False  # Không tiếp tục vòng lặp
                else:
                    if ask_user == "y":  # Nếu người dùng chọn 'y', tiếp tục hỏi lại
                        ask_user = (
                            input("Bạn có muốn đăng ký lại không? (y/n): ")
                            .strip()
                            .lower()
                        )
                        if ask_user == "n":
                            continue_register = False
                        elif ask_user == "phuc":
                            continue_register = True
        else:
            print(
                Fore.RED
                + Style.BRIGHT
                + "Đã xảy ra lỗi khi đăng ký lớp học. Đang thử lại.",
                response.text,
            )
            # Delay for a short time before trying again
            time.sleep(1)
