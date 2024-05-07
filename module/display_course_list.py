from colorama import Fore
import time
from module.random_fact import random_fact
from bs4 import BeautifulSoup
from tabulate import tabulate

# Khai báo 2 biến toàn cục để lưu trữ response của mỗi option
CACHED_RESPONSE_PLAN = None
CACHED_RESPONSE_EXTRA = None


def display_course_list(session):
    global CACHED_RESPONSE_PLAN, CACHED_RESPONSE_EXTRA

    print(Fore.BLUE + "Lựa chọn:")
    print(Fore.BLUE + "1. Kế hoạch")
    print(Fore.BLUE + "2. Ngoài kế hoạch (Khả dụng khi mở đăng ký bổ sung)")
    choice = input(Fore.BLUE + "Chọn (1/2): ")

    if choice == "1":
        typeId = "KH"
        cached_response = CACHED_RESPONSE_PLAN
    elif choice == "2":
        typeId = "NKH"
        cached_response = CACHED_RESPONSE_EXTRA

    # Kiểm tra xem biến cached_response có giá trị không
    if cached_response is not None:
        print(Fore.YELLOW + "Đang sử dụng dữ liệu được lưu trữ...")
        soup = BeautifulSoup(cached_response, "html.parser")
    else:
        while True:
            print(Fore.YELLOW + f"Đang lấy thông tin các MÔN học...-{random_fact()}")
            response = session.get(
                f"https://regist.vlu.edu.vn/DangKyHocPhan/DanhSachHocPhan?typeId={typeId}&id="
            )
            if response.status_code != 200:
                print(Fore.RED + f"Server lỗi, đang thử lại...-{random_fact()}")
                time.sleep(1)
            else:
                # Lưu response vào biến cached_response tương ứng
                if choice == "1":
                    CACHED_RESPONSE_PLAN = response.text
                else:
                    CACHED_RESPONSE_EXTRA = response.text
                cached_response = response.text
                break

    soup = BeautifulSoup(cached_response, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")
    data = []
    selected_row = None
    for row in rows[1:]:
        cells = row.find_all("td")
        row_data = [cell.get_text(strip=True) for cell in cells[:5]]
        link = row.find("a")
        if link:
            href = link.get("href")
            start_index = href.index("('") + 2
            end_index = href.index("',")
            course_id = href[start_index:end_index]
            row_data.append(course_id)
        else:
            row_data.append("")
        data.append(row_data)
    headers = [
        "STT",
        "STT (Đừng quan tâm)",
        "Mã học phần",
        "Tên học phần",
        "STC",
        "Số lượng LHP",
    ]
    print(
        Fore.LIGHTCYAN_EX
        + (tabulate(data, headers, tablefmt="fancy_grid", showindex=True))
    )
    row_number = int(input("Nhập STT(Bên trái ngoài cùng) MÔN HỌC cần đăng ký: "))
    selected_row = data[row_number]
    course_id = selected_row[-1]
    return course_id, typeId
