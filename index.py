from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
import os
import json
import time
import random
from colorama import Fore, Back, Style
from getpass import getpass


def disclaimer():
    print(Style.BRIGHT + Back.MAGENTA)
    print('****************************************************************************************************************************************************************************')
    print('*                                                                          Tuyên bố miễn trừ trách nhiệm                                                                   *')
    print('*                                          Mục đích: Công cụ này được phát triển nhằm mục đích hỗ trợ sinh viên đăng ký môn học trực tuyến.                                *')
    print('*                                                Trách nhiệm: Mình không chịu bất kỳ trách nhiệm nào về kết quả đăng ký của sinh viên.                                     *')
    print('*Cách thức hoạt động: Công cụ hoạt động bằng cách truy cập vào hệ thống đăng ký trực tuyến của trường. Tuy nhiên, việc xử lý cuối cùng vẫn do hệ thống của trường thực hiện*')
    print('*                                           Miễn trừ trách nhiệm: Mình không chịu trách nhiệm về bất kỳ sai sót hoặc hậu quả có thể xảy ra.                                *')
    print('*                                              Trách nhiệm của người dùng: Sinh viên cần tự kiểm tra kết quả trên hệ thống của trường.                                     *')
    print('*                                                                Liên hệ: Mọi thắc mắc vui lòng liên hệ mình.                                                              *')
    print('*                                                                       Tác giả: PhúcChiVas và Đỗ Huy                                                                      *')
    print('*                                                     Donate CF và phát triển thêm tool : Momo (0931323078) (Dương Ngọc Phúc)                                              *')
    print('****************************************************************************************************************************************************************************')
    print(Back.RESET + Style.RESET_ALL)


def random_fact():
    with open("FACT.txt", "r", encoding="utf-8") as file:
        facts = file.readlines()
        return random.choice(facts).strip()


def login():
    while True:
        USER_NAME = input(Fore.BLUE + 'Nhập MSSV: ')
        PASSWORD = getpass(
            Fore.BLUE + 'Nhập mật khẩu(Khi nhập sẽ không hiện ra mật khẩu để bảo mật): ')
        url = "https://regist.vlu.edu.vn"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "username": USER_NAME,
            "password": PASSWORD
        }
        session = requests.Session()
        response = session.post(url, headers=headers,
                                data=data, allow_redirects=False)
        print(Fore.YELLOW + f"Đang đăng nhập...-{random_fact()}")
        if response.status_code == 302:
            print(Fore.GREEN + 'Đăng nhập thành công')
            # Lưu cookie vào session
            session.cookies.update(response.cookies)
            return session
        else:
            print(Fore.RED + 'Đăng nhập thất bại. Hoặc đăng không mở đăng ký môn học.')
            try_again = input(
                Fore.YELLOW + 'Bạn có muốn đăng nhập lại không? (y/n): ')
            if try_again.lower() != 'y':
                print(Fore.MAGENTA + 'Đã thoát chương trình.')
                return None


def display_course_list(session, typeId):
    while True:
        response = session.get(
            f"https://regist.vlu.edu.vn/DangKyHocPhan/DanhSachHocPhan?typeId={typeId}&id=")
        print(Fore.YELLOW +
              f"Đang lấy thông tin các môn học...-{random_fact()}")
        if response.status_code != 200:
            print(Fore.RED +
                  f"Server lỗi, đang thử lại...-{random_fact()}")
            time.sleep(3)
        else:
            break
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    data = []
    selected_row = None
    for row in rows[1:]:
        cells = row.find_all('td')
        row_data = [cell.get_text(strip=True) for cell in cells[:5]]
        link = row.find('a')
        if link:
            href = link.get('href')
            start_index = href.index("('") + 2
            end_index = href.index("',")
            class_id = href[start_index:end_index]
            row_data.append(class_id)
        else:
            row_data.append('')
        data.append(row_data)
    headers = ['STT', 'STT (Đừng quan tâm)', 'Mã học phần', 'Tên học phần',
               'STC', 'Số lượng LHP']
    print(Fore.LIGHTCYAN_EX + (tabulate(data, headers,
          tablefmt='fancy_grid', showindex="always")))
    row_number = int(input("Nhập STT môn học cần đăng ký: "))
    selected_row = data[row_number]
    class_id = selected_row[-1]
    return class_id


def choice_cousre(session, typeId, class_id):
    print(Fore.YELLOW + f"Đang lấy thông tin các lớp học ... -{random_fact()}")
    while True:
        response = session.get(
            f"https://regist.vlu.edu.vn/DangKyHocPhan/DanhSachLopHocPhan?id={class_id}&registType={typeId}&scheduleStudyUnitID=")
        if response.status_code != 200:
            print(Fore.RED +
                  f"Server lỗi, đang thử lại...-{random_fact()}")
            time.sleep(3)
        else:
            break
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr', class_='')
    data = []
    for row in rows[1:]:  # Bỏ qua hàng tiêu đề
        cells = row.find_all('td')
        row_data = [cell.get_text(strip=True)
                    for cell in cells if not cell.find('span')]
        link = row.find('input')
        if link:
            id_attr = link.get('id')
            row_data.append(id_attr)
        data.append(row_data)
    ly_thuyet = []
    thuc_hanh = []
    thi = []
    for item in data:
        if item and item[1] == 'Lý thuyết':
            del item[0]
            del item[2]
            del item[4]
            ly_thuyet.append(item)
        elif item and item[1] == 'Thi':
            del item[0]
            del item[4]
            del item[4]
            del item[4]
            thi.append(item)
        elif item and item[0] == '':
            del item[0]
            thuc_hanh.append(item)

    table = 'fancy_grid'
    # Xuất bảng cho lý thuyết
    if ly_thuyet:
        headers = ["STT", "Loại", "Mã LHP",
                   "SL còn lại", "Lịch Học", "Ghi Chú", "Code lớp"]
        print(Style.BRIGHT + Fore.GREEN + "Bảng Lý thuyết:")
        print(Style.NORMAL + Fore.GREEN +
              (tabulate(ly_thuyet, headers=headers, tablefmt=table, showindex=True)))

    # Xuất bảng cho thực hành
    if thuc_hanh:
        headers2 = ["STT", "Mã lớp", "SL", 'Lịch Học', 'Ghi chú', 'Code lớp']
        print(Style.BRIGHT + Fore.BLUE + "\nBảng Thực hành:")
        print(Style.NORMAL + Fore.BLUE +
              (tabulate(thuc_hanh, headers=headers2, tablefmt=table, showindex=True)))

    if thi:
        headers3 = ["STT", 'Loại', 'Mã LHP', 'Lớp sinh hoạt',
                    'SL', 'Ghi chú', 'ID Lớp học']
        print(Style.NORMAL + Fore.CYAN +
              (tabulate(thi, headers=headers3, tablefmt=table, showindex=True)))


def register_course(session, typeId):
    course_code = input(Fore.BLUE + "Nhập ID lớp cần đăng ký " + Fore.YELLOW + Style.BRIGHT +
                        "(Nếu môn nào có lớp thực thành thì nhập 2 mã liên tiếp cách nhau bởi dấu '|'. Ví dụ 'ID Lý thuyết|ID thực hành' ):")
    print(Style.RESET_ALL)
    response = session.get(
        f"https://regist.vlu.edu.vn/DangKyHocPhan/DangKy?Hide={course_code}|&acceptConflict=false&classStudyUnitConflictId=&RegistType={typeId}&ScheduleStudyUnitID=")
    text = response.text
    json_server = json.loads(text)
    msg = json_server['Msg']
    print(Fore.GREEN + Style.BRIGHT + f'{msg}')


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    disclaimer()
    session = login()
    while session:
        print(Fore.BLUE + "Lựa chọn:")
        print(Fore.BLUE + "1. Kế hoạch (KH)")
        print(Fore.BLUE + "2. Ngoài kế hoạch (NKH)")
        choice = input(Fore.BLUE + "Chọn (1/2): ")
        if choice == "1":
            typeId = "KH"
        elif choice == "2":
            typeId = "NKH"
        class_id = display_course_list(session, typeId)
        choice_cousre(session, typeId, class_id)
        register_course(session, typeId)
        try:
            continue_register = input(Fore.YELLOW +
                                      "Bạn có muốn đăng ký tiếp không? (y/n): ")
            if continue_register.lower() != 'y':
                print("Đã thoát chương trình.")
                break
        except KeyboardInterrupt:
            print("Đã thoát chương trình.")
            break


if __name__ == "__main__":
    main()
