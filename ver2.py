from bs4 import BeautifulSoup
from tabulate import tabulate
from colorama import Fore, Style

f = open("./draft/DanhSachLopHocPhan.txt", encoding="utf-8")
data = f.read()
soup = BeautifulSoup(data, 'html.parser')
table = soup.find('table')
tbody = table.find('tbody')
trCount = tbody.find_all(recursive=False)

def viewTheoryClass(row, stt):
    data = []
    cells = row.find_all('td')
    row_data = [cell.get_text(strip=True) for cell in cells if not cell.find('span') and cell.get_text(strip=True) != '']
    del row_data[2]
    row_data.insert(0,stt)
    inputTag = row.find('input')
    if (inputTag):
        row_data.append(inputTag.get('id'))
    else:
        row_data.append('null')
    data.append(row_data)
    if (len(row_data) == 6):
        headers = ['STT', 'Loại', 'Mã LHP', 'Số lượng', 'Lịch học', 'Ghi chú', 'ID lớp lý thuyết']
    else:
        headers = ['STT', 'Loại', 'Mã LHP', 'Số lượng', 'Lịch học', 'ID lớp lý thuyết']
    print(Style.BRIGHT + Fore.GREEN + '\n Bảng lý thuyết:')
    print(Fore.GREEN + Style.NORMAL + (tabulate(data, headers=headers, tablefmt='fancy_grid')))
    return row_data[2]

def viewTheoryAndPracticeClass():
    stt = 1
    for i in range(0, len(trCount)):
        row = trCount[i]
        if (i % 2 == 0):
            lhp = viewTheoryClass(row, stt)
            stt+=1
        else:
            span = row.find('span')
            if(span!=None):
                if("thực hành" in span.get_text()):
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
                        row_data_no_empty.insert(0,stt)
                        stt+=1
                        data.append(row_data_no_empty)
                        if (len(row_data_no_empty) == 5):
                            headers2 = ['STT', "Mã LHP", "SL còn lại",
                                        "Lịch học", "Ghi chú", 'ID lớp thực hành']
                        else:
                            headers2 = ['STT', "Mã LHP", "SL còn lại",
                                        "Lịch học", 'ID lớp thực hành']
                    print(Fore.BLUE + Style.BRIGHT + '\n Bảng thực hành tương ứng với:', lhp)
                    print(Fore.BLUE + Style.NORMAL + (tabulate(data, headers=headers2, tablefmt='mixed_grid')))
            else:
                viewTheoryClass(row, stt)
                stt+=1


if __name__ == "__main__":
    viewTheoryAndPracticeClass()