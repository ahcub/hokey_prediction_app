from html_table_parser.parser import HTMLTableParser
from lxml.html import fromstring, tostring
from pandas import DataFrame
from numpy import array
import pandas as pd

data = {
    'hits_count_mult_success_percent': {
        'Team1':
            {
                'Dominik Kubalík': 61.5429,
                'Viktor Hübl': 55.9860,
                'Rostislav Olesz': 79.9362,
            },
        'Team2':
            {
                'Nicholas Johnson': 58.3758,
                'Jakub Valský': 55.5128,
                'Marcel Haščák': 50.0100,
            }
    },
    'match_based_stat': {
        'Team1':
            {
                'Dominik Kubalík': 61.5429,
                'Viktor Hübl': 55.9860,
                'Rostislav Olesz': 79.9362,
            },
        'Team2':
            {
                'Nicholas Johnson': 58.3758,
                'Jakub Valský': 55.5128,
                'Marcel Haščák': 50.0100,
            }
    }
}
if __name__ == '__main__':
    a = 'http://www.hokej.cz/tipsport-extraliga/player-stats/detailni?stats-menu-section=shots&stats-filter-season=2015&stats-filter-competition=5574&do=stats-view-pager-all'

    import requests

    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate, sdch",
               "Accept-Language": "en-US,en;q=0.8,uk;q=0.6,ru;q=0.4",
               "Cache-Control": "max-age=0",
               "Connection": "keep-alive",
               "Cookie": "bblpasync=1449584613947; bblosync=1449585458940; __gfp_64b=sGN1O8XUlhJbt4ZWEMs2RKkIqL7nbIkleQ1NtqNQzx..M7; ibbid=BBID-01-01242986113897072; PHPSESSID=0i2j9hv3h877a3tullca1vfie4; nette-browser=gnqmgg5fbu; _ga=GA1.2.834154638.1449584608; _gat=1; __utmt=1; __utmt_trac2=1; __utma=47860542.834154638.1449584608.1449584610.1449584608.1; __utmb=47860542.4.10.1449584610; __utmc=47860542; __utmz=47860542.1449584610.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); popupShown=true; scrollingDivDisabled=true",
               "Host": "www.hokej.cz",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36", }

    # header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
    # r = requests.get(a, headers=headers)

    # v = get_url_response(a)
    # print(v)
    #

    # print(r.content)
    # doc = fromstring(r.content)
    # c = doc.find_class('table-stats')
    #
    # table_string = tostring(c[0])
    # p = HTMLTableParser()
    # p.feed(table_string.decode('utf-8'))
    #
    # for table_set in p.tables:
    #     for table in table_set[1:]:
    #         scoring_probability = float(table[7]) * float(table[-1])
    #         if scoring_probability > 15.0:
    #             a = '%s %f | %s %f' % (table[1], scoring_probability, table[1], scoring_probability)
    #             print(a)

    with open('example.html', 'rb') as file_:
        s = file_.read().decode('utf-8')
        p = HTMLTableParser()
        p.feed(s)
        table_set = array([table[1:] for table_group in p.tables for table in table_group])

        df = DataFrame(table_set[1:], columns=table_set[0])
        df = df.convert_objects(convert_numeric=True)
        # for team in df.get('Tým').unique():
        #     print(team)
        multiplication_result = df.get('S/Z') * df.get('RÚS')
        result_df = DataFrame({'Name': df.get('Jméno'), 'Team': df.get('Tým'), 'Probability':multiplication_result})
        for team, indexes in result_df.groupby('Team').groups.items():
            print(result_df.loc[indexes, ['Name', 'Probability']].set_index('Name').to_dict()['Probability'])
        # for table_set in p.tables:
        #     for table in table_set[1:]:
        #         scoring_probability = float(table[7]) * float(table[-1])
        #         if scoring_probability > 50.0:
        #
        #             a = '%20s %3.4f | %20s %3.4f' %(table[1], scoring_probability, table[1], scoring_probability)
        #             print(a)
