from urllib.parse import urlencode
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import time

# Define search words
lst_keywords = ['Github']

# Define dates
date_start, date_end = '2023-01-01', '2023-01-01'

# Define output path
export_path = '/Users/../../../'


def parse_naver_search(SEARCH='chatgpt', DATE='2023.01.01', PAGE=1):
    DATE_ = DATE.replace('.', '')
    search_params = urlencode({"query": SEARCH})
    url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&{search_params}&sort=2&photo=0&field=0&pd=3&ds={DATE}&de={DATE}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:rp:from{DATE_}to{DATE_},a:all&start={PAGE}'
    response = urlopen(url)
    soup = BeautifulSoup(response, "html.parser")  # html에 대하여 접근할 수 있도록
    res = soup.select('a.news_tit')

    df = pd.DataFrame()
    for _ in res:
        temp = pd.DataFrame({'DATE': [date], 'KEYWORD': [SEARCH], 'TITLE': _.get('title'), 'URL': _.get('href')})
        df = pd.concat([df, temp], axis=0, ignore_index=True)
        del temp

    return df


if __name__ == '__main__':
    lst_date = pd.date_range(start=date_start, end=date_end).strftime('%Y.%m.%d').tolist()
    export_file_name = f'naver_search_{date_start}_{date_end}.csv'
    result = pd.DataFrame()
    for keyword in lst_keywords:
        print(f'KEYWORD: {keyword}..')
        for date in lst_date:
            for page in range(1, 10000, 10):
                print(f'SEARCH={keyword}, DATE={date}, PAGE={page}')
                temp = parse_naver_search(SEARCH=keyword, DATE=date, PAGE=page)
                if len(temp) == 0:
                    break
                else:
                    result = pd.concat([result, temp], axis=0, ignore_index=True)
                time.sleep(3)
                del temp
            del date
        del keyword

    export = export_path + export_file_name
    print(f'Exporting {export}')
    result.to_csv(export, encoding='utf-8-sig', index=False)