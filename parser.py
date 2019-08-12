import requests
import re
from bs4 import BeautifulSoup
from multiprocessing import Pool


def get_html(url):
    r = requests.get(url)
    return r.text


def get_numbers(html):
    soup = BeautifulSoup(html, 'lxml')

    numbers = []

    text = soup.find('div')
    text = ' '.join(text.findAllNext(text=True))

    number = re.findall(r'(((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?([\d\-]{7,9}))', text)
    format_ = re.compile(r'\D+')

    for elem in number:
        elem = str(elem[0])
        format_number = format_.sub('', elem)

        if format_number != '':
            if len(format_number) == 7:
                numbers.append('8495' + format_number)
            elif len(format_number) == 10:
                numbers.append('8' + format_number)
            elif len(format_number) == 11:
                if format_number[0] == '8':
                    numbers.append(format_number)
                elif format_number[0] == '7':
                    numbers.append('8' + format_number[1:])
    return numbers


def make_all(url):
    html = get_html(url)
    numbers = get_numbers(html)
    print(numbers)
    return numbers


def main():
    sites = ['https://hands.ru/company/about', 'https://repetitors.info/']

    with Pool(40) as p:
        p.map(make_all, sites)


if __name__ == '__main__':
    main()
