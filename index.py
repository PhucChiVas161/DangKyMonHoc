import os
from colorama import Fore
from module.disclaimer import disclaimer
from module.login import login
from module.display_course_list import display_course_list
from module.display_class_list import display_class_list
from module.register_course import register_course


def main():
    os.system("cls" if os.name == "nt" else "clear")
    disclaimer()
    session = login()
    while session:
        course_id, typeId = display_course_list(session)
        url_regist_class_id = display_class_list(session, typeId, course_id)
        register_course(session, url_regist_class_id)
        try:
            continue_register = input(
                Fore.YELLOW + "Bạn có muốn đăng ký tiếp không? (y/n): "
            )
            if continue_register.lower() != "y":
                print("Đã thoát chương trình.")
                break
        except KeyboardInterrupt:
            print("Đã thoát chương trình.")
            break


if __name__ == "__main__":
    main()
