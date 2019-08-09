import requests
import re
from bs4 import BeautifulSoup

sites = ['https://hands.ru/company/about', 'https://repetitors.info/']


def parser (site):
    mas = []
    response = requests.get(site)
    root = BeautifulSoup(response.text, 'html.parser')

    text = root.find('div')
    text = ' '.join(text.findAllNext(text=True))

    number = re.findall(r'(((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?([\d\-]{7,9}))', text)
    form = re.compile(r'\D+')

    for elem in number:
        elem = str(elem[0])
        format_number = form.sub('', elem)

        if format_number != '':
            if len(format_number) == 7:
                mas.append('8495' + format_number)
            elif len(format_number) == 10:
                mas.append('8' + format_number)
            elif len(format_number) == 11:
                if format_number[0] == '8':
                    mas.append(format_number)
                elif format_number[0] == '7':
                    mas.append('8' + format_number[1:])

    print(mas)


if __name__ == '__main__':
    for site in sites:
        parser(site)
