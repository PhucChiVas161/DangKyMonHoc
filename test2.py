from bs4 import BeautifulSoup
from tabulate import tabulate
from colorama import Fore


f = open("./draft/DanhSachHocPhanNgoaiKeHoach.txt", encoding="utf-8")
data = f.read()
soup = BeautifulSoup(data, 'html.parser')
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
           'STC', 'Số lượng LHP', 'Mã lớp']
print(Fore.LIGHTCYAN_EX + (tabulate(data, headers,
      tablefmt='fancy_grid', showindex="always")))
row_number = int(input("Nhập STT bạn muốn chọn: "))
selected_row = data[row_number]
print(f"Class ID là: {selected_row[-1]}")
