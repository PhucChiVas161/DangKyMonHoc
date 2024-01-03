from bs4 import BeautifulSoup
from tabulate import tabulate

f = open("./draft/RutGon.txt", encoding="utf-8")
data = f.read()

soup = BeautifulSoup(data, 'html.parser')
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

# Xuất bảng cho thực hành
if thuc_hanh:
    headers2 = ["Mã lớp", "SL", 'Lịch Học', 'Ghi chú', 'Code lớp']
    print("\nBảng Thực hành:")
    print(tabulate(thuc_hanh, headers=headers2, tablefmt=table))
