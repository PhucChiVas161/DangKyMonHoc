from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
import os
import json
import time
import random
import tkinter as tk
from tkinter import ttk


def disclaimer():
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


def login():
    while True:
        USER_NAME = input("Nhập MSSV")
        PASSWORD = input("Nhập mật khẩu")
        print(USER_NAME)
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
        with open("FACT.txt", "r", encoding="utf-8") as file:
            facts = file.readlines()
        random_fact = random.choice(facts)
        print(f"Đang đăng nhập...-{random_fact.strip()}")
        if response.status_code == 302:
            print('Đăng nhập thành công')
            # Lưu cookie vào session
            session.cookies.update(response.cookies)
            return session
        else:
            print('Đăng nhập thất bại. Hoặc đăng không mở đăng ký môn học.')
            try_again = input('Bạn có muốn đăng nhập lại không? (y/n): ')
            if try_again.lower() != 'y':
                print('Đã thoát chương trình.')
                return None


def display_course_list(session, typeId):
    with open("FACT.txt", "r", encoding="utf-8") as file:
        facts = file.readlines()
    random_fact = random.choice(facts)
    while True:
        response = session.get(
            f"https://regist.vlu.edu.vn/DangKyHocPhan/DanhSachHocPhan?typeId={typeId}&id=")
        print(
            f"Đang lấy thông tin các môn học...-{random_fact.strip()}")
        if response.status_code == 500:
            print(f"Server lỗi, đang thử lại...-{random_fact.strip()}")
            time.sleep(3)
        else:
            break
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    data = []
    for row in rows[1:]:  # Bỏ qua hàng tiêu đề
        cells = row.find_all('td')
        row_data = [cell.get_text(strip=True) for cell in cells[:5]]
        # Lấy đoạn mã từ thẻ <a>
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
    headers = ['STT', 'Mã học phần', 'Tên học phần',
               'STC', 'Số lượng LHP', 'Mã lớp']
    print(tabulate(data, headers, tablefmt='fancy_grid'))


def choice_cousre(session, typeId):
    course_code = input("Nhập mã lớp ở bảng trên: ")

    with open("FACT.txt", "r", encoding="utf-8") as file:
        facts = file.readlines()
    random_fact = random.choice(facts)
    print(f"Đang lấy thông tin các lớp học ... -{random_fact.split()}")
    while True:
        response = session.get(
            f"https://regist.vlu.edu.vn/DangKyHocPhan/DanhSachLopHocPhan?id={course_code}&registType={typeId}&scheduleStudyUnitID=")
        if response.status_code == 500:
            print(f"Server lỗi, đang thử lại...-{random_fact.split()}")
            time.sleep(3)
        else:
            break
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    tbody = table.find('tbody')
    trCount = tbody.find_all(recursive=False)
    for i in range(0, len(trCount)):
        row = trCount[i]
        if (i % 2 == 0):
            data = []
            cells = row.find_all('td')
            row_data = [cell.get_text(strip=True)
                        for cell in cells if not cell.find('span') and cell.get_text(strip=True) != '']
            del row_data[2]
            inputTag = row.find('input')
            if (inputTag):
                row_data.append(inputTag.get('id'))
            else:
                row_data.append('null')
            data.append(row_data)
            if (len(row_data) == 6):
                headers = ['Loại', 'Mã LHP', 'Số lượng',
                           'Lịch học', 'Ghi chú', 'ID lớp lý thuyết']
            else:
                headers = ['Loại', 'Mã LHP', 'Số lượng',
                           'Lịch học', 'ID lớp lý thuyết']
            print('\n Bảng lý thuyết:')
            print(tabulate(data, headers=headers, tablefmt='fancy_grid'))
        else:
            cells = row.find_all('tr')  # ! td[]
            data = []
            for t in cells[1:]:
                tds = t.find_all('td')
                row_data = []
                for tdi in range(0, len(tds)):
                    tde = tds[tdi]
                    if (tdi == 0):
                        inp = tde.find('input')
                        if inp:
                            id_attr = inp.get('id')
                            row_data.append(id_attr)
                    else:
                        row_data.insert(tdi-1, tde.getText(strip=True))
                row_data_no_empty = list(filter(None, row_data))
                data.append(row_data_no_empty)
            if (len(row_data_no_empty) == 5):
                headers2 = ["Mã LHP", "SL còn lại",
                            "Lịch học", "Ghi chú", 'ID lớp thực hành']
            else:
                headers2 = ["Mã LHP", "SL còn lại",
                            "Lịch học", 'ID lớp thực hành']
            print('\n Bảng thực hành:')
            print(tabulate(data, headers=headers2, tablefmt='mixed_grid'))


def register_course(session, typeId):
    course_code = input("Nhập Code cần đăng ký: ")
    response = session.get(
        f"https://regist.vlu.edu.vn/DangKyHocPhan/DangKy?Hide={course_code}|&acceptConflict=false&classStudyUnitConflictId=&RegistType={typeId}&ScheduleStudyUnitID=")
    text = response.text
    json_server = json.loads(text)
    msg = json_server['Msg']
    print(msg)


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    disclaimer()
    session = login()
    while session:
        print("Lựa chọn:")
        print("1. Kế hoạch (KH)")
        print("2. Ngoài kế hoạch (NKH)")
        choice = input("Chọn (1/2): ")
        if choice == "1":
            typeId = "KH"
        elif choice == "2":
            typeId = "NKH"
        display_course_list(session, typeId)
        choice_cousre(session, typeId)
        register_course(session, typeId)
        try:
            continue_register = input(
                "Bạn có muốn đăng ký tiếp không? (y/n): ")
            if continue_register.lower() != 'y':
                print("Đã thoát chương trình.")
                break
        except KeyboardInterrupt:
            print("Đã thoát chương trình.")
            break


if __name__ == "__main__":
    main()
