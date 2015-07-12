import csv
import re
import subprocess
import urllib.request
import time
from datetime import date, timedelta

import xlrd
from bs4 import BeautifulSoup


def is_data_exist(row):
    result = False
    for cell in row:
        result = result or cell
    return bool(result)

domain = "http://www.phldcc.gov.tw"
mserno = "201110060008"
serno = "201110130001"
contlink = "ap/unit1_view.jsp"
lastday = (date.today() - timedelta(days=1)).strftime('%Y%m%d')
lastday = '20150703'
try_times = ['0001', '0002', '0003', '0004', '0005']

print('search for %s...' % lastday)
for x in try_times:
    #time.sleep(3)
    url = ("%s/ch/home.jsp?mserno=%s&serno=%s&dataserno=%s%s&contlink=%s") % (
        domain, mserno, serno, lastday, x, contlink)
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    text1 = soup.find_all(href=re.compile(".xls"))
    if not text1:
        print('no data in %s%s' % (lastday, x))
    else:
        pattern = re.compile("\d+\.xls")
        file_name = pattern.search(str(text1[0])).group(0)
        url_path = domain + "/uploaddowndoc?file=/pubpenghu/unitdata/" + file_name + "&flag=doc"
        urllib.request.urlretrieve(url_path, file_name)
        print('download %s...' % file_name)

        ### to csv
        workbook = xlrd.open_workbook(file_name)
        worksheet = workbook.sheet_by_index(0)
        num_rows = worksheet.nrows - 1
        input_data = [['animal_opendate', 'animal_found_place', 'animal_pedigree',
            'animal_sex', 'animal_bodytype', 'animal_colour', 'animal_chip_number',
            'animal_entry_reason']]
        curr_row = 1
        while curr_row < num_rows:
            curr_row += 1
            row = worksheet.row(curr_row)
            tmp_input_data = [(int(x.value) if type(x.value) == type(0.0) else x.value) for x in row]
            if is_data_exist(tmp_input_data):
                input_data += [tmp_input_data]

        csv_name = '%s.csv' % file_name[:-4]
        with open(csv_name, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for data in input_data[:-2]:
                    writer.writerow(data)
        print('write %s...' % csv_name)

        cmd = 'rm %s' % file_name
        subprocess.call(cmd, shell=True)
        print('delete %s...' % file_name)


