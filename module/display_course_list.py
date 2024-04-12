from colorama import Fore
import time
from module.random_fact import random_fact
from bs4 import BeautifulSoup
from tabulate import tabulate


def display_course_list(session):
    print(Fore.BLUE + "Lựa chọn:")
    print(Fore.BLUE + "1. Kế hoạch (KH)")
    print(Fore.BLUE + "2. Ngoài kế hoạch (NKH)")
    choice = input(Fore.BLUE + "Chọn (1/2): ")
    if choice == "1":
        typeId = "KH"
    elif choice == "2":
        typeId = "NKH"
    while True:
        response = session.get(
            f"https://regist.vlu.edu.vn/DangKyHocPhan/DanhSachHocPhan?typeId={typeId}&id="
        )
        print(Fore.YELLOW + f"Đang lấy thông tin các môn học...-{random_fact()}")
        if response.status_code != 200:
            print(Fore.RED + f"Server lỗi, đang thử lại...-{random_fact()}")
            time.sleep(3)
        else:
            break
    soup = BeautifulSoup(response.text, "html.parser")
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
