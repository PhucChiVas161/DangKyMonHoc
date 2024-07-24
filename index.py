import os
from colorama import Fore
from module.disclaimer import disclaimer
from module.login import login, load_session
from module.display_course_list import display_course_list
from module.register_course import register_course
from module.class_list.class_list import viewTheoryAndPracticeClass, decidePrompt

# from module.display_class_list import display_class_list


def main():
    os.system("cls" if os.name == "nt" else "clear")
    disclaimer()
    session = load_session()
    if session is None:
        session = login()
    else:
        print("Tìm thấy phiên đăng nhập trước đó.")
        choice = input(
            "Chọn 1 để sử dụng phiên đăng nhập trước đó, chọn 2 để đăng nhập mới: "
        )
        if choice == "2":
            session = login()
    while session:
        try:
            course_id, typeId = display_course_list(session)
            viewTheoryAndPracticeClass(session, course_id, typeId)
            url = decidePrompt(typeId)
            register_course(session, url)
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
        except Exception as e:
            print(Fore.RED + f"Lỗi: {e}")
            continue_register = input(
                Fore.YELLOW + "Bạn có muốn đăng ký tiếp không? (y/n): "
            )
            if continue_register.lower() != "y":
                print("Đã thoát chương trình.")
                break


if __name__ == "__main__":
    main()
