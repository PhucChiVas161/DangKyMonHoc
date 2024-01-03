from bs4 import BeautifulSoup
from tabulate import tabulate
from pprint import pprint

f = open("./draft/DanhSachLopHocPhan.txt", encoding="utf-8")
data = f.read()

soup = BeautifulSoup(data, 'html.parser')


table = soup.find('table')
# print(table)
tbody = table.find('tbody')
# print(tbody)
trCount = tbody.find_all(recursive=False)
# pprint(trCount)
headers = ["#", "Hình thức", 'Mã LHP', 'SL còn lại', 'Lịch học', "?",	'Ghi chú' , "ID"]
headers2 = ["Mã LHP",	"SL còn lại",	"Lịch học",	"Ghi chú", "ID"]

for i in range(0, len(trCount)-1):
    row = trCount[i] #! td[]
    if(i%2==0):
        data = []

        cells = row.find_all('td') #! td[]
        row_data = [cell.get_text(strip=True) for cell in cells if not cell.find('span') ]

        del row_data[3]

        # ? Add id from input tag
        inputTag=row.find('input')
        if(inputTag):
            row_data.append(inputTag.get('id'))
        else:
            row_data.append('null')

        data.append(row_data)
        
        print(tabulate(data, headers=headers, tablefmt='grid'))

    else:
        cells = row.find_all('tr') #! td[]
        data = []
        for t in cells[1:]:
            td = t.find_all('td')
            row_data = []
            for tdi in range(0,len(td)-1):
                tde = td[tdi]
                if(tdi==0):
                    inp = tde.find('input')
                    if inp:
                        id_attr = inp.get('id')
                        row_data.append(id_attr)
                else:
                    row_data.insert(tdi-1,tde.getText(strip=True))
                    
            data.append(row_data)

        print(tabulate(data, headers=headers2, tablefmt='grid'))



# if __name__ == "__main__":

