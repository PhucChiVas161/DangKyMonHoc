from bs4 import BeautifulSoup
from tabulate import tabulate
from colorama import Fore, Style

EXCLUDE_COURSES = ["Học phần: Đánh giá năng lực tiếng Anh đầu ra "]

f = open("./draft/DanhSachLopHocPhan.txt", encoding="utf-8")
data = f.read()
soup = BeautifulSoup(data, 'html.parser')
table = soup.find('table')
tbody = table.find('tbody')
trCount = tbody.find_all(recursive=False)

legend = soup.find("legend").get_text()

def viewTheoryAndPracticeClass():
    for i in range(0, len(trCount)):
        row = trCount[i]
        if (i % 2 == 0):
            data = []
            cells = row.find_all('td')
            row_data = [cell.get_text(strip=True)
                        for cell in cells if not cell.find('span') and cell.get_text(strip=True) != '']
            del row_data[2]
            inputTag = row.find('input')
            if (inputTag):
                row_data.append(inputTag.get('id'))
            else:
                row_data.append('null')
            data.append(row_data)
            if (len(row_data) == 6):
                headers = ['Loại', 'Mã LHP', 'Số lượng',
                        'Lịch học', 'Ghi chú', 'ID lớp lý thuyết']
            else:
                headers = ['Loại', 'Mã LHP', 'Số lượng',
                        'Lịch học', 'ID lớp lý thuyết']
            print(Style.BRIGHT + Fore.GREEN + '\n Bảng lý thuyết:')
            print(Fore.GREEN + Style.NORMAL +
                (tabulate(data, headers=headers, tablefmt='fancy_grid')))
        else:
            headers2 = []
            cells = row.find_all('tr')
            data = []
            for t in cells[1:]:
                tds = t.find_all('td')
                row_data_practice = []
                for tdi in range(0, len(tds)):
                    tde = tds[tdi]
                    if (tdi == 0):
                        inp = tde.find('input')
                        if inp:
                            id_attr = inp.get('id')
                            row_data_practice.append(id_attr)
                    else:
                        row_data_practice.insert(tdi-1, tde.getText(strip=True))
                row_data_no_empty = list(filter(None, row_data_practice))
                data.append(row_data_no_empty)
                if (len(row_data_no_empty) == 5):
                    headers2 = ["Mã LHP", "SL còn lại",
                                "Lịch học", "Ghi chú", 'ID lớp thực hành']
                else:
                    headers2 = ["Mã LHP", "SL còn lại",
                                "Lịch học", 'ID lớp thực hành']
            print(Fore.BLUE + Style.BRIGHT +
                '\n Bảng thực hành tương ứng với:', row_data[1])
            print(Fore.BLUE + Style.NORMAL + (tabulate(data,
                headers=headers2, tablefmt='mixed_grid')))


def viewTheoryClass():
    for i in range(0, len(trCount)):
        row = trCount[i]
        data = []
        cells = row.find_all('td')
        row_data = [cell.get_text(strip=True)
                    for cell in cells if not cell.find('span') and cell.get_text(strip=True) != '']
        del row_data[2]
        inputTag = row.find('input')
        if (inputTag):
            row_data.append(inputTag.get('id'))
        else:
            row_data.append('null')
        data.append(row_data)
        if (len(row_data) == 6):
            headers = ['Loại', 'Mã LHP', 'Số lượng',
                    'Lịch học', 'Ghi chú', 'ID lớp lý thuyết']
        else:
            headers = ['Loại', 'Mã LHP', 'Số lượng',
                    'Lịch học', 'ID lớp lý thuyết']
        print(Style.BRIGHT + Fore.GREEN + '\n Bảng lý thuyết:')
        print(Fore.GREEN + Style.NORMAL +
            (tabulate(data, headers=headers, tablefmt='fancy_grid')))


if __name__ == "__main__":
    if(legend in EXCLUDE_COURSES):
        viewTheoryClass()
    else:
        viewTheoryAndPracticeClass()