import re
import csv
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("untitled.html"), "html.parser")
articles = soup.find_all('a')

print('find %d articles' % len(articles))
print('extract to source.csv...')

input_data = [['date', 'title', 'url']]
pattern = re.compile("dataserno=\d+")
for link in reversed(articles):
    input_data += [[pattern.search(link['href']).group(0)[10:18], link.string, link['href']]]

with open('source.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for data in input_data:
        writer.writerow(data)

print('done.')
