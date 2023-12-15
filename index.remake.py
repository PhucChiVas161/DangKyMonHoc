from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
# from dotenv import load_dotenv
import os
import json
import time

# load_dotenv()


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


def login(username, password):
    url = "https://regist.vlu.edu.vn"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "username": username,
        "password": password
    }

    session = requests.Session()

    response = session.post(url, headers=headers,
                            data=data, allow_redirects=False)

    if response.status_code == 302:
        print('Đăng nhập thành công')
        # Lưu cookie vào session
        session.cookies.update(response.cookies)
        return session
    else:
        print('Đăng nhập thất bại. Hoặc không trong thời gian đăng ký')
        return None


def display_course_list(session):
    print("Lựa chọn:")
    print("1. Kế hoạch (KH)")
    print("2. Ngoài kế hoạch (NKH)")

    choice = input("Chọn (1/2): ")

    if choice == "1":
        typeId = "KH"
    elif choice == "2":
        typeId = "NKH"

    response = session.get(f"https://regist.vlu.edu.vn/DangKyHocPhan/DanhSachHocPhan?typeId={typeId}&id="
                           )

    if response.status_code == 500:
        print("Hệ thống đang gặp vấn đề. Vui lòng thử lại sau :)))))")
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')

        data = []
        for row in rows[1:]:  # Bỏ qua hàng tiêu đề
            cells = row.find_all('td')
            row_data = [cell.get_text(strip=True) for cell in cells]

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
                   'STC', 'Số lượng LHP', 'Mã lớp', 'Code lớp']
        print(tabulate(data, headers, tablefmt='grid'))


def choice_cousre(session):
    course_code = input("Nhập code: ")
    response = session.get(
        f"https://regist.vlu.edu.vn/DangKyHocPhan/DanhSachLopHocPhan?id={course_code}&registType=NKH&scheduleStudyUnitID=")
    if response.status_code == 500:
        print("Hệ thống đang gặp vấn đề. Vui lòng thử lại sau :)))))")
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')

        data = []
        for row in rows[1:]:  # Bỏ qua hàng tiêu đề
            cells = row.find_all('td')
            row_data = [cell.get_text(strip=True) for cell in cells]

            # Lấy đoạn mã từ thẻ <input>
            link = row.find('input')
            if link:
                id_attr = link.get('id')
                row_data.append(id_attr)
            else:
                row_data.append('')

            data.append(row_data)

        headers = ["STT", "Loai", "Mã LHP",
                   "Lớp sinh hoạt", "SL còn lại", "Lịch học", "Số tiền", "Ghi chú", "Code lớp"]
        print(tabulate(data, headers, tablefmt='grid'))


def register_course(session):
    course_code = input("Nhập Code cần đăng ký: ")
    response = session.get(
        f"https://regist.vlu.edu.vn/DangKyHocPhan/DangKy?Hide={course_code}|&acceptConflict=false&classStudyUnitConflictId=&RegistType=NKH&ScheduleStudyUnitID=")
    text = response.text
    json_server = json.loads(text)
    msg = json_server['Msg']
    print(msg)


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    disclaimer()
    # USER_NAME = os.getenv("USER_NAME")
    # PASSWORD = os.getenv("PASSWORD")
    # USER_NAME = input('Nhập MSSV: ')
    # PASSWORD = input('Nhập mật khẩu: ')
    USER_NAME = '207CT40540'
    PASSWORD = '16012002'
    session = login(USER_NAME, PASSWORD)
    if session:
        display_course_list(session)
        choice_cousre(session)
        register_course(session)

    while True:
        try:
            print("Nhấn Ctrl + C để thoát")
            time.sleep(30)
        except KeyboardInterrupt:
            print("Đã thoát chương trình")
        break


if __name__ == "__main__":
    main()
