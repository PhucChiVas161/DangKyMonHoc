from colorama import Fore, Style
from module.random_fact import random_fact
import time
from bs4 import BeautifulSoup
import tabulate

def display_class_list(session, typeId, course_id):
    print(Fore.YELLOW + f"Đang lấy thông tin các lớp học ... -{random_fact()}")
    while True:
        response = session.get(
            f"https://regist.vlu.edu.vn/DangKyHocPhan/DanhSachLopHocPhan?id={course_id}&registType={typeId}&scheduleStudyUnitID=")
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
    headers_theory = ["STT", "Loại", "Mã LHP",
                      "SL còn lại", "Lịch Học", "Ghi Chú"]
    headers_practice = ["STT", "Mã lớp", "SL", 'Lịch Học', 'Ghi chú']
    headers_exam = ["STT", 'Loại', 'Mã LHP', 'Lớp sinh hoạt', 'SL', 'Ghi chú']

    ly_thuyet_table = [row[:-1] for row in ly_thuyet]
    thuc_hanh_table = [row[:-1] for row in thuc_hanh]
    thi_table = [row[:-1] for row in thi]
    if ly_thuyet:
        selected_row_theory = None
        print(Fore.GREEN + Style.BRIGHT + "Bảng Lý thuyết:")
        print(Fore.GREEN + Style.NORMAL + (tabulate(ly_thuyet_table, headers_theory,
              tablefmt=table, showindex=True)))
    if thuc_hanh:
        selected_row_practice = None
        print(Fore.BLUE + Style.BRIGHT + "\nBảng Thực hành:")
        print(Fore.BLUE + Style.NORMAL +(tabulate(thuc_hanh_table, headers_practice,
                       tablefmt=table, showindex=True)))
    if thi:
        selected_row_exam = None
        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "\nBảng Thi:")
        print(Fore.LIGHTMAGENTA_EX + Style.NORMAL +(tabulate(thi_table, headers_exam, tablefmt=table, showindex=True)))

    class_id_theory = ''
    class_id_practice = ''
    class_id_exam = ''
    if ly_thuyet:
        row_number_theory = int(input(Fore.GREEN + Style.BRIGHT + "Nhập STT lớp cần đăng ký: "))
        selected_row_theory = ly_thuyet[row_number_theory]
        class_id_theory = selected_row_theory[-1]
    if thuc_hanh:
        row_number_practice = int(
            input(Fore.BLUE + Style.BRIGHT +"Nhập STT lớp THỰC HÀNH cần đăng ký: "))
        selected_row_practice = thuc_hanh[row_number_practice]
        class_id_practice = selected_row_practice[-1]
    if thi:
        row_number_exam = int(input(Fore.MAGENTA + Style.BRIGHT + "Nhập STT lớp THI cần đăng ký: "))
        selected_row_exam = thi[row_number_exam]
        class_id_exam = selected_row_exam[-1]
    url_regist_class_id = f"https://regist.vlu.edu.vn/DangKyHocPhan/DangKy?Hide={class_id_theory or class_id_exam}|{
        class_id_practice}|&acceptConflict=false&classStudyUnitConflictId=&RegistType={typeId}&ScheduleStudyUnitID="
    return url_regist_class_id
