from bs4 import BeautifulSoup
from tabulate import tabulate

f = open("./draft/DanhSachHocPhanNgoaiKeHoach.txt", encoding="utf-8")
data = f.read()

soup = BeautifulSoup(data, 'html.parser')
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
