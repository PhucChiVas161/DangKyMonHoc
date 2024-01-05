from bs4 import BeautifulSoup
from tabulate import tabulate

f = open("./draft/DanhSachLopHocPhan.txt", encoding="utf-8")
data = f.read()

soup = BeautifulSoup(data, 'html.parser')
table = soup.find('table')
rows = table.find_all('tr', class_='')
data = []
selected_row = None
for row in rows[1:]:  # Bỏ qua hàng tiêu đề
    cells = row.find_all('td')
    row_data = [cell.get_text(strip=True)
                for cell in cells if not cell.find('span')]

    link = row.find('input')
    if link:
        id_attr = link.get('id')
        row_data.append(id_attr)
    data.append(row_data)


# Phân chia dữ liệu thành lý thuyết và thực hành
ly_thuyet = []
thuc_hanh = []

for item in data:
    if item and item[1] == 'Lý thuyết':
        del item[0]
        del item[2]
        del item[4]
        ly_thuyet.append(item)
    elif item and item[0] == '':
        del item[0]
        thuc_hanh.append(item)

table = 'fancy_grid'
# Xuất bảng cho lý thuyết
if ly_thuyet:
    headers = ["Loại", "Mã LHP",
               "SL còn lại", "Lịch Học", "Ghi Chú", "Code lớp"]
    print("Bảng Lý thuyết:")
    print(tabulate(ly_thuyet, headers=headers, tablefmt=table))
    row_number = int(input("Nhập STT lớp lý thuyết: "))
    selected_row_theory = ly_thuyet[row_number]
# Xuất bảng cho thực hành
if thuc_hanh:
    headers2 = ["Mã lớp", "SL", 'Lịch Học', 'Ghi chú', 'Code lớp']
    print("\nBảng Thực hành:")
    print(tabulate(thuc_hanh, headers=headers2, tablefmt=table))
    row_number = int(input("Nhập STT lớp thực hành: "))
    selected_row_practice = thuc_hanh[row_number]

print(f"Class ID là: {selected_row[-1]}")
print(f"Class ID là: {selected_row[-1]}")
