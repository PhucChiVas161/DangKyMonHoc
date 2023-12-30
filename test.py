from bs4 import BeautifulSoup
from tabulate import tabulate

f = open("./draft/RutGon.txt", encoding="utf-8")
data = f.read()

soup = BeautifulSoup(data, 'html.parser')
table = soup.find('table')
rows = table.find_all('tr')
data = []
for row in rows[1:]:  # Bỏ qua hàng tiêu đề
    cells = row.find_all('td')
    row_data = [cell.get_text(strip=True)
                for cell in cells if not cell.find('span')]
    # Lấy đoạn mã từ thẻ <input>
    link = row.find('input')
    if link:
        id_attr = link.get('id')
        row_data.append(id_attr)
    else:
        row_data.append('')
    data.append(row_data)

# Find the index of the "Lớp sinh hoạt" header and remove it from the headers
header_index = -1
headers = ["STT", "Loai", "Mã LHP", "Lớp sinh hoạt",
           "SL còn lại", "Lịch học", "Số tiền", "Ghi chú", "Code lớp"]
for i, header in enumerate(headers):
    if header == "Lớp sinh hoạt":
        header_index = i
        break

if header_index != -1:
    headers.pop(header_index)

# Remove the "Lớp sinh hoạt" column from the table data
for row_data in data:
    if len(row_data) > header_index:
        row_data.pop(header_index)

print(tabulate(data, headers, tablefmt='fancy_grid'))
