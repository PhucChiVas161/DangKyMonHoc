from bs4 import BeautifulSoup
import requests
from tabulate import tabulate

url = "https://regist.vlu.edu.vn"

username = "207CT40540"
password = "16012002"

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

data = {
    "username": username,
    "password": password
}

session = requests.Session()

response = session.post(url, headers=headers, data=data)

if '<a href="/Login/Logout">Đăng xuất</a>' in response.text:
    print('Đăng nhập thành công')
    # Lưu cookie vào session
    session.cookies.update(response.cookies)

    print("Lựa chọn:")
    print("1. Kế hoạch (KH)")
    print("2. Ngoài kế hoạch (NKH)")

    choice = input("Chọn (1/2): ")

    if choice == "1":
        typeId = "KH"
    elif choice == "2":
        typeId = "NKH"

    response = session.get(
        url + f"/DangKyHocPhan/DanhSachHocPhan?typeId={typeId}&id="
    )

    if '<b style="color:red">Hệ Thống Đang Xử Lý. Quay lại sau 3 giây</b>' in response.text:
        print("Dizzconme web lol sập hoài. Vui lòng thử lại sau :)))))")
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
                   'STC', 'Số lượng LHP', 'Mã lớp']
        print(tabulate(data, headers, tablefmt='grid'))

else:
    print('Đăng nhập thất bại')
