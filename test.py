from bs4 import BeautifulSoup
from tabulate import tabulate

f = open("./draft/DanhSachLopCo1Loai.txt", encoding="utf-8")
data = f.read()

soup = BeautifulSoup(data, "html.parser")
table = soup.find("table")
rows = table.find_all("tr", class_="")
data = []
for row in rows[1:]:  # Bỏ qua hàng tiêu đề
    cells = row.find_all("td")
    row_data = [cell.get_text(strip=True) for cell in cells if not cell.find("span")]

    link = row.find("input")
    if link:
        id_attr = link.get("id")
        row_data.append(id_attr)
    data.append(row_data)

# Phân chia dữ liệu thành lý thuyết và thực hành
ly_thuyet = []
thuc_hanh = []
thi = []

for item in data:
    if item and item[1] == "Lý thuyết":
        del item[0]
        del item[2]
        del item[4]
        ly_thuyet.append(item)
    elif item and item[1] == "Thi":
        del item[0]
        del item[4]
        del item[4]
        del item[4]
        thi.append(item)
    elif item and item[0] == "":
        del item[0]
        thuc_hanh.append(item)

table = "fancy_grid"

# Ẩn cột "Code lớp" và "ID Lớp học" khi xuất bảng
headers_theory = ["STT", "Loại", "Mã LHP", "SL còn lại", "Lịch Học", "Ghi Chú"]
headers_practice = ["STT", "Mã lớp", "SL", "Lịch Học", "Ghi chú"]
headers_exam = ["STT", "Loại", "Mã LHP", "Lớp sinh hoạt", "SL", "Ghi chú"]

ly_thuyet_table = [row[:-1] for row in ly_thuyet]
thuc_hanh_table = [row[:-1] for row in thuc_hanh]
thi_table = [row[:-1] for row in thi]
# Xuất bảng cho lý thuyết
if ly_thuyet:
    selected_row_theory = None
    print("Bảng Lý thuyết:")
    print(tabulate(ly_thuyet_table, headers_theory, tablefmt=table, showindex=True))

# Xuất bảng cho thực hành
if thuc_hanh:
    selected_row_practice = None
    print("\nBảng Thực hành:")
    print(tabulate(thuc_hanh_table, headers_practice, tablefmt=table, showindex=True))

# Xuất bảng cho thi
if thi:
    selected_row_exam = None
    print("\nBảng Thi:")
    print(tabulate(thi_table, headers_exam, tablefmt=table, showindex=True))

course_id_theory = ""
course_id_practice = ""
course_id_exam = ""
if ly_thuyet:
    row_number_theory = int(input("Nhập STT lớp cần đăng ký: "))
    selected_row_theory = ly_thuyet[row_number_theory]
    course_id_theory = selected_row_theory[-1]
if thuc_hanh:
    row_number_practice = int(input("Nhập STT lớp THỰC HÀNH cần đăng ký: "))
    selected_row_practice = thuc_hanh[row_number_practice]
    course_id_practice = selected_row_practice[-1]
if thi:
    row_number_exam = int(input("Nhập STT lớp THI cần đăng ký: "))
    selected_row_exam = thi[row_number_exam]
    course_id_exam = selected_row_exam[-1]

url = f"http/abc.com/{course_id_theory or course_id_exam}|{course_id_practice}|"
print(url)
